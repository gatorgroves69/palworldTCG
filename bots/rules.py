"""RuleBot: fast rule-of-thumb decisions, no lookahead.

Used on its own as a baseline, and inside HeuristicBot's lookahead for every
decision other than the searching player's main-phase action (targets,
blocks, the Quick step). Reads only public information, its own hand, and
what its own effects revealed.
"""
from __future__ import annotations

from engine.actions import Attack, EndMain, Pass, PlayCard, UseInterrupt
from engine.state import CardInstance

from .base import Bot
from .evaluate import HAND_CARD, INTERRUPT_IN_HAND, LIFE, pal_value

LUCKY_RATE = 0.18  # rough chance a damage check hits a lucky card (8 of ~45)


def effect_damage(game, source: CardInstance, target: CardInstance, amount: int) -> int:
    """Damage an effect from `source` would really deal to `target` (Suzaku etc.)."""
    for ps in game.players:
        for x in ps.base:
            amount = x.impl.modify_effect_damage(game, x, source, target, amount)
    return amount


def card_worth(game, c: CardInstance) -> float:
    """Rough value of a card in hand, used for discards and sacrifices."""
    return c.defn.cost + (1.5 if c.kw("interrupt") else 0) + (1 if c.defn.lucky else 0)


class RuleBot(Bot):
    name = "rules"

    # ------------------------------------------------------------ mulligan
    def choose_redraw(self, game, player):
        """Redraw if there's no Pal we can deploy by turn 2 (◇4 or less), or
        the hand is clogged with 3+ cards costing ◇7 or more."""
        hand = game.players[player].hand
        early = any(c.is_pal and c.defn.cost <= 4 for c in hand)
        heavy = sum(1 for c in hand if c.defn.cost >= 7)
        return not early or heavy >= 3

    # ------------------------------------------------------------ actions
    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        return self.simple_main(game, player, actions)

    def simple_main(self, game, player, actions):
        """Baseline main phase: play the most expensive card, then attack the player."""
        plays = [a for a in actions if isinstance(a, PlayCard)]
        if plays:
            return max(plays, key=lambda a: (game.card(a.uid).defn.cost, -(a.mode or 0)))
        attacks = [a for a in actions if isinstance(a, Attack) and a.target_uid is None]
        if attacks:
            return attacks[0]
        return next((a for a in actions if isinstance(a, EndMain)), actions[0])

    def quick_step(self, game, me, actions):
        """Defender's window, in order of preference:
        - Ignis Breath (or any Quick 'deal N damage' event) if it kills the attacker,
          alone or together with the battle damage it's about to take;
        - Crystal Breath on a Strike-2+ hit at us (Strike -3 and a lock);
        - Aurora Guide with a lucky card to put on top;
        - an Interrupt when the hit costs more than the cards spent."""
        b = game.battle
        if b is None:
            return Pass()
        att = b.attacker
        loss = self.expected_loss(game, me, b)
        hand = game.players[me].hand
        events = {game.card(a.uid).code: a for a in actions if isinstance(a, PlayCard)}
        ignis = events.get("TD01-011")
        if ignis is not None:
            dmg = effect_damage(game, game.card(ignis.uid), att, 500)
            back = game.power(b.target) if b.target is not None and b.target.is_pal else 0
            hp = game.power(att) - att.damage
            kills_now = dmg >= hp
            kills_in_battle = back > 0 and back < hp <= dmg + back
            if (kills_now or kills_in_battle) and pal_value(game, att) + max(loss, 0) > HAND_CARD:
                return ignis
        if loss <= 0:
            return Pass()
        crystal = events.get("TD01-022")
        if crystal is not None and b.target is None and game.strike(att) >= 2 and loss > HAND_CARD:
            return crystal
        # Aurora Guide + a lucky card in hand guarantees the damage check is cancelled.
        if b.target is None:
            aurora = [a for a in actions if isinstance(a, PlayCard)
                      and game.card(a.uid).code == "BP01-048"]
            if aurora and any(c.defn.lucky for c in hand) and loss >= 2 * LIFE:
                return aurora[0]
        ints = [a for a in actions if isinstance(a, UseInterrupt)]
        if not ints:
            return Pass()
        # Cheapest interrupt card; pay with a soul if we can, else the worst other card.
        by_soul = [a for a in ints if a.discard_uid is None]
        pool = by_soul or ints
        pick = min(pool, key=lambda a: (card_worth(game, game.card(a.uid)),
                                        card_worth(game, game.card(a.discard_uid))
                                        if a.discard_uid is not None else 0))
        # Worth it if the hit costs more than the cards spent to stop it.
        cost = HAND_CARD + INTERRUPT_IN_HAND + (0.5 if pick.discard_uid is None else HAND_CARD)
        life = game.players[me].life
        lethal = b.target is None and game.strike(att) >= life
        return pick if loss > cost or lethal else Pass()

    def expected_loss(self, game, me, b) -> float:
        att = b.attacker
        if b.target is None:
            s = game.strike(att)
            return s * LIFE * (1 - LUCKY_RATE) if s > 0 else 0.0
        t = b.target
        if t.owner != me:
            return 0.0
        dies = t.damage + game.power(att) >= game.power(t) > 0 or game.power(t) <= 0
        kills = att.damage + game.power(t) >= game.power(att) and game.power(t) > 0
        return (pal_value(game, t) if dies else 0.0) - (pal_value(game, att) if kills else 0.0)

    # ------------------------------------------------------------ decisions
    def choose(self, game, d):
        if d.kind == "block":
            return self.block(game, d)
        if d.kind == "may":
            if d.context.get("intent") == "deploy":
                return [len(game.players[d.player].pals) < 5]
            return [True]
        if d.kind == "target":
            return self.target(game, d)
        return list(d.options[: d.min])

    def block(self, game, d):
        me = d.player
        att = game.card(d.context["attacker"])
        tgt_uid = d.context.get("target")
        ap = game.power(att)
        life = game.players[me].life
        # A Quick damage event we can afford adds to what our blocker deals (Ignis Breath).
        ps = game.players[me]
        trick = next((c for c in ps.hand if c.code == "TD01-011"
                      and ps.souls_standing >= game.cost(c)), None)
        extra = effect_damage(game, trick, att, 500) if trick is not None else 0
        best, best_score = None, 0.5
        for uid in d.options:
            b = game.card(uid)
            bp = game.power(b)
            b_dies = b.damage + ap >= bp or bp <= 0
            kills = bp > 0 and att.damage + bp + extra >= ap
            score = (pal_value(game, att) if kills else 0) - (pal_value(game, b) if b_dies else 0)
            if tgt_uid is None:
                s = game.strike(att)
                score += s * LIFE * (1 - LUCKY_RATE)
                if s >= life:
                    score += 100  # otherwise this hit is probably lethal
            else:
                t = game.card(tgt_uid)
                tp = game.power(t)
                if t.damage + ap >= tp or tp <= 0:
                    score += pal_value(game, t)  # we save it
                if tp > 0 and att.damage + tp >= ap:
                    score -= pal_value(game, att)  # it would have killed the attacker anyway
            if score > best_score:
                best, best_score = uid, score
        return [best] if best is not None else []

    def target(self, game, d):
        intent = d.context.get("intent", "")
        amount = d.context.get("amount", 0)
        me = d.player
        cards = [game.card(u) for u in d.options]
        if intent in ("harm", "lock"):
            scored = [(self._harm_score(game, me, c, amount, intent == "lock")
                       + self._attacker_bonus(game, me, c), c.uid) for c in cards]
        elif intent == "help":
            scored = [(self._help_score(game, me, c, d.prompt), c.uid) for c in cards]
        elif intent in ("discard", "sacrifice"):
            scored = [(-self._keep_score(game, c), c.uid) for c in cards]
        elif intent == "top":
            # Stack a Dragon (◇8 or less) only if a Chillet can still be played from hand
            # this turn to deploy it free. Otherwise our next draw phase just draws it,
            # and a lucky card on top is worth more: it cancels the next hit at us.
            hand = game.players[me].hand
            ps = game.players[me]
            chain = (game.active == me and game.phase == "main" and game.battle is None
                     and any(c.code == "BP01-025" and game.cost(c) <= ps.souls_standing
                             for c in hand))
            if chain:
                dragons = [c for c in cards if c.is_pal and c.defn.has_element("dragon")
                           and c.defn.cost <= 8 and not (c.code == "BP01-025" and sum(
                               x.code == "BP01-025" for x in hand) < 2)]
                if dragons:
                    return [max(dragons, key=lambda c: c.defn.cost).uid]
            lucky = [c for c in cards if c.defn.lucky]
            if lucky:
                return [min(lucky, key=lambda c: card_worth(game, c)).uid]
            if d.min == 0:
                return []
            scored = [(-card_worth(game, c), c.uid) for c in cards]
        elif intent == "recover":
            scored = [(card_worth(game, c), c.uid) for c in cards]
        elif intent == "stand":
            scored = [((pal_value(game, c) if c.owner == me else -pal_value(game, c)), c.uid)
                      for c in cards]
        elif intent == "edict":
            # Butcher our worst Pal only if the opponent's worst Pal (their pick) is worth more.
            theirs = [pal_value(game, c) for c in game.players[game.opponent(me)].pals]
            gain = min(theirs) if theirs else 0.0
            scored = [(gain - pal_value(game, c), c.uid) for c in cards]
        else:
            return list(d.options[: d.min])
        scored.sort(key=lambda x: -x[0])
        k = d.max
        picked = [uid for s, uid in scored[:k] if s > 0 or d.min > 0]
        if len(picked) < d.min:
            picked = [uid for _, uid in scored[: d.min]]
        return picked

    @staticmethod
    def _attacker_bonus(game, me, c) -> float:
        """While defending, harm/lock effects should hit the Pal attacking us."""
        b = game.battle
        if b is not None and b.attacker is c and c.owner != me:
            return 50.0
        return 0.0

    def _harm_score(self, game, me, c, amount, lock=False):
        v = pal_value(game, c)
        sign = -1 if c.owner == me else 1
        if amount > 0:  # damage
            hp = game.power(c) - c.damage
            if hp <= 0:
                return 0.01 * sign  # already lethally damaged: more damage is wasted
            v = v if amount >= hp else v * 0.3 * amount / max(hp, 1)
        elif amount == 0 and c.rested and not lock:  # resting something already rested
            v *= 0.1
        return sign * v

    def _help_score(self, game, me, c, prompt):
        if c.owner != me:
            return -pal_value(game, c)
        s = pal_value(game, c) + (2 if not c.rested else 0)
        if prompt.startswith("Rocket Launcher") and "Pengullet" in game.main_names(c):
            s += 20  # unlocks the barrage
        return s

    def _keep_score(self, game, c):
        if c.zone.value == "base":
            return pal_value(game, c)
        return card_worth(game, c)


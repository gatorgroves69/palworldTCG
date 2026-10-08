"""FastBot: a lookahead-free main-phase policy, used for rollouts inside SearchBot.

Everything is decided from the current position with rules of thumb, so a
whole turn costs about a millisecond. Its decisions outside the main phase
(blocks, the Quick step, targets) are RuleBot's. It only has to be a
reasonable opponent inside simulations, not a strong player.
"""
from __future__ import annotations

from engine.actions import Activate, Attack, EndMain, Pass, PlayCard, SoulDraw
from engine.model import CardType

from .evaluate import LIFE, pal_value
from .rules import RuleBot, expected_hit


class FastBot(RuleBot):
    name = "fast"

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        return (self._play(game, player, actions) or self._attack(game, player, actions)
                or self._activate(game, player, actions) or self._leftover(actions))

    # 1. Deploy / cast first, so new Pals can attack and removal clears the way.
    def _play(self, game, p, actions):
        opp_pals = game.players[game.opponent(p)].pals
        best, best_key = None, None
        for a in actions:
            if not isinstance(a, PlayCard):
                continue
            c = game.card(a.uid)
            if c.type is CardType.EVENT:
                key = self._event_priority(game, p, c, a.mode, opp_pals)
                if key <= 0:
                    continue
            else:
                if c.is_pal and len(game.players[p].pals) >= 5:
                    continue
                key = c.defn.cost + (0.5 if c.is_pal else 0)
            if best_key is None or key > best_key:
                best, best_key = a, key
        return best

    @staticmethod
    def _event_priority(game, p, c, mode, opp_pals) -> float:
        """Crude usefulness of an event/mode right now (0 = don't cast)."""
        modes = c.impl.modes(game, c)
        label = modes[mode] if modes and mode is not None else c.defn.text.lower()
        label = label.lower()
        if any(w in label for w in ("destroy", "deal", "graveyard", "return 1 pal")):
            return c.defn.cost + 1 if opp_pals else 0
        if "draw" in label or "top" in label or "look at" in label:
            return 1.0
        if "+1000" in label:
            return 2.0 if len([x for x in game.players[p].pals if not x.rested]) >= 2 else 0
        if "resources" in label or "soul" in label:
            return 0.2
        if "stand" in label or "cannot block" in label:
            return 0.5
        return 0

    # 2. Attack when it wins a fight, trades up, or the path to the player is clear.
    def _attack(self, game, p, actions):
        opp = game.players[game.opponent(p)]
        blockers = [c for c in opp.pals if not c.rested and game.can_block(c)]
        best, best_score = None, 0.0
        for a in actions:
            if not isinstance(a, Attack):
                continue
            att = game.card(a.attacker_uid)
            ap = game.power(att)
            if a.target_uid is None:
                bad_block = any(game.power(b) >= ap - att.damage and game.power(b) > b.damage
                                for b in blockers) and not game.has_kw(att, "stealth")
                s = expected_hit(game, game.opponent(p), game.strike(att))
                if opp.life <= sum(game.strike(x) for x in game.players[p].pals if not x.rested):
                    s += 20  # push for lethal
                elif bad_block:
                    s -= pal_value(game, att)
                score = s
            else:
                t = game.card(a.target_uid)
                tp = game.power(t)
                kills = ap >= tp - t.damage
                dies = t.is_pal and tp >= ap - att.damage and tp > 0
                score = ((pal_value(game, t) if t.is_pal else 4.0) if kills else 0.0) - (
                    pal_value(game, att) if dies else 0.0)
            if score > best_score:
                best, best_score = a, score
        return best

    # 3. Use abilities with what's left (resource engines, digs, revives, buffs).
    def _activate(self, game, p, actions):
        acts = [a for a in actions if isinstance(a, Activate)]
        if not acts:
            return None
        # Prefer the biggest X, and assigning the least valuable standing Pal.
        def key(a):
            pal = game.card(a.assign_uid) if a.assign_uid is not None else None
            return ((a.x or 0), -(pal_value(game, pal) if pal else 0))
        return max(acts, key=key)

    @staticmethod
    def _leftover(actions):
        for a in actions:
            if isinstance(a, SoulDraw):
                return a
        return next((a for a in actions if isinstance(a, EndMain)), actions[0])

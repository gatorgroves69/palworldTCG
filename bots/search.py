"""SearchBot: turn-level lookahead with the opponent's reply.

For each candidate main-phase action it runs `samples` simulations on
determinized copies of the game (the same seeds for every candidate). Each
simulation performs the action, finishes this turn with FastBot, plays the
opponent's whole next turn with FastBot, and scores the position at the start
of our next turn. Blocks, the Quick step and targets use RuleBot's rules.

This is flat Monte Carlo over the first action. Replacing the per-candidate
loop with a tree (MCTS) would reuse the same clone/determinize/rollout pieces.
"""
from __future__ import annotations

import random

from engine.actions import Activate, Attack, EndMain, Pass, PlayCard
from engine.game import GameOver

from .evaluate import evaluate
from .fast import FastBot
from .heuristic import determinize
from .rules import RuleBot


class SearchBot(RuleBot):
    name = "search"

    def __init__(self, seed: int = 0, samples: int = 3, max_candidates: int = 16,
                 reply_turns: int = 1) -> None:
        super().__init__(seed)
        self.samples = samples
        self.max_candidates = max_candidates
        self.reply_turns = reply_turns

    def choose_action(self, game, player, actions):
        if any(isinstance(a, Pass) for a in actions):
            return self.quick_step(game, player, actions)
        cands = self.candidates(game, player, actions)
        if len(cands) == 1:
            return cands[0]
        seeds = [self.rng.random() for _ in range(self.samples)]
        best, best_v = None, None
        for a in cands:
            v = sum(self.rollout(game, player, a, s) for s in seeds) / len(seeds)
            if best_v is None or v > best_v + 1e-9:
                best, best_v = a, v
        return best

    def candidates(self, game, player, actions):
        """Prune near-duplicates: one Activate per (card, ability, X) with the least
        valuable Pal assigned, and at most `max_candidates` in total (ending the turn
        is always kept)."""
        from .evaluate import pal_value
        seen, out = {}, []
        for a in actions:
            if isinstance(a, Activate) and a.assign_uid is not None:
                k = (a.uid, a.index, a.x)
                v = pal_value(game, game.card(a.assign_uid))
                if k in seen and seen[k][0] <= v:
                    continue
                seen[k] = (v, a)
            else:
                out.append(a)
        out += [a for _, a in seen.values()]
        if len(out) > self.max_candidates:
            end = [a for a in out if isinstance(a, EndMain)]
            rest = [a for a in out if not isinstance(a, EndMain)]
            # Keep plays and attacks first; they drive the game.
            rest.sort(key=lambda a: not isinstance(a, (PlayCard, Attack)))
            out = rest[: self.max_candidates - 1] + end
        return out

    def rollout(self, game, me, action, seed) -> float:
        rng = random.Random(seed)
        g = game.clone([FastBot(), FastBot()], rng=rng)
        determinize(g, me, rng)
        try:
            if not isinstance(action, EndMain):
                g.perform(action)
                g.main_phase()
            g.end_phase()
            for _ in range(self.reply_turns):
                g.take_turn()  # the opponent's reply
        except GameOver:
            pass
        return evaluate(g, me, leaf=True)

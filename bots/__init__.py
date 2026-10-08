"""AI players. All implement bots.base.Bot.

In use:
- heuristic2 (TwoStepHeuristicBot): default for runs. Scores each action with its best
  follow-up action this turn.
- heuristic (HeuristicBot): one-action lookahead. The second opinion for every kept swap.
- rules (RuleBot): fast rules of thumb; also answers blocks, targets and Interrupts for
  the bots above.

Experiments, kept for reference and not used for results (see docs/m2-status.md):
- search, plan, fast, lookahead: rollout-based bots that were weaker or no better.
- heuristic-learned: learned evaluation; never plays Structures or Gear.
- random: engine fuzzing only.
"""
from .base import Bot
from .fast import FastBot
from .heuristic import HeuristicBot, LearnedHeuristicBot, LookaheadBot, TwoStepHeuristicBot
from .plan import PlanBot
from .random_bot import RandomBot
from .rules import RuleBot
from .search import SearchBot

BOTS = {
    # in use
    "heuristic2": TwoStepHeuristicBot,
    "heuristic": HeuristicBot,
    "rules": RuleBot,
    # experiments
    "lookahead": LookaheadBot,
    "heuristic-learned": LearnedHeuristicBot,
    "plan": PlanBot,
    "search": SearchBot,
    "fast": FastBot,
    "random": RandomBot,
}

def bot_class(name: str):
    """BOTS[name], or "name@xK": that bot with its defence exchange rate set to K
    (e.g. "heuristic2@x1.5" Interrupts only when the expected loss is 1.5x the cards spent)."""
    if "@x" in name:
        base, k = name.split("@x", 1)
        cls = BOTS[base]
        return type(f"{cls.__name__}_x{k}", (cls,), {"name": name, "defend_cost": float(k)})
    return BOTS[name]


__all__ = ["BOTS", "bot_class", "Bot", "FastBot", "HeuristicBot", "LearnedHeuristicBot", "LookaheadBot",
           "PlanBot", "RandomBot", "RuleBot", "SearchBot", "TwoStepHeuristicBot"]

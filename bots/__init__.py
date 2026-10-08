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
    """BOTS[name], optionally with defence variants after "@":
    "@xK"    Interrupt only when the expected loss is K times the cards spent (default 1).
    "@exact" value hits as Strike*(1-p)^Strike with the deck's real lucky odds (default: the
             legacy linear estimate, which is what the M1 calibration passed with).
    e.g. "heuristic2@exact@x0.8"."""
    base, *opts = name.split("@")
    cls = BOTS[base]
    if not opts:
        return cls
    attrs = {"name": name}
    for o in opts:
        if o == "exact":
            attrs["exact_odds"] = True
        elif o.startswith("x"):
            attrs["defend_cost"] = float(o[1:])
        else:
            raise KeyError(f"unknown bot option {o!r} in {name!r}")
    return type(f"{cls.__name__}_{'_'.join(opts)}", (cls,), attrs)


__all__ = ["BOTS", "bot_class", "Bot", "FastBot", "HeuristicBot", "LearnedHeuristicBot", "LookaheadBot",
           "PlanBot", "RandomBot", "RuleBot", "SearchBot", "TwoStepHeuristicBot"]

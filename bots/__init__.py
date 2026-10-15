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
from .heuristic import (HeuristicBot, LearnedHeuristicBot, LookaheadBot, ThreeStepHeuristicBot,
                        TwoStepHeuristicBot)
from .plan import PlanBot
from .random_bot import RandomBot
from .rules import RuleBot
from .search import SearchBot

BOTS = {
    # in use
    "heuristic2": TwoStepHeuristicBot,
    "heuristic3": ThreeStepHeuristicBot,
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
    "@cautious" rested Pals keep 40/60% of their value instead of 70/90%: attacks less,
             holds blockers (an experiment on why engine decks lose too much).
    "@exact" value hits as Strike*(1-p)^Strike with the deck's real lucky odds (default: the
             legacy linear estimate, which is what the M1 calibration passed with).
    "@human" defend like Palify's top-50 players: hoard Interrupts at high life, protect
             Pals more, block less (2026-10-13 calibration).
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
        elif o == "bold":  # rested Pals keep 85/95% of their value: attacks more (Palify:
            attrs["exposure_default"] = (0.85, 0.95)  # real Stone Pit deals 5.0/game, bot 2.9)
        elif o == "seq":  # assign engine structures before attacking (Palify calibration)
            attrs["engine_first"] = True
        elif o.startswith("struct"):  # opponent/own structures worth K times more (kill the engine)
            attrs["struct_scale"] = float(o[6:] or 2.0)
        elif o.startswith("engine"):  # Material/Ingredient worth K times more (experiment)
            attrs["resource_scale"] = float(o[6:] or 2.0)
        elif o == "human":  # Palify top-50 defence profile, see RuleBot
            attrs.update(life_scaled=True, pal_protect=1.8, block_threshold=3.0,
                         open_soul_by_life=True, death_value=True, soul_draw_eager=True,
                         structure_defence=True)
        elif o == "cautious":  # a rested Pal keeps less value: hold blockers back more
            attrs["exposure_default"] = (0.4, 0.6)
        else:
            raise KeyError(f"unknown bot option {o!r} in {name!r}")
    return type(f"{cls.__name__}_{'_'.join(opts)}", (cls,), attrs)


__all__ = ["BOTS", "bot_class", "Bot", "FastBot", "HeuristicBot", "LearnedHeuristicBot", "LookaheadBot",
           "PlanBot", "RandomBot", "RuleBot", "SearchBot", "ThreeStepHeuristicBot",
           "TwoStepHeuristicBot"]

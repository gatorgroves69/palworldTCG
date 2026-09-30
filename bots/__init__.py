"""AI players. All implement bots.base.Bot."""
from .base import Bot
from .fast import FastBot
from .heuristic import HeuristicBot, LearnedHeuristicBot, TwoStepHeuristicBot
from .plan import PlanBot
from .random_bot import RandomBot
from .rules import RuleBot
from .search import SearchBot

BOTS = {"heuristic2": TwoStepHeuristicBot, "heuristic-learned": LearnedHeuristicBot, "plan": PlanBot, "search": SearchBot, "heuristic": HeuristicBot, "fast": FastBot, "rules": RuleBot,
        "random": RandomBot}

__all__ = ["BOTS", "Bot", "FastBot", "HeuristicBot", "LearnedHeuristicBot", "TwoStepHeuristicBot", "PlanBot", "RandomBot", "RuleBot", "SearchBot"]

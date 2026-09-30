"""AI players. All implement bots.base.Bot."""
from .base import Bot
from .heuristic import HeuristicBot
from .random_bot import RandomBot
from .rules import RuleBot

BOTS = {"heuristic": HeuristicBot, "rules": RuleBot, "random": RandomBot}

__all__ = ["BOTS", "Bot", "HeuristicBot", "RandomBot", "RuleBot"]

"""Small helpers shared by card implementations."""
from __future__ import annotations

from typing import Callable

from engine.game import Game
from engine.state import CardInstance, Zone


def all_pals(game: Game) -> list[CardInstance]:
    """Every Pal in both bases, turn player's first."""
    order = (game.active, game.opponent(game.active))
    return [c for p in order for c in game.players[p].pals]


def opp_pals(game: Game, player: int) -> list[CardInstance]:
    return list(game.players[game.opponent(player)].pals)


def choose_pal(game: Game, player: int, prompt: str,
               pred: Callable[[CardInstance], bool] = lambda c: True,
               up_to: bool = True, intent: str = "", amount: int = 0) -> CardInstance | None:
    """"Choose (up to) 1 Pal" among Pals in either base that satisfy `pred`."""
    picked = game.choose_cards(player, prompt, [c for c in all_pals(game) if pred(c)],
                               n=1, up_to=up_to, intent=intent, amount=amount)
    return picked[0] if picked else None


def rest_card(game: Game, c: CardInstance) -> None:
    if c.rested:
        game.log(f"  {c.name} is chosen (already rested)")
    else:
        game.rest(c)
        game.log(f"  {c.name} is rested")


def is_dragon_pal(c: CardInstance) -> bool:
    return c.is_pal and c.defn.has_element("dragon")


def put_on_top(game: Game, c: CardInstance) -> None:
    game.move(c, Zone.DECK, top=True)
    game.log(f"  {game.pname(c.owner)} puts {c.name} from hand on top of the deck")

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
    c.known_top = True
    game.log(f"  {game.pname(c.owner)} puts {c.name} from hand on top of the deck")


def look_top(game: Game, p: int, n: int) -> list[CardInstance]:
    """"Look at the top n cards of your deck" (they stay in the deck until moved)."""
    cards = game.players[p].deck[:n]
    game.log(f"  {game.pname(p)} looks at the top {len(cards)}: "
             + ", ".join(c.name for c in cards))
    return cards


def shuffle_deck(game: Game, p: int) -> None:
    game.rng.shuffle(game.players[p].deck)
    for c in game.players[p].deck:
        c.known_top = False
    game.log(f"  {game.pname(p)} shuffles the deck")


def my_structures(game: Game, p: int) -> list[CardInstance]:
    return list(game.players[p].structures)


def my_gears(game: Game, p: int) -> list[CardInstance]:
    return [c for c in game.players[p].base if c.type.value == "gear"]


def plus_power(amount: int):
    """ACT effect: "Choose 1 Pal, and it gets Power +N until end of turn"."""
    def effect(game: Game, card: CardInstance, ctx: dict) -> None:
        t = choose_pal(game, card.owner, f"{card.name}: +{amount} power to 1 Pal", up_to=False,
                       intent="help", amount=amount)
        if t:
            game.add_mod(t, "power", amount, "turn", card.name)
    return effect


def has_resources(kind: str, n: int):
    return lambda game, card: game.players[card.owner].resources[kind] >= n


def consume_cost(kind: str, n: int | None = None):
    """pay_extra for [Consume N kind] (N=None: consume the chosen X)."""
    def pay(game: Game, card: CardInstance, ctx: dict) -> None:
        if not game.consume(card.owner, kind, n if n is not None else ctx["x"]):
            raise ValueError(f"{card.name}: not enough {kind}")
    return pay


def mill_cost(n: int):
    """[Put the top n cards of the deck into the graveyard]."""
    def can(game: Game, card: CardInstance) -> bool:
        return len(game.players[card.owner].deck) >= n

    def pay(game: Game, card: CardInstance, ctx: dict) -> None:
        game.mill(card.owner, n)
    return can, pay


def discard_cost(n: int):
    """[Discard n cards from hand] (the chosen card for a self-discard is excluded)."""
    def can(game: Game, card: CardInstance) -> bool:
        return len([c for c in game.players[card.owner].hand if c is not card]) >= n

    def pay(game: Game, card: CardInstance, ctx: dict) -> None:
        hand = [c for c in game.players[card.owner].hand if c is not card]
        for c in game.choose_cards(card.owner, f"{card.name}: discard {n}", hand, n,
                                   intent="discard"):
            game.log(f"  {game.pname(card.owner)} discards {c.name}")
            game.discard(c)
    return can, pay


def graveyard_cards(game: Game, p: int, pred=lambda c: True) -> list[CardInstance]:
    return [c for c in game.players[p].graveyard if pred(c)]

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
2 compañías compiten en el mercado poniendo precios por bienes homogenuos.

Ver "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    players_per_group = 2
    name_in_url = 'bertrand'
    num_rounds = 1

    instructions_template = 'bertrand/Instructions.html'
    header_template='global/header.html'
    footer_template='global/footer.html'

    maximum_price = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == winning_price]
        winner = random.choice(winners)
        for p in players:
            p.payoff = c(0)
            if p == winner:
                p.is_a_winner = True
                p.payoff += p.price


class Player(BasePlayer):
    price = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Precio el jugador elige vender el producto"""
    )

    is_a_winner = models.BooleanField(
        initial=False,
        doc="""Si el jugador ofreció el precio mas bajo"""
    )

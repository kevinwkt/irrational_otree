from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
El "bargaining game" involucra 2 jugadores. Cada uno demanda una porción de un monto disponible.
Si la suma de las demandas es menor que el monto disponible, ambos jugadores obtienen la porción demandada.
En caso contrario, los dos jugadores obtienen nada.
"""


class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'bargaining/Instructions.html'
    header_template='global/header.html'
    footer_template='global/footer.html'

    amount_shared = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        total_requested_amount = sum([p.request_amount for p in players])
        if total_requested_amount <= Constants.amount_shared:
            for p in players:
                p.payoff = p.request_amount
        else:
            for p in players:
                p.payoff = c(0)


class Player(BasePlayer):
    request_amount = models.CurrencyField(
        doc="""
        Monto pedido por este jugador.
        """,
        min=0, max=Constants.amount_shared
    )

    def other_player(self):
        """Regresa el oponente del jugador actual"""
        return self.get_others_in_group()[0]

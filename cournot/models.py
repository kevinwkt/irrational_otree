from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
En "Cournot", las empresas deciden simultáneamente las unidades de productos para
fabricar. El precio de venta unitario depende del total de unidades producidas. En
esta implementación, hay 2 empresas que compiten por 1 período.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'cournot/Instructions.html'
    header_template='global/header.html'
    footer_template='global/footer.html'

    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    price = models.CurrencyField(
        doc="""Precio por unidad: P = T - \sum U_i, donde T es la capacidad total y U_i es la cantidad de unidades producidas por jugador i"""
    )

    total_units = models.PositiveIntegerField(
        doc="""Unidades totales producidas por los jugadores"""
    )

    def set_payoffs(self):
        self.total_units = sum([p.units for p in self.get_players()])
        self.price = Constants.total_capacity - self.total_units
        for p in self.get_players():
            p.payoff = self.price * p.units


class Player(BasePlayer):

    units = models.PositiveIntegerField(
        min=0, max=Constants.max_units_per_player,
        doc="""Cantidades de unidades a producir"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]

from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def vars_for_template(self):
        return {'prog': 25}
    currentProgress=0
    """Description of the game: How to play and returns expected"""
    pass


class Contribute(Page):
     def vars_for_template(self):
        return {'prog': 50}
    currentProgress=50
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}


class MyWaitPage(WaitPage):
    def vars_for_template(self):
       return {'prog': 75}
    template_name = 'global/MyWaitPage.html'
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Esperando a que los otros participantes contribuyan."


class Results(Page):
    def vars_for_template(self):
       return {'prog': 100}
    currentProgress=100
    """Payoff de los Jugadores: Ganancia de cada Jugador"""

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
        }


page_sequence = [
    Introduction,
    Contribute,
    MyWaitPage,
    Results
]

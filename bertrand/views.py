from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Decide(Page):
    form_model = models.Player
    form_fields = ['price']


class MyWaitPage(WaitPage):
    template_name = 'global/MyWaitPage.html'
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Esperando a que los otros participantes contribuyan."


class Results(Page):
    def vars_for_template(self):
        return {
            'table': [
                ('Tu precio', self.player.price),
                ('Precio mas bajo', min(
                    p.price for p in self.group.get_players())),
                ('Tu producto fue vendido?',
                 'Si' if self.player.is_a_winner else 'No'),
                ('Tus ganancias', self.player.payoff),
            ]
        }


page_sequence = [Introduction,
                 Decide,
                 MyWaitPage,
                 Results]

from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Decide(Page):
    form_model = models.Player
    form_fields = ['decision']


class MyWaitPage(WaitPage):
    template_name = 'global/MyWaitPage.html'
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Esperando a que los otros participantes contribuyan."


class Results(Page):
    pass


page_sequence = [Introduction,
                 Decide,
                 MyWaitPage,
                 Results]

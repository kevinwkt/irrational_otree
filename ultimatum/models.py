from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
El juego "Ultimatum" con 2 características: Respuesta directa y método estratégico.
En la respuesta directa, un jugador hace una propuesta y el segundo acepta o rechaza.
Viene en 2 maneras, con y sin preguntas hipotéticas sobre la respuesta del segundo jugador a ofertas distintas a la que se hace.
En el método estratégico, el segundo jugador recibe una lista de todas las ofertas posibles y se le pregunta cuáles aceptar o rechazar.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'ultimatum/Instructions.html'
    header_template='global/header.html'
    footer_template='global/footer.html'

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(10)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)

    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                g.use_strategy_method = self.session.config['use_strategy_method']
            else:
                g.use_strategy_method = random.choice([True, False])


def question(amount):
    return 'Aceptarías una propuesta de {}?'.format(c(amount))


class Group(BaseGroup):
    use_strategy_method = models.BooleanField(
        doc="""Si el grupo utiliza el método estrategia"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField(
        doc="Si la oferta es aceptada (direct response method)"
    )

    # for strategy method
    response_0 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(0))
    response_10 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(10))
    response_20 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(20))
    response_30 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(30))
    response_40 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(40))
    response_50 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(50))
    response_60 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(60))
    response_70 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(70))
    response_80 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(80))
    response_90 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(90))
    response_100 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal, verbose_name=question(100))


    def set_payoffs(self):
        p1, p2 = self.get_players()

        if self.use_strategy_method:
            self.offer_accepted = getattr(self, 'response_{}'.format(
                int(self.amount_offered)))

        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    pass

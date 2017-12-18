from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class Contribute(Page):
    """Player: Choose how much to contribute"""
    form_model = models.Player
    form_fields = ['contribution']

class ObserveWaitPage(WaitPage):
    body_text = "Waiting for other participants to contribute."

class Observe(Page):
    form_model = models.Player
    form_fields = ['eval_p1', 'eval_p2', 'eval_p3']

    def vars_for_template(self):
        return {
            'p1_contrib':self.group.get_player_by_id(1).contribution,
            'p2_contrib':self.group.get_player_by_id(2).contribution,
            'p3_contrib':self.group.get_player_by_id(3).contribution,
            'total_contrib':self.group.total_contribution,
        }

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
    body_text = "Waiting for other participants to evaluate."


class Results(Page):
    """Players payoff: How much each has earned"""
    def vars_for_template(self):
        return {
            'p1_contrib':self.group.get_player_by_id(1).contribution,
            'p2_contrib':self.group.get_player_by_id(2).contribution,
            'p3_contrib':self.group.get_player_by_id(3).contribution,
            'total_contrib':self.group.total_contribution,
            'p1_score':self.group.get_player_by_id(1).individual_score,
            'p2_score':self.group.get_player_by_id(2).individual_score,
            'p3_score':self.group.get_player_by_id(3).individual_score,
            'median_score':statistics.median(self.group.get_player_by_id(1).individual_score, self.group.get_player_by_id(2).individual_score, self.group.get_player_by_id(3).individual_score,),
            'p1_remainder_tokens':None,
            'group_grade':self.group.get_player_by_id(1).group_grade,
            'p1_individual_grade':self.group.get_player_by_id(1).individual_grade,
            'p1_final_grade':self.group.get_player_by_id(1).final_grade,
        }

page_sequence = [
    Introduction,
    Contribute,
    ObserveWaitPage,
    Observe,
    ResultsWaitPage,
    Results
]

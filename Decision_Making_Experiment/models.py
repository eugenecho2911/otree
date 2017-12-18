from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from statistics import median

author = 'Eugene Cho'

doc = """
This is an experiment in decision making.
"""


class Constants(BaseConstants):
    name_in_url = 'Decision_Making_Experiment'
    players_per_group = 3
    num_rounds = 30

    instructions_template ='Decision_Making_Experiment/Instructions.html'
    endowment = c(12)
    multiplier = 13


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.FloatField()
    individual_score = models.FloatField()
    individual_grade = models.FloatField()
    group_grade = models.FloatField()

    def set_payoffs(self):
        self.contribution = [p.contribution for p in self.get_players()]
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        for p in self.get_players():
            p.individual_score = statistics.median(get.player_by_id(1).form.eval_p1, get.player_by_id(2).form.eval_p1, get.player_by_id(3).form.eval_p1)
            p.individual_grade = Constants.multiplier * (3 * get.player_by_id(1).individual_score) - 0.5 * (3 * get.player_by_id(1).individual_score)^2
            p.group_grade = Constants.multiplier * (self.total_contribution) - 0.5 * (self.total_contribution)^2
            p.final_grade =  0.25 * (p.group_grade) + 0.75 * (p.individual_grade)


class Player(BasePlayer):
    endowment = models.FloatField(
        min=0, max=Constants.endowment,
        doc="""Number of tokens this player receives"""
    )
    contribution = models.FloatField(
        min=0, max=Constants.endowment,
        doc="""Number of tokens this player contributes""",
        widget=widgets.SliderInput(attrs={'step':'0.1'})
    )
    eval_p1 =  models.FloatField(
        min=0, max=Constants.endowment,
        doc="""This player's evaluation of player 1""",
        widget=widgets.SliderInput(attrs={'step':'0.1'})
    )
    eval_p2 =  models.FloatField(
        min=0, max=Constants.endowment,
        doc="""This player's evaluation of player 2""",
        widget=widgets.SliderInput(attrs={'step':'0.1'})
    )
    eval_p3 =  models.FloatField(
        min=0, max=Constants.endowment,
        doc="""This player's evaluation of player 3""",
        widget=widgets.SliderInput(attrs={'step':'0.1'})
    )
    score_median = models.FloatField(
        doc="""The median of score_p1, score_p2, and score_p3""",
        min=0, max=Constants.endowment,
    )
    group_grade = models.FloatField(
        doc="""This is the group grade that contributes to all player's final grade.""",
    )
    p1_individual_grade = models.FloatField(
        doc="""This player's individual grade.""",
    )
    p1_final_grade = models.FloatField(
        doc="""This player

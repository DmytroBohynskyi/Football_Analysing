import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib

# New Antecedent/Consequent objects hold universe variables and membership
# functions
from gui.db_conect import DataBase


class Fuzzy:
    def __init__(self, first_club="Arka Gdynia", second_club="Lechia Gdansk"):
        self.first_club = first_club
        self.second_club = second_club

        self.create_antecedent()
        self.start_automf()
        self.start_trimf()
        self.fuzzy_rules()

    def create_antecedent(self) -> None:
        """
        New Antecedent/Consequent objects hold universe variables and membership
        functions
        :return: None
        """
        #
        self.advancement_first_team = ctrl.Antecedent(np.arange(0, 3, .01), 'advancement_first_team')
        self.advancement_second_team = ctrl.Antecedent(np.arange(0, 3, .01), 'advancement_second_team')

        # the results of the game in the last season
        self.lost_first_team = ctrl.Antecedent(np.arange(0, 100, 1), 'lost_first_team')
        self.lost_second_team = ctrl.Antecedent(np.arange(0, 100, 1), 'lost_second_team')

        # remiss in matches among themselves
        self.goals_statistics = ctrl.Antecedent(np.arange(0, 4, 1), 'goals_statistics')

        self.remiss = ctrl.Consequent(np.arange(0, 100, 1), 'remiss')

    def start_trimf(self):
        # -----------------------------------------------------------------------------
        self.goals_statistics['poor'] = fuzz.trimf(self.goals_statistics.universe, [1.5, 3, 3])
        self.goals_statistics['average'] = fuzz.trimf(self.goals_statistics.universe, [0.5, 1, 3])
        self.goals_statistics['good'] = fuzz.trimf(self.goals_statistics.universe, [0, 0, 2])
        # self.lost_second_team.view()
        # ------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------
        self.advancement_first_team['poor'] = fuzz.trimf(self.advancement_first_team.universe, [0, 0, 1])
        self.advancement_first_team['average'] = fuzz.trimf(self.advancement_first_team.universe, [.8, 1.2, 1.8])
        self.advancement_first_team['good'] = fuzz.trimf(self.advancement_first_team.universe, [1.2, 3, 3])
        # self.lost_second_team.view()
        # ------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------
        self.advancement_second_team['poor'] = fuzz.trimf(self.advancement_second_team.universe, [0, 0, 0.9])
        self.advancement_second_team['average'] = fuzz.trimf(self.advancement_second_team.universe, [.6, 1.2, 1.6])
        self.advancement_second_team['good'] = fuzz.trimf(self.advancement_second_team.universe, [1.2, 3, 3])
        # self.lost_second_team.view()
        # ------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------
        self.lost_first_team['poor'] = fuzz.trimf(self.lost_first_team.universe, [0, 0, 30])
        self.lost_first_team['average'] = fuzz.trimf(self.lost_first_team.universe, [15, 45, 60])
        self.lost_first_team['good'] = fuzz.trimf(self.lost_first_team.universe, [30, 100, 100])
        # self.lost_second_team.view()
        # ------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------
        self.lost_second_team['poor'] = fuzz.trimf(self.lost_second_team.universe, [0, 0, 30])
        self.lost_second_team['average'] = fuzz.trimf(self.lost_second_team.universe, [15, 45, 60])
        self.lost_second_team['good'] = fuzz.trimf(self.lost_second_team.universe, [30, 100, 100])
        # self.lost_second_team.view()
        # ------------------------------------------------------------------------------

    def start_automf(self):
        self.advancement_first_team.automf(3)
        self.advancement_second_team.automf(3)

        self.lost_first_team.automf(3)
        self.lost_second_team.automf(3)

        self.goals_statistics.view()
        self.remiss.automf(3)

    # describes the relationship between
    def fuzzy_rules(self):
        rules = [
            ctrl.Rule(self.advancement_first_team['good'] | self.advancement_second_team['good'], self.remiss['good']),
            ctrl.Rule(self.advancement_first_team['poor'] | self.advancement_second_team['good'], self.remiss['poor']),
            ctrl.Rule(self.advancement_first_team['good'] | self.advancement_second_team['poor'], self.remiss['poor']),
            ctrl.Rule(self.advancement_first_team['average'] | self.advancement_second_team['average'] |
                      self.goals_statistics['good'], self.remiss['good']),
            ctrl.Rule(self.advancement_first_team['average'] | self.advancement_second_team['average'] |
                      self.goals_statistics['poor'], self.remiss['poor']),

            ctrl.Rule(self.advancement_first_team['good'] | self.lost_second_team['average'] |
                      self.advancement_second_team['average'], self.remiss['good']),
            ctrl.Rule(self.advancement_first_team['average'] | self.lost_first_team['average'] |
                      self.advancement_second_team['good'], self.remiss['good']),

        ]

        self.tipping_ctrl = ctrl.ControlSystem(rules)

        self.tipping = ctrl.ControlSystemSimulation(self.tipping_ctrl)

    def start_symulation(self, db, **kwargs):
        db = DataBase()

        # Remiss for the previous 5 years as a percentage [%]
        self.advancement_first_team = ctrl.Antecedent(np.arange(0, 100, 1), 'advancement_first_team')
        self.advancement_second_team = ctrl.Antecedent(np.arange(0, 100, 1), 'advancement_second_team')

        # the results of the game in the last season
        self.lost_first_team = ctrl.Antecedent(np.arange(0, 100, 1), 'results_first_team')
        self.lost_second_team = ctrl.Antecedent(np.arange(0, 100, 1), 'results_second_team')

        # remiss in matches among themselves
        self.goals_statistics = ctrl.Antecedent(np.arange(0, 4, 1), 'goals_statistics')

        # check statistic for 5 years
        statistic = db.get_statistic(league=kwargs.get("league"))
        first_static = statistic.get(self.first_club)
        second_static = statistic.get(self.second_club)

        self.tipping.input['advancement_first_team'] = first_static["result"] / (
                first_static["won"] + first_static["drawn"] + first_static["lost"])
        self.tipping.input['advancement_second_team'] = second_static["result"] / (
                second_static["won"] + second_static["drawn"] + second_static["lost"])

        # check statistic for 2 years
        self.tipping.input['lost_first_team'] = (db.get_remiss(self.first_club, year=5) * 100) / \
                                                db.get_match_numbers(self.first_club)
        self.tipping.input['lost_second_team'] = (db.get_remiss(self.second_club, year=5) * 100) / \
                                                 db.get_match_numbers(self.second_club)

        self.tipping.input['goals_statistics'] = db.get_goals_statistics(self.first_club, self.second_club)

        self.tipping.compute()
        var = self.tipping.output['remiss']
        self.remiss.view(sim=self.tipping)
        return str(int(var))


if __name__ == '__main__':
    db = DataBase()
    fuzzy = Fuzzy()
    fuzzy.start_symulation(db)

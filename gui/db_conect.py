import os

import psycopg2


class DataBase:
    COUNTRIES = {"poland": 1, "england": 1}

    def __init__(self):
        self.__database: str = os.getenv("DB_database")
        self.__user: str = os.getenv("DB_user")
        self.__password: str = os.getenv("DB_password")

        # Establishing the connection
        self.conn = psycopg2.connect(database=self.__database, user=self.__user,
                                     password=self.__password, host='localhost', port='5432')
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor()

    def get_match_numbers(self, name: str, year=5):
        oll_match = f"""select count(r.id) from result r left join matches m on m.result_id = r.id 
                                where m.second_club = (select id from clubs where name = '{name}')
                                or m.first_club = (select id from clubs where name = '{name}')
                                AND match_day >= (now() - '{year} year'::interval)"""
        self.cursor.execute(oll_match)
        count_matches: int = self.cursor.fetchall()[0][0]
        return count_matches

    def get_remiss(self, club_name: str, year=5):
        """
        This function checks data base and looks for errors
        :param club_name:
        :return:
        """
        # sql request only remiss
        sql_request = f""" select * from result r left join matches m on m.result_id = r.id 
                            where r.first_club = r.second_club and  
                            m.first_club = (select id from clubs where name = '{club_name}')
                            AND match_day >= (now() - '{year} year'::interval)"""
        # all result
        sql_request_1 = f"""select * from result r left join matches m on m.result_id = r.id 
                            where r.first_club = r.second_club and  
                            m.second_club = (select id from clubs where name = '{club_name}')
                            AND match_day >= (now() - '{year} year'::interval)"""

        self.cursor.execute(sql_request)
        fetch = self.cursor.fetchall()
        count_remiss: int = fetch[0][0] if fetch else 0

        self.cursor.execute(sql_request_1)
        fetch = self.cursor.fetchall()
        count_other_matches: int = fetch[0][0] if fetch else 0

        return count_remiss + count_other_matches

    def get_win(self, name: str, year=5):
        """
        This function checks data base and looks for errors
        :param name:
        :return:
        """
        # sql request only remiss
        sql_request = f""" select count(r.id) from result r left join matches m on m.result_id = r.id 
                            where r.first_club > r.second_club and  
                            m.first_club = (select id from clubs where name = '{name}')
                            AND match_day >= (now() - '{year} year'::interval)"""
        # all result
        sql_request_1 = f"""select count(r.id) from result r left join matches m on m.result_id = r.id 
                            where r.first_club > r.second_club and  
                            m.second_club = (select id from clubs where name = '{name}')
                            AND match_day >= (now() - '{year} year'::interval)"""

        self.cursor.execute(sql_request)
        count_win_1: int = self.cursor.fetchall()[0][0]

        self.cursor.execute(sql_request_1)
        count_win_2: int = self.cursor.fetchall()[0][0]

        return count_win_1 + count_win_2

    def get_goals_statistics(self, name_1: str, name_2: str):
        sql_request = f"""select sum(r.first_club), sum(r.second_club), count(r.id) from result r
                                                left join matches m on m.result_id = r.id
                                                where r.first_club = r.second_club
                                                and m.first_club = (select id from clubs where name = '{name_2}')
                                                or m.second_club = (select id from clubs where name = '{name_1}')
                                                or m.second_club = (select id from clubs where name = '{name_2}')
                                                or m.first_club = (select id from clubs where name = '{name_1}') and
                                                match_day >= (now() - '1 month'::interval);"""

        self.cursor.execute(sql_request)
        count_other_matches: list = self.cursor.fetchall()[0]

        return (count_other_matches[0] + count_other_matches[1]) / count_other_matches[2]

    def get_data_about_previously_match(self, name):
        sql_request = f"""select count(title) from result r left join matches m on m.result_id = r.id
                                    and m.second_club = (select id from clubs where name = '{name}')
                                    or m.first_club = (select id from clubs where name = '{name}')
                                    and match_day > (now() - '1 year'::interval);"""

        self.cursor.execute(sql_request)
        count_other_matches: int = self.cursor.fetchall()[0][0]

        return count_other_matches

    def get_statistic(self, league, seasons='2020/2021') -> dict:
        matches_list = self.get_matches(seasons, league)
        clubs_dict = {name: {"won": 0, "drawn": 0, "lost": 0, "result": 0} for name in self.get_clubs(league, seasons)}

        for match in matches_list:
            if match[1] == match[2]:
                clubs_dict[match[0].rstrip()]["drawn"] += 1
                clubs_dict[match[3].rstrip()]["drawn"] += 1
            if match[1] > match[2]:
                clubs_dict[match[0].rstrip()]["won"] += 1
                clubs_dict[match[3].rstrip()]["lost"] += 1
            if match[1] < match[2]:
                clubs_dict[match[0].rstrip()]["lost"] += 1
                clubs_dict[match[3].rstrip()]["won"] += 1

        for name in clubs_dict:
            clubs_dict[name]["result"] = clubs_dict[name]["won"] * 3 + clubs_dict[name]["drawn"]
        return clubs_dict

    def get_league(self, country):
        sql_request = f"select label from league " \
                      f"where league.country = (select id from countries where countries.label = '{country}')"
        self.cursor.execute(sql_request)
        data: list = [n[0].rstrip() for n in self.cursor.fetchall()]
        return data

    def get_season(self, league):
        sql_request = f"select s.label from seasons s left join matches m on s.id = m.seasons_id " \
                      f"where m.league_id = (select id from league l where l.label = '{league}' ) " \
                      f"GROUP BY s.label order by s.label"
        self.cursor.execute(sql_request)
        data: list = [n[0].rstrip() for n in self.cursor.fetchall()]
        return data

    def get_clubs(self, league, seasons='2020/2021'):
        sql_request = """ select name from matches m
                         left join league l on l.id = m.league_id
                        left JOIN clubs c on m.first_club = c.id or m.second_club = c.id
                        where m.league_id = (select league.id from league where league.label = '{0}')
                        AND m.seasons_id = (select id from seasons where seasons.label = '{1}')
                        group by name;""".format(league, seasons)
        self.cursor.execute(sql_request)
        data: list = [n[0].rstrip() for n in self.cursor.fetchall()]
        return data

    def get_matches(self, seasons, league):
        sql_request = """ select first_club, first_club_result , second_club_result, c.name second_club, match_day
                                from LATERAL (select c.name        first_club,
                                                     r.first_club  first_club_result,
                                                     r.second_club second_club_result,
                                                     m.second_club second_club,
                                                     m.match_day   match_day
                                              from matches m
                                                       inner join clubs c on c.id = m.first_club
                                                       inner join result r on m.result_id = r.id
                                              where m.seasons_id = (select s.id from seasons s where s.label = '{0}')
                                                and m.league_id = (select l.id from league l where l.label = '{1}')) r
                                inner join clubs c on c.id = r.second_club""".format(seasons, league)
        self.cursor.execute(sql_request)
        data: list = self.cursor.fetchall()
        return data

    def exit(self):
        self.conn.close()
        self.cursor.close()

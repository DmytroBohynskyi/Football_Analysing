import os
import re
from datetime import datetime

import psycopg2
from soccer.items import SoccerItem


class SoccerPipeline:

    def open_spider(self, spider) -> None:
        """
        Connect with database.
        :param spider:
        :return:
        """
        self.__database: str = os.getenv("DB_database")
        self.__user: str = os.getenv("DB_user")
        self.__password: str = os.getenv("DB_password")

        # Establishing the connection
        self.conn = psycopg2.connect(database=self.__database, user=self.__user,
                                     password=self.__password, host='localhost', port='5432')
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor()

        self.cookies = {
            "countries": {
                "poland": 1,
                "england": 2
            },
            "league": {},
            "clubs": {},
            "seasons": {},
            "result": {},
        }

    def process_item(self, item, spider) -> SoccerItem:
        """
        This function gets data from item and writes they to the database tables
        :param item: Object of SoccerItem class.
        :param spider:
        :return: None
        """
        country_id: int = self.cookies['countries'].get(item["country"])
        season_id: int = self.insert_new_row(item["season"], table_name="seasons", column_name="label")
        league_id: int = self.insert_new_row(item["league"], table_name="league", column_name="label",
                                             key=[f", '{item['url']}'", f", {country_id}", ],
                                             key_name=[", href, country", ])
        first_club_id: int = self.insert_new_row(item["first_club_name"], table_name="clubs", column_name="name")
        second_club_id: int = self.insert_new_row(item["second_club_name"], table_name="clubs", column_name="name")
        result_id: int = self.insert_result(item["result"], table_name="result")
        date = self.string_to_date(item["date"])

        self.insert_matches(first_club_id, second_club_id, league_id, season_id, result_id, date, )

        return item

    def close_spider(self, spider) -> None:
        """
        Closes connection with database.
        :param spider:
        :return: None
        """
        self.conn.close()
        self.cursor.close()


    def insert_new_row(self, value, table_name, column_name=None, key: list = None, key_name: list = None,
                       sql_query=None) -> int:
        """
        This function creates SQL Query and sends it to data base.
        :param value: Value of the table
        :param table_name: Name of the table in which the data is written
        :param column_name: Name of the column in which the data is written
        :param key: Additional data
        :param key_name: Name of the Additional data
        :param sql_query:   SQL Query that will be sent to the database,
                            if it is None then it will be created automatically
        :return: [int] Row id.
        """
        if None in [key_name, key]:
            [key_name, key] = ["", ""]

        id_of_row: int  # row id
        try:
            id_of_row = self.cookies[table_name][value]  # if data is in cookies
        except KeyError:
            if not sql_query:
                sql_query: str = f"INSERT INTO {table_name} ({column_name}{''.join(key_name)}) " \
                                 f"VALUES ('{str(value)}'{''.join(key)}) " \
                                 f"ON CONFLICT ({column_name}) DO UPDATE SET {column_name}=EXCLUDED.{column_name} " \
                                 f"RETURNING id;"

            id_of_row = self.insert(sql_query, table_name=table_name, value=value)
        finally:
            return id_of_row


    def insert_result(self, value: str, table_name, ) -> int:
        """
        This function creates SQL Query from value["result"] and sends it to data base.
        :param value: Value of the table
        :param table_name: Name of the table in which the data is written
        :return: [int] Row id
        """
        # spit result from " {value} ,{value}" on two value
        # or if value is "avard" then write "avard"
        p = re.compile(r'\d+')
        try:
            first_value, second_value = p.findall(value)
        except ValueError:
            first_value, second_value = [-1, -1]
        # Create query
        sql_query: str = r"INSERT INTO result (first_club, second_club, title) " \
                         f"VALUES ({first_value},{second_value},'{value}') " \
                         f"ON CONFLICT (title) " \
                         f"DO UPDATE SET first_club=EXCLUDED.first_club, second_club=EXCLUDED.second_club, title=EXCLUDED.title " \
                         f"RETURNING id;"
        return self.insert_new_row(str(value), table_name, sql_query=sql_query)


    def insert_matches(self, *args) -> None:
        """
        Crates SQL Query from data in args and next send to database
        :param args:[first_club_id: int, second_club_id: int, league_id: int, season_id: int, result_id: int, date: str]
        :return: None
        """

        sql_query: str = r"INSERT INTO matches (first_club, second_club, league_id, seasons_id, result_id, match_day) " \
                         "values (%s,%s,%s,%s,%s,'%s') on conflict do nothing;" % args
        self.insert(sql_query, cookies=False)


    def insert(self, sql_query, table_name=None, value=None, cookies=True):
        """
        This function sends sql query to database or save
        :param sql_query: String object as sql query
        :param table_name: Name of the table in which the data is written
        :param value: Value of the table
        :param cookies: Save values id in dictionary. Default True
        :return: Row id or None
        """

        try:
            self.cursor.execute(sql_query)  # send query
        except Exception as error:
            self.conn.rollback()
        finally:
            self.conn.commit()  # save data in database
            # self.conn.commit()

        if cookies:
            id_of_new_row = self.cursor.fetchone()[0]  # get row id
            self.cookies[table_name][value] = id_of_new_row  # save id in cookies dictionary
            return id_of_new_row

        return None


    @staticmethod
    def string_to_date(value: str):
        """
        This function converts string data from [item:SoccerItem] to datetime object.
        :param value: string object ["%d %b %Y, %H:%M", "Yesterday, %d %b , %H:%M"]
        :return: Datetime object.
        """

        if value.find("Today", ) == -1 and value.find("Yesterday", ) == -1:
            return datetime.strptime(value, "%d %b %Y, %H:%M")
        if value.find("Today", ) >= 0:
            value = value.replace("Today,", str(datetime.today().year))
        elif value.find("Yesterday", ) >= 0:
            value = value.replace("Yesterday,", str(datetime.today().year))

        return datetime.strptime(value, "%Y %d %b , %H:%M")


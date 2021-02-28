import os

import psycopg2


class Database:
    def __init__(self):
        self.__database: str = os.getenv("DB_database")
        self.__user: str = os.getenv("DB_user")
        self.__password: str = os.getenv("DB_password")

        # Establishing the connection
        self.conn = psycopg2.connect(database=self.__database, user=self.__user,
                                     password=self.__password, host='localhost', port='5432')
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor()

    def __del__(self) -> None:
        # Closing the connection
        self.conn.close()
        self.cursor.close()


if __name__ == '__main__':
    pass

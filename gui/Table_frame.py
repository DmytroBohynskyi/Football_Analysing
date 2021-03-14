from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

from gui.db_conect import DataBase

HEADER_LABELS = {
    "MATCH LIST": ["First Team", "Result1", "Result1", "Second Team", "data"],
    "STATISTIC": ["First Team", "Won matches", "Drawn matches", "Lost matches", "Points"]
}

TABLE_STYLE = """
QTableWidget{
font: 14pt "Futura";
border : 1px solid #616161;
background :#212121;
color:#EEEEEE;
}

QTableWidget::item:hover{
border : 0px solid;
background : #424242;
}

QTableWidget QScrollBar:vertical {            
    border: 1px solid #999999;
    background:white;
    width:10px;    
    margin: 0px 0px 0px 0px;
}
QTableWidget QScrollBar::handle:vertical {
    background: #004D40;
    border-round: 3 px;
}

"""


class Table_Frame(QTableWidget):
    def __init__(self, data_base, **kwargs):
        super(Table_Frame, self).__init__()
        # table class values
        self.database: DataBase = data_base
        self.action = kwargs.get("action_")
        self.season = kwargs.get("season")
        self.country = kwargs.get("country")
        self.league = kwargs.get("league")
        # set table design
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setStyleSheet(TABLE_STYLE)

        # definite columns and set they size
        self.columns_create()
        self.set_size()

        # show table
        self.data_from_db = self.__load_data() # load data from data base
        if self.action == "MATCH LIST":
            self.show_match_list()
        else:
            self.show_statistic()

    def columns_create(self) -> None:
        """
        This function defines the columns of the table
        :return:None
        """
        header = HEADER_LABELS.get(self.action)  # gen columns names
        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)

    def set_size(self):
        """
        This function sets the size for each column
        :return: None
        """
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        if self.action == "MATCH LIST":
            header.setSectionResizeMode(3, QHeaderView.Stretch)
        else:
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def __load_data(self):
        """
        This function loads datha from data base
        """
        if self.action == "MATCH LIST":  # load data about matches
            data_from_db = self.database.get_matches(self.season, self.league)
        if self.action == "STATISTIC":  # load data about  statistic
            data_from_db = self.database.get_statistic(self.league, self.season, )
        return data_from_db

    def show_match_list(self) -> None:
        """
        This function show match items, from self.data_from_db.
        :return: None
        """
        for table_row, row in enumerate(self.data_from_db):
            self.insertRow(table_row)
            for column, item in enumerate(row):
                self.setItem(table_row, column, QTableWidgetItem(str(item)))

    def show_statistic(self) -> None:
        """
        This function show statistic items, from self.data_from_db.
        :return:
        """
        for table_row, row in enumerate(self.data_from_db):  # get name row name
            self.insertRow(table_row)  # create new row in table
            self.setItem(table_row, 0, QTableWidgetItem(row))  # save name in first column
            for column, item in enumerate(self.data_from_db.get(row), start=1):  # save other data
                self.setItem(table_row, column, QTableWidgetItem(str(self.data_from_db[row][item])))

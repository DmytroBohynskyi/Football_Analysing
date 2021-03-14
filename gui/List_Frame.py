from PySide6.QtWidgets import QListWidget

from gui.db_conect import DataBase

LIST_STYLE = """
QListWidget{
font: 20pt "Roboto";
border : 0px solid;
background :#212121;
color:#EEEEEE;
}
QListWidget QScrollBar{
background : lightblue;
}
QListView::item:hover{
border : 0px solid;
background : #424242;
}
QListView::item:selected{
border : 2px solid black;
background : #424242;
}
QListView::item:pressed{
border : 0px solid;
background : #00796B;
}
"""


class List_Frame(QListWidget):
    def __init__(self, action, data_base, **kwargs):
        super(List_Frame, self).__init__()
        self.database: DataBase = data_base
        self.action: str = action
        self.other_information: dict = kwargs
        self.first_club = None
        # set list style
        self.setStyleSheet(LIST_STYLE)
        # work with items
        list_item = self.__load_data()
        self.addItems(list_item)
        # Signals
        self.itemClicked.connect(self.item_click)

    def __load_data(self):
        """
        This function loads datha from data base
        """
        if self.action in ["STATISTIC", 'PROBABLY', "MATCH LIST"]:
            list_item = self.database.get_league(self.other_information.get("country"))  # get Tournament list
        elif self.action == "seasons":
            list_item = self.database.get_season(self.other_information.get("league"))
        elif self.action == "clubs":
            list_item = self.database.get_clubs(self.other_information.get("league"))
        return list_item

    def item_click(self, item):
        """
        This function opens the next frame depending on the current action
        :param item: item they clicked on
        :return: None
        """
        top_widget = self.topLevelWidget()  # main_windows object

        if self.action in ["STATISTIC", 'MATCH LIST']:
            top_widget.create_list(action="seasons", league=item.text(), **self.other_information)
        elif self.action == "PROBABLY":
            top_widget.create_list(action="clubs", league=item.text(), **self.other_information)
        elif self.action == "seasons":
            top_widget.create_table(season=item.text(), **self.other_information)
        elif self.action == "clubs":
            if self.first_club and self.first_club != item.text():
                top_widget.load_probability(first_club=self.first_club, second_club=item.text(),
                                            **self.other_information)
            else:
                self.first_club = item.text()
        print(item, str(item.text()))

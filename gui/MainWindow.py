import os
import sys

import PySide6
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget

from gui.List_Frame import List_Frame
from gui.Screen_design import NewWindow, ButtonWidget
from gui.Table_frame import Table_Frame
from gui.db_conect import DataBase
from gui.fuzzy import Fuzzy


dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainWindow(QMainWindow, NewWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        NewWindow.__init__(self)

        self.database = DataBase()  # connect with data base

        # self.start_btn.clicked.connect(self.refresh) # refresh button
        self.back_btn.clicked.connect(self.go_to_back)  # signal, ig clicked on "back_btn" then open "go_to_back"

        self.program_start()  # start function

    def program_start(self) -> None:
        """
        This function creates start page
        :return: None
        """
        page: QWidget = ButtonWidget(["POLAND", "ENGLAND"], sub_text="\n (league)")
        self.stackedWidget.addWidget(page)

        self.back_btn.setVisible(False)
        self.start_btn.setVisible(False)

    def second_page(self, country: str) -> None:
        """
        This function creates second page, with push buttons
        :param country:str,the country that was selected on page 1
        :return: None
        """
        self.back_btn.setVisible(True)
        # Create page, we passe the names of the buttons and country name
        second_page: QWidget = ButtonWidget(["STATISTIC", 'PROBABLY', "MATCH LIST"], country=country)
        self.add_new_frame(second_page)

    def create_list(self, action, **kwargs):
        """
        This function creates page with  items list
        :param action: What have to show, for example: seasons list, clubs list
        :param kwargs: Save previously data, for example: country, league ...
        :return: None
        """
        my_list_widget: QWidget = List_Frame(action, self.database, **kwargs)
        self.add_new_frame(my_list_widget)

    def load_probability(self, first_club, second_club, **kwargs):
        """
        This function counts the probability
        :param first_club:
        :param second_club:
        :param kwargs:
        :return:
        """
        probability = Fuzzy(first_club, second_club)
        results = probability.start_symulation(self.database, **kwargs)
        print(f"The match between {first_club} and {second_club} will end in a draw with probability: {results} %")

    def create_table(self, **kwargs):
        """
        This functions creates table frame this statistic data or matches list
        :param kwargs: Save previously data, for example: country, league ...
        :return: None
        """
        my_table_widget: QWidget = Table_Frame(self.database, **kwargs)
        self.add_new_frame(my_table_widget)

    def add_new_frame(self, frame: QWidget) -> None:
        """
        This function adds object of QWidget to stackedWidget and open new frame.
        :param frame: object of QWidget class with new frame.
        :return: None
        """
        self.stackedWidget.addWidget(frame)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)

    def go_to_back(self):
        """
        This function deletes the current page and opens the previous one
        :return: None
        """
        # Get current_widget
        current_widget: QWidget = self.stackedWidget.currentWidget()
        current_index = self.stackedWidget.currentIndex()
        # If current frame is second frame then hide the back_btn
        if current_index == 1:
            self.back_btn.setVisible(False)
        # Remove current frame
        self.stackedWidget.setCurrentIndex(current_index - 1)
        self.stackedWidget.removeWidget(current_widget)

    def refresh(self):
        pass

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        """
        This function closes the connection from the data
        :param event:
        :return: None
        """
        self.database.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

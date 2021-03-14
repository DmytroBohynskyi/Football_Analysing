from PySide6.QtCore import QMetaObject, QRect, QSize
from PySide6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QFrame, \
    QHBoxLayout

# from GUI_main import MainWindow

WIDTH = 1000
HEIGHT = 700

BTN_STYLE = '''
    QPushButton{
                font: 12pt "Roboto";
                color: rgb(238, 238, 238); 
                border: 0px solid;
                %s}

    QPushButton:hover{background-color:#757575;} 
    QPushButton:pressed{background-color: #616161}
    '''


class ButtonWidget(QWidget):

    def __init__(self, btn_list: list, country: str = None, sub_text: str = " ", ) -> None:
        super(ButtonWidget, self).__init__()

        self.btn_width = 250
        self.btn_height = 200
        self.num_of_btn = len(btn_list)
        self.btn_splitter = 40  # size between buttons
        self.sub_text = sub_text
        self.country = country

        self.splitter_x = self.get_splitter()
        self.generate_button(btn_list)

    def generate_button(self, btn_list: list) -> None:
        for n, name in enumerate(btn_list):
            x: int = int(self.splitter_x + n * (self.btn_width + self.btn_splitter))
            position = QRect(x, 200, self.btn_width, self.btn_height)
            self.add_button(name, position)

    def get_splitter(self) -> int:
        splitter = (WIDTH - (self.num_of_btn * self.btn_width + (self.num_of_btn - 1) * self.btn_splitter)) / 2
        return int(splitter)

    def add_button(self, name: str, position: QRect):
        button = QPushButton(f"{name} {self.sub_text}", self)
        button.setGeometry(position)
        button.setObjectName(f"{name}")
        button.setStyleSheet(BTN_STYLE % "background-color: #424242;")
        button.clicked.connect(lambda: self.open_next_page(button))

    def open_next_page(self, button: QPushButton):
        action: str = button.objectName()
        main_widget = self.topLevelWidget()
        if action in ["POLAND", "ENGLAND"]:
            main_widget.second_page(country=action)
        elif action in ["STATISTIC", 'PROBABLY', "MATCH LIST"]:
            main_widget.create_list(action, country=self.country.lower(), action_=action)


class NewWindow:
    def __init__(self: QMainWindow):
        self.setMinimumSize(WIDTH, HEIGHT)
        self.setStyleSheet("background-color: #212121;")
        # Add content
        self.central_widget = self.__create_central_widget(self)
        self.central_layout = self.__create_box_layout(self.central_widget)
        # =================== Top frame -> ===================
        self.top_frame = self.__create_frame(parent=self.central_widget, name="top_frame", size=QSize(16777215, 60),
                                             min_size=QSize(16777215, 60), layout=self.central_layout)

        self.top_layout = self.__create_horizontal_layout(parent=self.top_frame, name="top_layout")
        # Top left frame
        self.top_left_frame = self.__create_frame(self.top_frame, name="top_left_frame", size=QSize(150, 16777215),
                                                  layout=self.top_layout)
        self.top_left_layout = self.__create_horizontal_layout(parent=self.top_left_frame, name="top_left_Layout")

        # Top center frame
        self.top_centre_frame = self.__create_frame(self.top_frame, name="centre_frame", layout=self.top_layout)

        # Top right frame
        self.top_right_frame = self.__create_frame(self.top_frame, name="top_right_frame", layout=self.top_layout,
                                                   size=QSize(150, 16777215))
        self.top_right_layout = self.__create_horizontal_layout(parent=self.top_left_frame, name="top_left_Layout")

        # Button
        self.back_btn: QPushButton = self.__create_btn(self.top_left_frame, "BACK", name="back_btn",
                                                       layout=self.top_left_layout)
        self.start_btn: QPushButton = self.__create_btn(self.top_right_frame, "MAIN", name="start_btn",
                                                        layout=self.top_right_layout)

        # =================== CONTENT frame -> ===================
        self.content_frame = self.__create_frame(parent=self.central_widget, name="content_frame",
                                                 layout=self.central_layout)
        self.content_layout = self.__create_horizontal_layout(parent=self.content_frame, name="content_layout")

        self.stackedWidget = QStackedWidget(self.central_widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.content_layout.addWidget(self.stackedWidget)
        # start page
        # self.__program_start()

        #
        self.setCentralWidget(self.central_widget)
        QMetaObject.connectSlotsByName(self)

    @staticmethod
    def __create_central_widget(parent: QMainWindow) -> QWidget:
        central_widget = QWidget(parent)
        central_widget.setObjectName("centralwidget")
        central_widget.setStyleSheet("background-color: #212121")
        return central_widget

    @staticmethod
    def __create_frame(parent: QWidget, name: str, size=QSize(16777215, 16777215), min_size=QSize(0, 0), layout=None,
                       style=None) -> QWidget:
        frame = QFrame(parent)
        frame.setObjectName(name)
        frame.setMaximumSize(size)
        frame.setMinimumSize(min_size)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Raised)
        layout.addWidget(frame) if layout else None
        frame.setStyleSheet(style) if style else None
        return frame

    @staticmethod
    def __create_box_layout(parent: QWidget) -> QVBoxLayout:
        layout = QVBoxLayout(parent)
        layout.setSpacing(0)
        layout.setObjectName(u"central_layout")
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    @staticmethod
    def __create_horizontal_layout(parent: QWidget, name: str) -> QVBoxLayout:
        layout = QHBoxLayout(parent)
        layout.setSpacing(0)
        layout.setObjectName(name)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    @staticmethod
    def __create_btn(parent: QWidget, text: str, name: str, layout=None, size=QSize(150, 60)) -> QPushButton:
        push_button = QPushButton(parent)
        push_button.setObjectName(name)
        push_button.setText(text)
        push_button.setMinimumSize(size)
        push_button.setStyleSheet(BTN_STYLE % "")
        # add to layout
        layout.addWidget(push_button) if layout else None
        return push_button

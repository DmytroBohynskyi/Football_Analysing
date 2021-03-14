import argparse
import sys
import warnings

from PySide6.QtWidgets import QApplication
from scrapy import cmdline

from gui.MainWindow import MainWindow


def open_gui() -> None:
    """
    This function shows GUI.
    :return: None
    """
    # Show Main Windows
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def start_scrapy() -> None:
    """
    This function starts parsing.
    :return:
    """
    cmdline.execute("scrapy crawl parser".split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List the options:')
    parser.add_argument("--parsing", help="Starts the page parsing (https://www.oddsportal.com)",
                        action="store_true")
    parser.add_argument("--gui", help="Opens the project gui",
                        action="store_true")

    args = parser.parse_args()

    if args.gui:  # start gui
        open_gui()
    elif args.parsing:  # start parsing
        start_scrapy()
    else:
        warnings.warn('Please use argument: \n')
        parser.print_help()

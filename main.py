# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui import WallpaperApp


def main():
    app = QApplication(sys.argv)
    wallpaper_app = WallpaperApp()
    wallpaper_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

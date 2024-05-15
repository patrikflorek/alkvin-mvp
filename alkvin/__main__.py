import os

from .config import app_dirs

from alkvin.main import MainApp


def create_app_dirs():
    for dir_path in app_dirs:
        os.makedirs(dir_path, exist_ok=True)


if __name__ == "__main__":
    create_app_dirs()

    MainApp().run()

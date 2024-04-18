from kivy.properties import StringProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class DeleteBotDialog(MDDialog):
    bot_name = StringProperty()

    def __init__(self, **kwargs):
        self.title = "Delete bot"
        self.text = "Are you sure you want to delete this bot?"
        self.buttons = [
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: self.dismiss(),
            ),
            MDFlatButton(
                text="DELETE",
                theme_text_color="Error",
                on_release=lambda x: self.on_delete_bot_callback(),
            ),
        ]
        super().__init__(**kwargs)

    def on_delete_bot_callback(self):
        pass

    def open(self, bot_name, on_delete_bot_callback):
        self.text = f"Are you sure you want to delete bot {bot_name}?"
        self.on_delete_bot_callback = on_delete_bot_callback

        super().open()

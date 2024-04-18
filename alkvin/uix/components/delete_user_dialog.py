from kivy.properties import StringProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class DeleteUserDialog(MDDialog):
    user_name = StringProperty()

    def __init__(self, **kwargs):
        self.title = "Delete user"
        self.text = "Are you sure you want to delete this user?"
        self.buttons = [
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: self.dismiss(),
            ),
            MDFlatButton(
                text="DELETE",
                theme_text_color="Error",
                on_release=lambda x: self.on_delete_user_callback(),
            ),
        ]
        super().__init__(**kwargs)

    def on_delete_user_callback(self):
        pass

    def open(self, user_name, on_delete_user_callback):
        self.text = f"Are you sure you want to delete user {user_name}?"
        self.on_delete_user_callback = on_delete_user_callback

        super().open()

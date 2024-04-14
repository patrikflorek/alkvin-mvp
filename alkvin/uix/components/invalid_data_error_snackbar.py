from kivy.core.window import Window
from kivy.properties import StringProperty

from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton


class InvalidDataErrorSnackbar(MDSnackbar):
    """Snackbar for displaying an error message when invalid data is detected."""

    text = StringProperty()

    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text

        self.error_label = MDLabel(text=self.text, padding="10dp")
        self.add_widget(self.error_label)

        self.add_widget(
            MDSnackbarActionButton(
                text="OK",
                on_release=self.dismiss,
                pos_hint={"right": 1, "center_y": 0.5},
            )
        )

    def on_text(self, instance, value):
        self.error_label.text = value

    def open(self):
        if self in Window.parent.children:
            return

        super().open()

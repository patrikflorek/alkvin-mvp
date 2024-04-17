"""
Select User Dialog
==================

This module contains the SelectUserDialog class, which is a custom dialog widget
used for selecting a chat user from a list of available chat users.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem


Builder.load_string(
    """
<SelectUserListItem>:
    id: select_user_list_item

    on_release: user_select_checkbox.active = True

    IconLeftWidget:
        MDCheckbox:
            id: user_select_checkbox
            _select_user_list_item: select_user_list_item
            group: "users"
            
            on_release: self.active = True

    IconRightWidget:
        icon: "pencil"
        disabled: not user_select_checkbox.active
        opacity: int(user_select_checkbox.active)
        
        on_release: root.edit_user()
"""
)


class SelectUserListItem(OneLineAvatarIconListItem):
    """Custom list item widget for selecting a chat user."""

    user_id = NumericProperty()

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.app = MDApp.get_running_app()

    def edit_user(self):
        chat_screen = self.app.root.get_screen("chat_screen")
        chat_screen.select_user_dialog.dismiss()
        self.app.root.switch_screen("user_screen", {"user_id": self.user_id})


class SelectUserDialog(MDDialog):
    """Custom dialog widget for selecting a chat user."""

    selected_user_id = NumericProperty()

    def __init__(self, on_select_user_callback, **kwargs):
        self.on_select_user_callback = on_select_user_callback

        super().__init__(
            title="Chat user",
            text="Select a user from the list below or create a new user",
            type="confirmation",
            buttons=[
                MDFlatButton(
                    text="CREATE NEW",
                    on_release=self._create_new_user,
                ),
                MDFlatButton(
                    text="SELECT",
                    on_release=self._select_user,
                ),
            ],
            auto_dismiss=False,
            **kwargs,
        )

        self.app = MDApp.get_running_app()

    def open(self, items_data, chat_user_id=None):
        if chat_user_id is not None:
            self.selected_user_id = chat_user_id

    def _create_new_user(self, instance):
        self.dismiss()

        self.app.root.switch_screen("user_screen")

    def _select_user(self, instance):
        self.dismiss()

        self.on_select_user_callback(self.selected_user_id)

    def _select_user_list_item_active(self, checkbox, is_active):
        if is_active:
            self.selected_user_id = checkbox._select_user_list_item.user_id

    def _get_select_user_list_items(self, items_data, selected_user_id):
        if selected_user_id is not None:
            self.selected_user_id = selected_user_id

        select_user_list_items = []
        is_selected_user_id_found = False

        for item_data in items_data:
            select_user_list_item = SelectUserListItem(
                user_id=item_data["user_id"], text=item_data["user_name"]
            )

            select_user_list_item.ids.user_select_checkbox.bind(
                active=self._select_user_list_item_active
            )

            if item_data["user_id"] == self.selected_user_id:
                select_user_list_item.ids.user_select_checkbox.active = True
                is_selected_user_id_found = True

            select_user_list_items.append(select_user_list_item)

        if not is_selected_user_id_found:
            select_user_list_items[0].ids.user_select_checkbox.active = True
            self.selected_user_id = select_user_list_items[0].user_id

        return select_user_list_items

    def update_items(self, items_data, selected_user_id=None):
        super().update_items(
            self._get_select_user_list_items(items_data, selected_user_id)
        )

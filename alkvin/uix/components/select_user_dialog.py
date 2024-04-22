"""
Select User Dialog
==================

This module contains the SelectUserDialog class, which is a custom dialog widget
used for selecting a chat user from a list of available chat users.
"""

from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem

from alkvin.entities.user import User


Builder.load_string(
    """
<SelectUserListItem>:
    preselected: False
    divider: None
    text: root.user_name
    
    on_release: user_select_checkbox.active = True
    
    IconLeftWidget:
        MDCheckbox:
            id: user_select_checkbox
            group: "users"
            
            on_release: root.preselected = self.active

    IconRightWidget:
        icon: "pencil"
        disabled: not user_select_checkbox.active
        opacity: int(user_select_checkbox.active)
        
        on_release: root.editing_user = True
"""
)


class SelectUserListItem(OneLineAvatarIconListItem):
    """Custom list item widget for selecting a chat user."""

    preselected = BooleanProperty(False)
    editing_user = BooleanProperty(False)

    user_id = NumericProperty()
    user_name = StringProperty()


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
                    on_release=self.create_user,
                ),
                MDFlatButton(
                    text="SELECT",
                    on_release=self.select_user,
                ),
            ],
            auto_dismiss=False,
            **kwargs,
        )

        self.app = MDApp.get_running_app()

    def open(self, chat_user_id=None):
        if User.select().count() == 0:
            User.create(name="Dummy User")

        users = User.select(User.id, User.name).order_by(User.name)
        user_ids = [user.id for user in users]
        self.selected_user_id = (
            chat_user_id if chat_user_id in user_ids else user_ids[0]
        )
        user_list_items = []
        for user in users:
            user_list_item = SelectUserListItem(user_id=user.id, user_name=user.name)
            if user.id == self.selected_user_id:
                user_list_item.ids.user_select_checkbox.active = True

            user_list_item.bind(preselected=self.preselect_user)
            user_list_item.bind(editing_user=self.edit_user)
            user_list_items.append(user_list_item)

        self.update_items(user_list_items)

        super().open()

    def create_user(self, instance):
        new_user = User.new()
        self.on_select_user_callback(new_user.id)

        self.dismiss()

        self.app.root.switch_screen("user_create_screen", new_user.id)

    def preselect_user(self, user_list_item, value):
        if value:
            self.selected_user_id = user_list_item.user_id

    def edit_user(self, user_list_item, value):
        self.on_select_user_callback(user_list_item.user_id)

        self.dismiss()

        self.app.root.switch_screen("user_screen", user_list_item.user_id)

    def select_user(self, instance):
        self.on_select_user_callback(self.selected_user_id)

        self.dismiss()

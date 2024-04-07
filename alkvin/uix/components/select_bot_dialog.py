"""
Select Bot Dialog
=================

This module contains the SelectBotDialog class, which is a custom dialog widget
used for selecting a chat bot from a list of available chat bots.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem


Builder.load_string(
    """
<SelectBotListItem>:
    id: select_bot_list_item

    on_release: bot_select_checkbox.active = True

    IconLeftWidget:
        MDCheckbox:
            id: bot_select_checkbox
            _select_bot_list_item: select_bot_list_item
            group: "bots"
            
            on_release: self.active = True

    IconRightWidget:
        icon: "pencil"
        disabled: not bot_select_checkbox.active
        opacity: int(bot_select_checkbox.active)
        
        on_release: root.edit_bot()
"""
)


class SelectBotListItem(OneLineAvatarIconListItem):
    """Custom list item widget for selecting a chat bot."""

    bot_id = NumericProperty()

    def __init__(self, bot_id, **kwargs):
        super().__init__(**kwargs)
        self.bot_id = bot_id
        self.app = MDApp.get_running_app()

    def edit_bot(self):
        chat_screen = self.app.root.get_screen("chat_screen")
        chat_screen.select_bot_dialog.dismiss()
        self.app.root.switch_screen("bot_screen", {"bot_id": self.bot_id})


class SelectBotDialog(MDDialog):
    """Custom dialog widget for selecting a chat bot."""

    selected_bot_id = NumericProperty()

    def __init__(self, on_select_bot_callback, **kwargs):
        self.on_select_bot_callback = on_select_bot_callback

        super().__init__(
            title="Chat bot",
            text="Select a bot from the list below or create a new bot",
            type="confirmation",
            buttons=[
                MDFlatButton(
                    text="CREATE NEW",
                    on_release=self._create_new_bot,
                ),
                MDFlatButton(
                    text="SELECT",
                    on_release=self._select_bot,
                ),
            ],
            auto_dismiss=False,
            **kwargs,
        )

        self.app = MDApp.get_running_app()

    def _create_new_bot(self, instance):
        self.dismiss()

        self.app.root.switch_screen("bot_screen")

    def _select_bot(self, instance):
        self.dismiss()

        self.on_select_bot_callback(self.selected_bot_id)

    def _select_bot_list_item_active(self, checkbox, is_active):
        if is_active:
            self.selected_bot_id = checkbox._select_bot_list_item.bot_id

    def _get_select_bot_list_items(self, items_data, selected_bot_id):
        if selected_bot_id is not None:
            self.select_bot_id = selected_bot_id

        select_bot_list_items = []
        is_selected_bot_id_found = False

        for item_data in items_data:
            select_bot_list_item = SelectBotListItem(
                bot_id=item_data["bot_id"], text=item_data["bot_name"]
            )

            select_bot_list_item.ids.bot_select_checkbox.bind(
                active=self._select_bot_list_item_active
            )

            if item_data["bot_id"] == self.selected_bot_id:
                select_bot_list_item.ids.bot_select_checkbox.active = True
                is_selected_bot_id_found = True

            select_bot_list_items.append(select_bot_list_item)

        if not is_selected_bot_id_found:
            select_bot_list_items[0].ids.bot_select_checkbox.active = True
            self.select_bot_id = select_bot_list_items[0].bot_id

        return select_bot_list_items

    def update_items(self, items_data, selected_bot_id=None):
        super().update_items(
            self._get_select_bot_list_items(items_data, selected_bot_id)
        )

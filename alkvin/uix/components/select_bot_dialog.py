"""
Select Bot Dialog
=================

This module contains the SelectBotDialog class, which is a custom dialog widget
used for selecting a chat bot from a list of available chat bots.

Example usage:
    dialog = SelectBotDialog(on_select_bot_callback=lambda bot_id: print(f"Bot selected: {bot_id}"))
    dialog.open(chat_bot_id=1)
"""

from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem

from alkvin.entities.bot import Bot


Builder.load_string(
    """
<SelectBotListItem>:
    divider: None
    text: root.bot_name

    on_release: bot_select_checkbox.active = True

    IconLeftWidget:
        MDCheckbox:
            id: bot_select_checkbox
            group: "bots"
            
            on_active: root.preselected = self.active

    IconRightWidget:
        icon: "pencil"
        disabled: not bot_select_checkbox.active
        opacity: int(bot_select_checkbox.active)
        
        on_release: root.editing_bot = True
"""
)


class SelectBotListItem(OneLineAvatarIconListItem):
    """Custom list item widget for selecting a chat bot."""

    preselected = BooleanProperty(False)
    editing_bot = BooleanProperty(False)

    bot_id = NumericProperty()
    bot_name = StringProperty()


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
                    on_release=self.create_bot,
                ),
                MDFlatButton(
                    text="SELECT",
                    on_release=self.select_bot,
                ),
            ],
            auto_dismiss=False,
            **kwargs,
        )

        self.app = MDApp.get_running_app()

    def preselect_bot(self, bot_list_item, value):
        if value:
            self.selected_bot_id = bot_list_item.bot_id

    def edit_bot(self, bot_list_item, value):
        self.on_select_bot_callback(bot_list_item.bot_id)

        self.dismiss()

        self.app.root.switch_screen("bot_screen", bot_list_item.bot_id)

    def open(self, chat_bot_id=None):
        self.auto_dismiss = (
            chat_bot_id is not None
        )  # Can only dismiss if a bot is preselected

        # There must be at least one bot in the database
        if Bot.select().count() == 0:
            Bot.create(name="Dummy Bot")

        bots = Bot.select(Bot.id, Bot.name).order_by(Bot.name)
        bot_ids = [bot.id for bot in bots]
        self.selected_bot_id = chat_bot_id if chat_bot_id in bot_ids else bot_ids[0]

        bot_list_items = []
        for bot in bots:
            bot_list_item = SelectBotListItem(bot_id=bot.id, bot_name=bot.name)
            if bot.id == self.selected_bot_id:
                bot_list_item.ids.bot_select_checkbox.active = True

            bot_list_item.bind(preselected=self.preselect_bot)
            bot_list_item.bind(editing_bot=self.edit_bot)
            bot_list_items.append(bot_list_item)

        self.update_items(bot_list_items)

        super().open()

    def create_bot(self, instance):
        new_bot = Bot.new()
        self.on_select_bot_callback(new_bot.id)

        self.dismiss()

        self.app.root.switch_screen("bot_create_screen", new_bot.id)

    def select_bot(self, instance):
        self.on_select_bot_callback(self.selected_bot_id)

        self.dismiss()

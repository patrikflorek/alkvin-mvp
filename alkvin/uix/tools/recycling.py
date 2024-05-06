"""
Recycling Bin
=============

This module defines the RecyclingBin class, which is used to recycle message 
widgets. Its purpose is to increase the application performance by preventing
unnecessary creation and destruction of message widgets.

When there are no more references to a message widget, upon request 
the RecyclingBin class creates and stores a new instance of appropriate 
message widget.
"""

from alkvin.uix.components.user_message_card import UserMessageCard
from alkvin.uix.components.assistant_message_card import AssistantMessageCard

from alkvin.entities.user_message import UserMessage
from alkvin.entities.assistant_message import AssistantMessage


def get_recycling_bin():
    if not hasattr(get_recycling_bin, "recycling_bin"):
        get_recycling_bin.recycling_bin = RecyclingBin()

    return get_recycling_bin.recycling_bin


class RecyclingBin:
    def __init__(self):
        self.user_message_widgets = []
        self.assistant_message_widgets = []

    def get_message_widget(self, message, chat):
        if isinstance(message, UserMessage):
            if self.user_message_widgets:
                message_widget = self.user_message_widgets.pop()
                message_widget.message = message
                message_widget.chat = chat
            else:
                message_widget = UserMessageCard(message, chat)

            return message_widget
        elif isinstance(message, AssistantMessage):
            if self.assistant_message_widgets:
                message_widget = self.assistant_message_widgets.pop()
                message_widget.message_widget = message
            else:
                message_widget = AssistantMessageCard(message, chat)

            return message_widget
        else:
            raise ValueError("Unsupported message type.")

    def recycle_message_widgets(self, message_widgets):
        for message_widget in message_widgets:
            if message_widget.parent is not None:
                message_widget.parent.remove_widget(message_widget)

            if isinstance(message_widget, UserMessageCard):
                self.user_message_widgets.append(message_widget)
            elif isinstance(message_widget, AssistantMessageCard):
                self.assistant_message_widgets.append(message_widget)
            else:
                raise ValueError("Unsupported message widget type.")

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

    def get_message_widget(self, message):
        if isinstance(message, UserMessage):
            if self.user_message_widgets:
                message_widget = self.user_message_widgets.pop()
                message_widget.message = message

                return message_widget

            return UserMessageCard(message)
        elif isinstance(message, AssistantMessage):
            if self.assistant_message_widgets:
                message_widget = self.assistant_message_widgets.pop()
                message_widget.message_widget = message

                return message_widget

            return AssistantMessageCard(message)
        else:
            raise ValueError("Unsupported message type.")

    def recycle_message_widgets(self, message_widgets):
        for message_widget in message_widgets:
            if isinstance(message_widget, UserMessageCard):
                self.user_message_widgets.append(message_widget)
            elif isinstance(message_widget, AssistantMessageCard):
                self.assistant_message_widgets.append(message_widget)
            else:
                raise ValueError("Unsupported message widget type.")

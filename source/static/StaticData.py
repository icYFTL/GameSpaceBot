import threading


class StaticData:
    stack_messages = []
    current_games = []
    new_message_trigger = threading.Event()

    name = "GameSpaceBot"
    version = "1.2 Release"
    author = "icYFTL"

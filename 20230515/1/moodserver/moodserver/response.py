"""Module with Response class."""


class Response:
    """
    Response class.

    It is used to pass information to server about
    what messages to send to players.
    """

    def __init__(self, text, insert_values, send_method, player=None):
        assert send_method in ['broadcast', 'personal', 'others']
        self.text = text
        self.insert_values = insert_values
        self.send_method = send_method
        self.player = player

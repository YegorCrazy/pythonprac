"""Module with Response class."""


class Response:
    """
    Response class.

    It is used to pass information to server about
    what messages to send to players.
    """

    def __init__(self, text, send_method):
        assert send_method in ['broadcast', 'personal', 'others']
        self.text = text
        self.send_method = send_method

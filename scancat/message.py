"""Message allows output of messages to a websocket or via print.

Usage:
1. `from scancat.message import msg` in main.py.
2. Set `msg.websocket = ws` where ws is the open socket.
3. Send messages to the socket with msg.send() and msg.title().

msg is effectively a singleton instance, so it can be reused between modules.
"""
import logging


class Message():
    websocket = None

    def send(self, message, log=False):
        """Send a message to the WebSocket if open, otherwise print it.

        :param message: The message to send
        :type message: string
        :param log: Log the message if True, defaults to False
        :type log: bool, optional
        """
        if log:
            logging.info(message)
        if self.websocket and not self.websocket.closed:
            self.websocket.send(message)
            logging.debug('Sending: ' + message)
        else:
            print(message)

    def title(self, title, level=2):
        """Send a title. Used to break messages into sections.

        :param title: The text to send to screen or the socket
        :type title: string
        :param level: The header level to use, defaults to 2
        :type level: int
        """
        if self.websocket and not self.websocket.closed:
            tag = 'h' + str(level)
            self.websocket.send('<' + tag + '>' + title + '</' + tag + '>')
            logging.debug('Sending title: ' + title)
        else:
            print('\n===' + title + '===')


msg = Message()

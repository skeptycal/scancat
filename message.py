"""Message allows output of messages to a websocket or via print."""
import logging

class Message():
    websocket = None

    def send(self, message):
        """Send a message to the socket if open, otherwise print it."""
        if self.websocket and not self.websocket.closed:
            self.websocket.send(message)
            logging.debug('Sending: ' + message)
        else:
            print(message)

    def title(self, title):
        """Send a title."""
        if self.websocket and not self.websocket.closed:
            self.websocket.send('<h2>' + title + '</h2>')
            logging.debug('Sending title: ' + title)
        else:
            print('\n===' + title + '===')


msg = Message() # Import msg from message, set websocket, then use msg.send().

"""Message allows output of messages to a websocket or via print."""
import logging

class Message():
    websocket = None

    def send(self, message):
        """Send a message to the socket if open, otherwise print it."""
        if self.websocket and not self.websocket.closed:
            self.websocket.send(message)
            print('Sending: ' + message)
        else:
            print(message)


msg = Message() # Import msg from message, set websocket, then use msg.send().

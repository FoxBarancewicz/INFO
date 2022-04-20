from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import bcrypt
from cryptography.fernet import Fernet

class messaging:

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2
        self.u1_messages = ['']*8
        self.u2_messages = ['']*8
    
    # user is the user message is sent from
    # should also encrypt using other users' key
    def message_send(self, user, message):
        if user == self.user_1:
            return self.u1_messages.insert(0, message)
        return self.u2_messages.insert(0, message)

    # user is defined as the person requesting messages
    def fetch_messages(self, user):
        if user == self.user_1:
            return self.u1_messages[:4] + self.u2_messages[:4]
        return self.u2_messages[:4] + self.u1_messages[:4]

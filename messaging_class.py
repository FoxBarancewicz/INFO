class messaging:

    u1_messages = ['']*8

    u2_messages = ['']*8

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2
    
    # user is the user message is sent from
    def message_send(self, user, message):
        if user == self.user_1:
            return self.u1_messages.insert(0, message)
        return self.u2_messages.insert(0, message)

    # user is defined as the person requesting messages
    def fetch_messages(self, user):
        if user == self.user_1:
            return self.u1_messages[:4] + self.u2_messages[:4]
        return self.u2_messages[:4] + self.u1_messages[:4]

'''
    if messages != None:
        message_array[current_index] = messages

        if current_index==7:
            i = 1
            while i<7:
                message_array[i] = message_array[i+1]
                i+=1
        else:
            current_index+=2
'''
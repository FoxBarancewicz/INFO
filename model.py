'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
from base64 import decode
from email import message
from email.utils import decode_rfc2231
import view
import random
import secrets
from bottle import request, response

from password_verify import verify_pass, verify_user

from messaging_class import messaging

from cryptography.fernet import Fernet

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
message_array=['']*8
current_index = 1 # init at 1 (i.e. blue boxes)
cookie_dict = {}

prev_messaging_class = None

# key: object, elements: user_1, user_2
messaging_class_ls = []

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password, curr_cookie):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # Checks for valid credentials
    login, err_str = verify_pass(username,password)
        
    if login: 
        # Generate cookie, store cookie in dict
        # Generate key
        given_cookie = curr_cookie

        # Checks if user already has cookie
        for cookie in cookie_dict:
            if cookie_dict[cookie][0] == username:
                curr_cookie = cookie

        # User doesn't have a cookie, issues a new one and adds to cookie_dict
        if given_cookie == curr_cookie:

            curr_cookie = secrets.token_hex(16)

            key = Fernet.generate_key()

            cookie_dict[curr_cookie] = (username, key)

        return page_view("valid", name=username), curr_cookie, login

    else:
        return page_view("invalid", reason=err_str), None, login

def messaging_service(cookie):
    '''
        messaging_service
        Returns the view for the messaging service if logged in
    '''
    
    if cookie in cookie_dict:
        #just to show the messaging page, modify however you want
        return page_view("messaging"
        ,name_to="Name"
        ,name_from=cookie_dict[cookie][0]
        ,one=message_array[0]
        ,two=message_array[1]
        ,three=message_array[2]
        ,four=message_array[3]
        ,five=message_array[4]
        ,six=message_array[5]
        ,seven=message_array[6]
        ,eight=message_array[7])
    else:
        return page_view("invalid_cookie")

#-----------------------------------------------------------------------------
def messages_send(message, cookie, send_to):
    # cookie used to ident which user is logged in, always set logged in user as 'blue' message boxes
    # messaging class to manage who is messaging who?
    # hashmap of from_to/send_to with class of chat.

    global prev_messaging_class

    user_from = cookie_dict[cookie][0]

    if send_to != None:

        curr_messaging_class = None

        for _class in messaging_class_ls:
            if ((_class.user_1 == send_to or _class.user_2 == send_to) and 
            (_class.user_1 == user_from or _class.user_2 == user_from)):
                # class already created for the two users
                curr_messaging_class = _class

        # creates new messaging class if users have no prior chat history
        if curr_messaging_class == None:
            curr_messaging_class = messaging(user_from, send_to)
            messaging_class_ls.append(curr_messaging_class)

        prev_messaging_class = curr_messaging_class 

    message_array = ['']*8
    new_message_arr = []

    '''
    When taking part in a two-way chat, the sender will encrypt messages with their private key (accessed through local 
    dictionary variable, referenced with sender's authentication cookie. (i.e. to send an encrypted message from 'user', 
    'user' must be logged in.)). The receiver of said message must have previously logged in for the current instance of
    the messaging webapp (i.e. receiver must have a unique log-in every time the server restarts). If authenticated, the
    receiver will be able to access the encrypted messages through access-control to the messaging class for any chat they
    are involved in. For messages sent by the receiver, these are decrypted locally using the receiver's private key (accessed
    in same way as for the sender, see above), and for messages received from the sender, these are decrypted (also locally),
    however using the sender's private key, with the effectively being given access to the private key of the sender for the
    purpose of decrypting the messages. The receiver does not ever see the senders' private-key, nor will the sender ever be able
    to see the receiver's private key.
    '''

    if prev_messaging_class != None:
        send_to = prev_messaging_class.user_1 if prev_messaging_class.user_1 != user_from else prev_messaging_class.user_2
        if message != None:
            prev_messaging_class.message_send(user_from, message)
        print(prev_messaging_class.u1_messages, prev_messaging_class.u2_messages)
        message_array = prev_messaging_class.fetch_messages(user_from)

    count = 0

    for message in message_array:

        # Handles first 4 messages in message_array, which represent messages sent from the logged-in user, 
        # to be decrypted using said users' key
        if message != '' and (count < 4):
            # Inits new fernet class using logged-in users' key
            fernet = Fernet(cookie_dict[cookie][1])
            new_message_arr.append(fernet.decrypt(message).decode())

        '''
        Access control: other users' key cannot be physically viewed, and can only be called upon when other user is verified as
        the other party in the messaging class between two parties.
        '''
        # Handles last 4 messages in message_array, representing messages sent from the other user in the two-way chat,
        # to be decrypted using the other users' key.
        if message != '' and (count >= 4):
            for user_cookie in cookie_dict:
                if cookie_dict[user_cookie][0] == send_to:
                    fernet = Fernet(cookie_dict[user_cookie][1])
                    new_message_arr.append(fernet.decrypt(message).decode())

        elif message == '':
            new_message_arr.append('')

        count += 1
        
    return page_view("messaging"
    ,name_to=send_to
    ,name_from=user_from
    ,one=new_message_arr[7]
    ,two=new_message_arr[3]
    ,three=new_message_arr[6]
    ,four=new_message_arr[2]
    ,five=new_message_arr[5]
    ,six=new_message_arr[1]
    ,seven=new_message_arr[4]
    ,eight=new_message_arr[0])
    


#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)

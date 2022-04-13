'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
from email import message
import view
import random
import secrets
from bottle import request

from password_verify import verify_pass

from messaging_class import messaging

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
def login_check(username, password):
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

        cookie = secrets.token_hex(16)
        cookie_dict[cookie] = (username)
        return page_view("valid", name=username), cookie, login

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
        ,name_from=cookie_dict[cookie]
        ,one=message_array[0]
        ,two=message_array[1]
        ,three=message_array[2]
        ,four=message_array[3]
        ,five=message_array[4]
        ,six=message_array[5]
        ,seven=message_array[6]
        ,eight=message_array[7])
        return page_view("valid_cookie")
    else:
        return page_view("invalid_cookie")

#-----------------------------------------------------------------------------
def messages_send(messages, cookie, send_to):
    # cookie used to ident which user is logged in, always set logged in user as 'blue' message boxes
    # messaging class to manage who is messaging who?
    # hashmap of from_to/send_to with class of chat.

    global prev_messaging_class

    user_from = cookie_dict[cookie]

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

    if messages != None:
        prev_messaging_class.message_send(user_from, messages)

    message_array = prev_messaging_class.fetch_messages(user_from)

    send_to = prev_messaging_class.user_1 if prev_messaging_class.user_1 != user_from else prev_messaging_class.user_2

    return page_view("messaging"
    ,name_to=send_to
    ,name_from=user_from
    ,one=message_array[7]
    ,two=message_array[3]
    ,three=message_array[6]
    ,four=message_array[2]
    ,five=message_array[5]
    ,six=message_array[1]
    ,seven=message_array[4]
    ,eight=message_array[0])
    


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

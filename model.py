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

from password_verify import verify_pass

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
message_array=['']*8
current_index = 0
cookie_dict = {}

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
        return page_view("messaging",name="fox",one=message_array[0],two=message_array[1],three=message_array[2],four=message_array[3],five=message_array[4],six=message_array[5],seven=message_array[6],eight=message_array[7])
        return page_view("valid_cookie")
    else:
        return page_view("invalid_cookie")

#-----------------------------------------------------------------------------
def messages_send(messages):
    global current_index
    
    if current_index==7:
        i = 0
        while i<7:
            message_array[i] = message_array[i+1]
            i+=1
    else:
        current_index+=1
        
    message_array[current_index]= messages
    return page_view("messaging",name="fox",one=message_array[0],two=message_array[1],three=message_array[2],four=message_array[3],five=message_array[4],six=message_array[5],seven=message_array[6],eight=message_array[7])
    


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
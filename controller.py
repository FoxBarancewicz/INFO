'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, error, request, static_file, response, request, redirect

import model

from Crypto.Hash import SHA512

from password_verify import verify_pass, verify_user

from cryptography.fernet import Fernet

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the messaging page
@get('/messaging')
def get_messaging():
    '''
        get_messaging

        Serves the messaging page
    '''


    cookie = request.get_cookie('auth')

    return model.messaging_service(cookie)

#-----------------------------------------------------------------------------

# Must message to a particular user
@post('/messaging')
def post_messaging():
    
    cookie = request.get_cookie('auth')

    send_to = request.forms.get('send_to')

    # Send message to server
    # message should be encrypted here
    message = request.forms.get('messages')

    # verify_user will return True if user exists in database, else false
    if not verify_user(send_to):
        send_to = None

    # Do some fancy encryption so that both parties can read message TODO

    fernet = Fernet(model.cookie_dict[cookie][1])

    if message != None:
        message = fernet.encrypt(message.encode())

    cookie = request.get_cookie('auth')

    return model.messages_send(message, cookie, send_to)

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()


#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    b64pwd = SHA512.new(password.encode()).digest()

    # Call the appropriate method
    valid_login, cookie, login = model.login_check(username, b64pwd, request.get_cookie('auth'))

    if login:

        response.set_cookie('auth', cookie, secure=True, httponly=True)

        redirect('/messaging')

    return valid_login

    # Set a cookie
    #response.set_cookie('auth', cookie, secure=True, httponly=True)


#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)

model.about()

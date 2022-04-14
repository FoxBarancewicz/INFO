from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import bcrypt
import binascii
#checks if the username is in database
def verify_username(username):
    
    with open('storage.csv', 'r') as f:
        while True:
            data = f.readline()
            if len(data) == 0:
                break
            if username==data[0]:
                return True
        return False



# password is pre-hashed in controller.py
def verify_pass(username, password):

    salt = None

    # fetches salt from storage file
    with open('storage.csv', 'r') as f:
        while True:
            data = f.readline()
            print(data)
            if len(data) == 0:
                break
            data = data.split(',')
            if data[0] == username:
                salt = binascii.unhexlify(data[2].strip("\n"))
                bcrypt_hash = bcrypt(password, 12, salt=salt)
                if data[1] == bcrypt_hash.hex():
                    # successful login
                    return True, "Successful Login!"
                if data[1] != bcrypt_hash.hex():
                    return False, "Incorrect Password!"
    return False, "Invalid Username!"

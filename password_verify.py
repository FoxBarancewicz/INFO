from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import bcrypt
import binascii

#username/pwd passed as input from js?
user = input()
#in the backend, password should be handed from frontend already hashed
#b64pwd = SHA512.new(password.encode()).digest()
pwd = input()

#for testing
b64pwd = SHA512.new(pwd.encode()).digest()

salt = None

# fetches salt from storage file
with open('storage.txt', 'r') as f:
    while True:
        data = f.readline().split(",")
        if data == None:
            break
        if data[0] == user:
            salt = binary_string = binascii.unhexlify(data[2].strip("\n"))\
            bcrypt_hash = bcrypt(b64pwd, 12, salt=salt)
            if data[1] == bcrypt_hash.hex():
                #Success
                print("Logged in!")
            elif data[1] != bcrypt_hash.hex():
                #Bad password
                print("Incorrect password!")
            break 

#invalid username if script gets here
#print("Invalid username")

#salt = get_random_bytes(16)
#b64pwd = SHA512.new(pwd_confirm.encode()).digest()
#bcrypt_hash = bcrypt(b64pwd, 12, salt=salt)
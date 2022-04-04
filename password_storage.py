from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import bcrypt

if __name__ == "__main__":

    username = input("Please enter username: ")
    pwd_first = input("Please enter password: ")
    pwd_confirm = input("Please confirm password: ")
    

    if (pwd_first != pwd_confirm):
        print("Passwords do not match!")
        exit()
    else:
        salt = get_random_bytes(16)
        b64pwd = SHA512.new(pwd_confirm.encode()).digest()
        bcrypt_hash = bcrypt(b64pwd, 12, salt=salt)
 
        with open("storage.csv", "a") as f:
            f.write(("{},{},{}\n").format(username, bcrypt_hash.hex(), salt.hex()))
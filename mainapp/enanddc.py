from cryptography.fernet import Fernet
import logging
import traceback
from myproject.settings import ENCRYPT_KEY


def encrypt(pas):
    try:
        pas = str(pas)
        cipher_pass = Fernet(ENCRYPT_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass=encrypt_pass.decode('ascii')
        print(encrypt_pass,type(encrypt_pass))
        print("encrpytion")
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None



def decrypt(pas):
    try:
        pas=pas.encode('utf-8')
        cipher_pass = Fernet(ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        print("decrpytion",decod_pass,type(decod_pass))
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


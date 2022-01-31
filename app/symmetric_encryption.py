from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


def get_key(pin):
    salt = get_random_bytes(16)
    super_key = PBKDF2(pin.encode('utf-8'), salt)
    return super_key


def encrypt(pin, password):
    aes_key = pad(pin.encode('utf-8'), AES.block_size)
    password = pad(password.encode('utf-8'), AES.block_size)
    aes = AES.new(aes_key, AES.MODE_CBC)
    encrypted_password_bytes = aes.encrypt(password)
    encrypted_password = b64encode(encrypted_password_bytes).decode('utf-8')
    iv = b64encode(aes.iv).decode('utf-8')
    return encrypted_password, iv


def decrypt(pin, iv, encrypted_password):
    try:
        aes_key = pad(pin.encode('utf-8'), AES.block_size)
        iv = b64decode(iv)
        encrypted_password = b64decode(encrypted_password)
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_password = aes.decrypt(encrypted_password)
        decrypted_password = unpad(decrypted_password, AES.block_size)
        return decrypted_password.decode('utf-8')
    except (ValueError, KeyError) as e:
        print(e)
        return "fake"


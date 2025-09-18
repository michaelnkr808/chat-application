HOST = "localhost"
SERVER_HOSTNAME = "localhost"
PORT = 9999
PROMPT = "Welcome to the server. Enter a message to begin chatting! ('quit' to close): \n"
BUF_SIZE = 1024
WELCOME_PREFIX = "Welcome "
CERT_PATH = "/Users/michaelr808/Desktop/Desktop - Michael’s MacBook Pro/projects/python/chat-app/certs/server.crt"
KEY_PATH = "/Users/michaelr808/Desktop/Desktop - Michael’s MacBook Pro/projects/python/chat-app/certs/server.key"


def validate_username(username):
    username = username.strip()
    username = username.lower()
    if(not username):
        raise ValueError("empty")
    if(len(username) > 24):
        raise ValueError("too_long")
    if(not namechars_check(username)):
        raise ValueError("invalid_chars")
    return username
        
def namechars_check(s):
    for char in s:
        if not (char.isalpha() or char.isnumeric()):
            return False
    return True
    
HOST = "localhost"
PORT = 9999
PROMPT = "Enter a message ('quit' to close):"
BUF_SIZE = 1024
WELCOME_PREFIX = "Welcome"


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
        if not char.isalpha():
            return False
    return True
    
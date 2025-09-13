def validate_username(username):
    username = username.strip()
    username = username.lower()
    if(type(username) is not str):
        raise ValueError("Username cannot contain numbers")
    if(not username):
        raise ValueError("Username cannot be empty")
    if(len(username) > 24):
        raise ValueError("Username too long")
    return username
        
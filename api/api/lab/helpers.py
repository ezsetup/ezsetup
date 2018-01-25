import random, string

def randomword(length: int) -> str:
    """Generate a random word"""
    char_pool = string.ascii_letters + string.digits
    return ''.join(random.choice(char_pool) for i in range(length))

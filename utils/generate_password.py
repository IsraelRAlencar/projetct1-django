import secrets
import string
import sys


def generate_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


if __name__ == "__main__":
    try:
        length = int(sys.argv[1])
        random_password = generate_password(length)
        print(random_password)
    except (IndexError, ValueError):
        print("Usage: python generate_password.py <length>")

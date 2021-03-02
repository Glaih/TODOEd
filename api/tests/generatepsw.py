import secrets
import string


def generatepsw():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))


if __name__ == '__main__':
    print(generatepsw())
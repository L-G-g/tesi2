import random
import string
def generate_random_name(length=3):
    """Generate a random name of specified length."""
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


if __name__ == "__main__":
    print(generate_random_name(3))
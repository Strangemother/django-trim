import random
import string


def rand_str(length=6):
    """
    Generate a random string of uppercase letters and digits.

    Creates a random string composed of uppercase ASCII letters (A-Z) and
    digits (0-9). Useful for generating random identifiers, tokens, or
    temporary names.

    Args:
        length (int, optional): The length of the random string to generate.
            Defaults to 6.

    Returns:
        str: A random string of the specified length containing only uppercase
            letters and digits.

    Examples:
        Generate a 6-character random string (default):

            >>> token = rand_str()
            >>> len(token)
            6

        Generate a 12-character random string:

            >>> token = rand_str(12)
            >>> len(token)
            12

        Use for temporary file names:

            >>> filename = f"temp_{rand_str(8)}.txt"
            >>> # Example output: "temp_A7X9K2D1.txt"

    Notes:
        - The function uses `random.choices()` which allows for repeated characters
        - Character pool includes: A-Z (26 letters) and 0-9 (10 digits)
        - For cryptographically secure random strings, use `secrets.token_urlsafe()`
          instead
    """
    choices = random.choices(string.ascii_uppercase + string.digits, k=length)
    return "".join(choices)

from random import sample
from string import ascii_letters, digits
from time import sleep
import subprocess
import os

DEFAULT = "\033[m"
BLACK = "\033[1;30m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PINK = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
INVERT = "\033[1;4;7;97m"
BOLD = "\033[1m"


def is_even(nbr: int) -> bool:
    return nbr % 2 == 0


def clear(init_wait_time: int = 0, final_wait_time: int = 0) -> None:
    """
    Clear the terminal screen with optional delays.

    This function pauses execution for an optional amount of time
    before clearing the terminal, clears the screen using the
    appropriate command for the current operating system, and
    optionally pauses again after clearing.

    :param init_wait_time: Time in seconds to wait before clearing
                           the terminal.
    :type init_wait_time: int
    :param final_wait_time: Time in seconds to wait after clearing
                            the terminal.
    :type final_wait_time: int
    :return: None
    :rtype: None
    """
    cmd = []
    os_name = os.name
    if os_name == "nt":
        cmd.append("cls")
    else:
        cmd.append("clear")
    sleep(float(init_wait_time))
    subprocess.run(cmd)
    sleep(float(final_wait_time))


def gen_chars(amount: int = 10) -> str:
    """
    Generate a random alphanumeric string.

    :param amount: Number of characters to generate.
    :type amount: int
    :return: A random string made of letters and digits.
    :rtype: str
    """
    chars = ascii_letters + digits
    return "".join(sample(chars, amount))


def gen_nbr(amount: int = 2) -> str:
    """
    Generate a random string of digits.

    :param amount: Number of digits to generate.
    :type amount: int
    :return: A random string made of digits only.
    :rtype: str
    """
    return "".join(sample(digits, amount))


def there_is_alpha(text: str) -> bool:
    """
    Check whether a string contains at least one alphabetic character.

    Alphabetic characters are determined using ``str.isalpha()``.

    :param text: The text to be analyzed.
    :type text: str
    :return: True if at least one alphabetic character is found,
             False otherwise.
    :rtype: bool
    """
    for c in text:
        if str(c).isalpha():
            return True
        else:
            pass
    return False


def split_by(text: str, chunk_len: int = 0, chunk: int = 2) -> list[str | int]:
    """
    Split a string into chunks of a fixed size.

    The function iterates through the string and splits it into
    substrings containing ``chunk_len`` characters each.

    :param text: The text to be split.
    :type text: str
    :param chunk_len: Number of characters per chunk.
    :type chunk_len: int
    :param chunk: number of chunks to return.
    :type chunk: int
    :return: A list of substrings split by the specified size.
    :rtype: list
    """
    if chunk_len == 0:
        chunk_len = int(len(text) / chunk)
    cnt = 0
    ret: list[str | int] = []
    i = 0
    e = chunk_len
    while cnt != chunk:
        if text[i:e] == "":
            break
        splited_by = text[i:e]
        i = e
        e += chunk_len
        if there_is_alpha(splited_by):
            ret.append(splited_by)
        else:
            ret.append(int(splited_by))
        cnt += 1
    return ret

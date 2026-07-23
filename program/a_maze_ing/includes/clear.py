from time import sleep
import subprocess
import os


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

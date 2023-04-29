import os
import subprocess


class CommandFailedError(Exception):
    pass


def run_commands(commands: list[str]) -> None:
    command_to_use = "&&".join(commands)
    os.system(command_to_use)

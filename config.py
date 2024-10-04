"""
This module handles configuration management for the embedding service.

It provides functionality to load environment variables, parse command-line arguments,
and create a structured configuration object using Pydantic models.
"""

import argparse
import os
from dotenv import load_dotenv
from embedding.data_models import Config


load_dotenv()

def get_arguments() -> list[str]:
    """
    Define and return a list of configuration arguments.

    Returns:
        list[str]: A list of configuration argument strings.
    """
    return [
        "embedding.port",
        "embedding.host",
        "version",
        "embedding.endpoint",
    ]


def add_env_vars(args: list[str], parser: argparse.ArgumentParser) -> argparse.Namespace:
    """
    Add environment variables as arguments to the parser.

    Args:
        args (list[str]): List of argument strings.
        parser (argparse.ArgumentParser): The argument parser object.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    for arg in args:
        env_label = arg.replace(".", "_").upper() if "." in arg else arg.upper()
        default_value = os.getenv(env_label)
        parser.add_argument(f"--{arg}", type=type(default_value), default=default_value, required=False)
    return parser.parse_args()


def create_nested_config(args: argparse.Namespace) -> dict:
    """
    Create a nested dictionary from parsed arguments.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns:
        dict: A nested dictionary representing the configuration.
    """
    env_dict = {}
    for label, value in args.__dict__.items():
        if "." in label:
            config_object, attribute = label.split(".")
            if config_object not in env_dict:
                env_dict[config_object] = {}
            env_dict[config_object][attribute] = value
        else:
            env_dict[label] = value
    return env_dict


def get_config_dict() -> dict:
    """
    Get the configuration as a dictionary.

    Returns:
        dict: A nested dictionary of the configuration.
    """
    parser = argparse.ArgumentParser()
    args = get_arguments()
    arguments = add_env_vars(args, parser)
    return create_nested_config(arguments)

def get_config() -> Config:
    """
    Create and return a Config object.

    Returns:
        Config: A configured Config object.
    """
    kwargs = get_config_dict()
    config = Config()
    config.update_config(kwargs)
    return config    


if __name__ == "__main__":
    config = get_config()
    print(config.model_dump_json(indent=4))
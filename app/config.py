import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import questionary

from app.settings import get_config_path

config_path = get_config_path()

CHUNK_SIZE = 4096
MB_RATE = 1_000_000
@dataclass
class Config:
    upload_destination: str
    download_destination: str

    def is_valid(self):
        return all(
            Path(getattr(self, attr)).exists() and Path(getattr(self, attr)).is_dir()
            for attr in self.__annotations__
        )
            

def initialize_config() -> Tuple[Path, Path]:
    config_file_path = Path(".filevault_config/config.json")
    config_dir = config_file_path.parent
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    if not config_file_path.exists():
        config_file_path.touch()
    default_config_path = Path("app/config/default_config.json")
    return config_file_path, default_config_path


def validate_input(config_path: str) -> bool:
    try:
        with open(config_path, "r") as config_file:
            data = json.load(config_file)
            config = Config(**data)
            return True if config.is_valid() else False
    except Exception as e:
        return False

def load_config(config_path: str) -> Config:
    with open(config_path, "r") as config_file:
        data = json.load(config_file)
    return Config(**data)

def save_config(config_path: str, config: Config):
    with open(config_path, "w") as config_file:
        config_file.write(json.dumps(config.__dict__, indent=4))

def manual_config(config_path) -> Config:
    config = {
        "upload_destination": questionary.path(
            message="Choose Upload Destination: ",
            only_directories=True
        ),
        "download_destination": questionary.path(
            message="Choose download destination: ",
            only_directories=True
        ),
    }
    
    # Questionary returns None if the user does a Keyboard interrupt, handling gracefully.
    for key, question in config.items():
        path = question.ask()
        if not path:
            print("Cancelled by user, Exiting program...")
            sys.exit(1)
        config[key] = str(Path(path)).replace("'", "")

    cfg = Config(**config)
    if not cfg.is_valid():
        print("Invalid config inputs, please enter correct directories.")
        return manual_config(config_path)
    save_config(config_path, cfg)
    print("Config saved successfully.")
    return cfg

def get_or_create_config(config_path, default_config_path) -> Config:
    if config_path.exists():
        valid = validate_input(config_path)
        if valid:
            return load_config(config_path)
    
    # Prompt for default config or manual config
    try:
        load_default_or_config_manually = questionary.select(
            message="Config file not found or invalid. Would you like to load defaults or configure manually?",
            choices=[
                "Load Defaults",
                "Manual Config"
            ],
            use_arrow_keys=True,
            use_emacs_keys=True,
            use_indicator=True,
            use_shortcuts=True,
            use_jk_keys=True,
        )
        choice = load_default_or_config_manually.ask()
        if choice == "Load Defaults":
            # Load default config and write it to the config.json
            print("Loading default config...")
            default_config = load_config(default_config_path)
            save_config(config_path, default_config)
            return default_config
        elif choice == "Manual Config":
            return manual_config(config_path)
        else:
            print("Invalid choice during configuration, relaunch the app and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("⚠️ Configuration cancelled by user.")
        sys.exit(1)

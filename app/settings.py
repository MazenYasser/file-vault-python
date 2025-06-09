_config = None
_config_path: str = ""

def configure(config, config_path: str):
    global _config, _config_path
    _config = config
    _config_path = config_path

def get_config():
    return _config

def get_config_path() -> str:
    return _config_path
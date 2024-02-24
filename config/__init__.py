from dotenv import dotenv_values
from pathlib import Path


CWD = Path.cwd()

def load(filename=".flaskenv"):
    parent = Path(__file__).parent
    config_path = Path.joinpath(CWD, parent, filename)
    print(f"Loading configuration from {config_path}...")

    if not Path.exists(config_path):
        raise FileNotFoundError(
            "\'.flaskenv\' file not found. Did you forget to create it? Is it in the \'config\' folder?"
        )
    
    print("Configuration loaded.")
    return dotenv_values(config_path)

app_config = load()

from dotenv import dotenv_values
from pathlib import Path


email_config = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 587,
    "MAIL_USERNAME": "csc535barberapp@gmail.com",
    "MAIL_PASSWORD": "ehxh xybx phlp mltp",
    "MAIL_USE_TLS": 1,
    "MAIL_USE_SSL": False
}


CWD = Path.cwd()

def load():
    config_path = Path.joinpath(CWD, ".flaskenv")
    print(f"Loading configuration from {config_path}...")

    if not Path.exists(config_path):
        raise FileNotFoundError(
            "\'.flaskenv\' file not found. Did you forget to create it? Is it in the \'config\' folder?"
        )
    
    print("Configuration loaded.")
    config = dotenv_values(config_path) 
    config.update(email_config)
    return config

app_config = load()

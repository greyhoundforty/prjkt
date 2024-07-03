import os
from pathlib import Path
import yaml
from rich.prompt import Prompt, Confirm
import db

CONFIG_DIR = Path.home() / ".config/prjkt"
CONFIG_FILE = CONFIG_DIR / "config.yml"
DB_FILE = CONFIG_DIR / "projects.db"

def setup_config():
    if CONFIG_FILE.exists():
        print("[yellow]Config file already exists[/yellow]. Edit settings?")
        if Confirm.ask("Edit settings"):
            edit_config()
        else: 
            print("[green]Keeping existing config[/green]")
    else:
        create_config()

def create_config():
    print("[bold]Setting up prjkt config[/bold]")
    
    config_dir = Prompt.ask("Config directory", default=str(CONFIG_DIR))
    db_path = Prompt.ask("DB file path", default=str(DB_FILE), show_default=False) 
    default_tags = Prompt.ask("Default tags (comma separated)")

    config = {
        "PRJKT_CONFIG_DIR": config_dir,
        "PRJKT_DB_FILE": db_path, 
        "DEFAULT_TAGS": default_tags
    }

    os.makedirs(config_dir, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)

    print(f"[green]Config written to {CONFIG_FILE}[/green]")
    print("[bold]Setting up prjkt database[/bold]")
    conn = db.create_connection()
    db.init_db(conn) 
    print(f"[green]Initialized database at {db_path}[/green]")
def edit_config():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    
    # Edit config dict based on user input

    with open(CONFIG_FILE, "w") as f: 
        yaml.dump(config, f)

    print("[green]Updated config[/green]")

def get_config_paths():
    setup_config() 
    return CONFIG_DIR, DB_FILE

if __name__ == '__main__':
    setup_config()


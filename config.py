import os
import yaml
from rich.prompt import Prompt


def setup(config_dir, projects_dir, global_tags):
    """Setup configuration"""
    CONFIG_DIR = config_dir 
    PROJECTS_DIR = projects_dir
    GLOBAL_TAGS = global_tags 
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'prjkt-config.yaml')
    TEMPLATES_DIR = os.path.join(CONFIG_DIR, 'templates')
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(PROJECTS_DIR, exist_ok=True)

    config = {
        'config_dir': CONFIG_DIR,
        'projects_dir': PROJECTS_DIR,
        'global_tags': GLOBAL_TAGS.split()
    }
    config_yaml = yaml.dump(config)

    print(f"Writing prjkt configuration file to {CONFIG_FILE}")
    with open(CONFIG_FILE, 'w') as f:
        f.write(config_yaml)
    
def view():
    """Update configuration"""
    print("View configuration")


def edit():
    """Edit configuration file"""
    print("Editing config file")

if __name__ == '__main__':
    setup()
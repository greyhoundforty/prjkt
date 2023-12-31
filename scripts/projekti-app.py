#!/usr/bin/env python3
import os
import click
import yaml

# used for testing
CONFIG_DIR_DEFAULT = os.path.expanduser('~/tmp/projekti-testing-dir')
#CONFIG_DIR_DEFAULT = os.path.expanduser('~/.config/prjkt')

def check_editor():
    # Checking if EDITOR environment variable is set
    if os.environ.get('EDITOR') is None:
        print("EDITOR is not set.")
        print("You will not be able to add, copy or edit projects.")
        print("Please set EDITOR environment variable to your preferred editor.")

@click.group()
def cli():
    pass

@cli.command()
def init():

    check_editor()
    """Initialize prjkt configuration"""
    
    config_dir = click.prompt('Provide prjkt config directory This should be the full path. If left blank it defaults to ~/.config/prjkt', default=CONFIG_DIR_DEFAULT)
    
    CONFIG_DIR = os.path.expanduser(config_dir)
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yml')
    PROJECTS_DIR = os.path.join(CONFIG_DIR, 'projects')
    TEMPLATES_DIR = os.path.join(CONFIG_DIR, 'templates')
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    
    base_config = {
    'version': '1.0.0',
    'prjkt_config_dir': CONFIG_DIR,
    'prjkt_projects_dir': PROJECTS_DIR,
    'prjkt_templates_dir': TEMPLATES_DIR
    }

    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(base_config, f)

    project_config = {
    'version': 'project_version',
    'prjkt_config_dir': CONFIG_DIR,
    'prjkt_projects_dir': PROJECTS_DIR,
    'prjkt_templates_dir': TEMPLATES_DIR
    }

    with open(os.path.join(TEMPLATES_DIR, 'project-config.yml'), 'w') as f:
        yaml.dump(project_config, f)

    with open(os.path.join(TEMPLATES_DIR, 'start.sh'), 'w') as f:
        f.write("""#!/usr/bin/env bash

    # This script will be invoked when starting the project. This can be used to activate virtualenvs, change in to a directory, etc.
    # Command line arguments can be used, $3 would be the first argument after your project name.

    echo "Starting project"
    """)

    with open(os.path.join(TEMPLATES_DIR, 'stop.sh'), 'w') as f:  
        f.write("""#!/usr/bin/env bash

    # This script will be invoked when stopping the project
    # Add any start logic here

    echo "Stopping project"
    """)
    click.echo("prjkt initialized!")

# Other commands...

if __name__ == '__main__':
    cli()


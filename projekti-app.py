import os
import click
import yaml

CONFIG_DIR = os.path.expanduser('~/.config/prjkt')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yml')
PROJECTS_DIR = os.path.join(CONFIG_DIR, 'projects')
TEMPLATES_DIR = os.path.join(CONFIG_DIR, 'templates')

@click.group()
def cli():
    pass

@cli.command()
@cli.command()
def init():
    """Initialize prjkt configuration"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # Create default config
    default_config = {'projects_dir': PROJECTS_DIR}
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(default_config, f)

    # Create template files
    with open(os.path.join(TEMPLATES_DIR, 'project-config-template.yml'), 'w') as f:
        f.write("""# This is a template for project configuration
    version: 1.0.0
    base_dir: ~/.config/prjkt
    projects_dir: ~/.config/prjkt/projects
    templates_dir: ~/.config/prjkt/templates

    default_template: base

    cli:
    colors: true
    output: text   # 'text' or 'json'

    # Command to use for running scripts
    run_command: bash 
    """)

    with open(os.path.join(TEMPLATES_DIR, 'start.sh'), 'w') as f:
        f.write("""#!/usr/bin/env bash

    # This script will be invoked when starting the project
    # Add any start logic here

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


import click
import os
import yaml
import utils
from rich.syntax import Syntax
from rich.console import Console
from rich.prompt import Prompt

CONFIG_DIR_DEFAULT = os.path.expanduser('~/.config/prjkt')

@click.group()
def cli():
    pass


@cli.group()
def config():
    """Configure settings"""
    pass


@config.command()
def edit():
    """Edit configuration file"""
    click.echo("Editing config file")


@config.command()
def setup():
    """Setup configuration"""
    click.echo("Setting up configuration")
    
    default_config_dir = os.path.expanduser('~/.config/prjkt')
    default_projects_dir = os.path.join(default_config_dir, 'projects')
    
    CONFIG_DIR = Prompt.ask("Enter the path to store prjkt configs", default=default_config_dir)
    PROJECTS_DIR = Prompt.ask("Enter the path to store project files", default=default_projects_dir)
    GLOBAL_TAGS = Prompt.ask("Enter global tags", default="")
    
    utils.setup(CONFIG_DIR, PROJECTS_DIR, GLOBAL_TAGS)  

@config.command() 
def update():
    """Update configuration"""
    click.echo("Updating configuration")


@cli.group()
def define():
    """Define projects and templates"""
    pass


@define.command()
@click.option("-n", "--name", required=True, help="Name of project")
@click.option("-l", "--language", help="Language of project")
def project(name, language):
    """Define a new project"""
    project_dir = os.path.join(CONFIG_DIR, 'projects', name)
    click.echo(f"Defining new project {name} in {language}")
    write_gitginore = utils.get_gitignore(language, project_dir)


@define.command() 
def template():
    """Define a template"""
    click.echo("Defining a new template")


@cli.group()
def list():
    """List saved projects and templates"""
    pass


@list.command() 
def project():
    """List saved projects"""
    click.echo("Listing projects")

@list.command()
def template():
    """List saved templates"""
    click.echo("Listing templates")

@cli.group()
def update():
    """Update existing project or template"""
    pass

@update.command()
def project():
    """Update project"""
    click.echo("Updating project")

@update.command()
def template():
    """Update template""" 
    click.echo("Updating template")

@cli.group()
def view():
    """View details of project or template"""
    pass

@view.command()
def project():
    """View project details"""
    click.echo("Viewing project")

@view.command() 
def template():
    """View template details"""
    click.echo("Viewing template")


if __name__ == "__main__":
    cli()

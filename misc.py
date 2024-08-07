
CONFIG_DIR_DEFAULT = os.path.expanduser('~/.config/prjkt')

def check_editor():
    # Checking if EDITOR environment variable is set
    if os.environ.get('EDITOR') is None:
        print("EDITOR is not set.")
        print("Although `prjkt` is initialized, you will not be able to add, copy or edit projects. Please set EDITOR environment variable to your preferred editor.")

@click.group()
def cli():
    pass

@click.command()
@click.option('-c', '--config-dir', default=CONFIG_DIR_DEFAULT, help='Set a custom location for the prjkt config directory, default is ~/.config/prjkt if not set', required=False)
def init(config_dir):

    
    """Initialize prjkt configuration"""
    
    config_dir = click.prompt('Provide prjkt config directory This should be the full path. If left blank it defaults to ~/.config/prjkt', default=config_dir)
   
    CONFIG_DIR = os.path.expanduser(config_dir)
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'prjkt-config.json')
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

    with open(os.path.join(CONFIG_DIR, CONFIG_FILE), 'w') as f:
        json.dump(base_config, f, indent=4)


    # with open(CONFIG_FILE, 'w') as f:
    #     yaml.dump(base_config, f)
    
    click.echo("prjkt initialized!")
    check_editor()

cli.add_command(init)

@click.command()
@click.option('-n', '--project-name', help='The name of the project you want to define', required=True)
@click.option('-v', '--version', help='The version of the project you want to define. Defaults to "0.0.1"', required=False, default='0.0.1')
@click.option('-t', '--tags', required=False, help='Tags for the project, comma separated', default = [])
@click.option('-m', '--metadata', required=False, is_flag=True, help='Add metadata to project-config.json. This collects the OS, python version, and project creation time.' )
def define_project(project_name, version, tags, metadata):
    """Define a new project
    
    Args:
        project_name (str): The name of the project.

        version (str): The version of the project. Defaults to "0.0.1".
        
        tags (str): Tags for the project, comma separated.
        
        metadata (bool): Add metadata to project-config.json. This collects the OS, python version, and project creation time.
    """
    # Convert project_name to lowercase and replace spaces with hyphens
    project_name = project_name.lower().replace(' ', '-')
    
    CONFIG_DIR = CONFIG_DIR_DEFAULT
    PROJECT_DIR = os.path.join(CONFIG_DIR, 'projects', project_name)
    if os.path.exists(PROJECT_DIR):
        raise Exception(f"Project '{project_name}' already exists. Please choose another name.")

    os.makedirs(PROJECT_DIR, exist_ok=True)
    # Split tags string into a list
    tags = tags.split(',')
    
    base_config = {
        'project_name': project_name,
        'version': version,
        'project_tags': tags
    }
    
    # If --metadata flag is supplied, add metadata to base_config
    if metadata:
        base_config['metadata'] = {
            'os': os.name,
            'python_version': platform.python_version(),
            'config_written_at': datetime.datetime.now().isoformat()
        }
    console = Console()
    console.print(JSON(base_config))

    with open(os.path.join(PROJECT_DIR, 'project-config.json'), 'w') as f:
        json.dump(base_config, f, indent=4)

    console.print(":building_construction: Project has been defined!")

    with open(os.path.join(PROJECT_DIR, 'start.sh'), 'w') as f:
        f.write("""#!/usr/bin/env bash
                
# This script will be invoked when starting the project. This can be used to activate virtualenvs, change in to a directory, run tfswitch, etc. Command line arguments can be used, $3 would be the first argument after your project name.

echo "Starting project"
if ${3}; then
    echo "Command override: $3 provided"
else
    echo "No command override provided"
fi

    """)
    os.chmod(os.path.join(PROJECT_DIR, 'start.sh'), stat.S_IXUSR)

    with open(os.path.join(PROJECT_DIR, 'stop.sh'), 'w') as f:  
        f.write("""#!/usr/bin/env bash

# This script will be invoked when stopping the project
# Add any start logic here

echo "Stopping project"
    """)

    os.chmod(os.path.join(PROJECT_DIR, 'stop.sh'), stat.S_IXUSR)

cli.add_command(define_project)

@click.command()
@click.option('-n', '--project-name', help='The name of the project you want to define', required=True)
@click.option('--start-override', help='Optional string to be passed to the start script and exposed as $3. Useful for targeting subfunctions in a project.', required=False)
def start_project(project_name, start_override):
    """Start a project"""
    CONFIG_DIR = CONFIG_DIR_DEFAULT
    PROJECT_DIR = os.path.join(CONFIG_DIR, 'projects', project_name)
    start_script = os.path.join(PROJECT_DIR, 'start.sh')
    
    # Ensure start_override is a string and properly escaped
    start_override = shlex.quote(str(start_override)) if start_override else ''
    
    os.system(f'{start_script} {start_override}')

cli.add_command(start_project)

@click.command(help='List all projects')
def list_projects():
    CONFIG_DIR = CONFIG_DIR_DEFAULT
    PROJECTS_DIR = os.path.join(CONFIG_DIR, 'projects')
    projects = os.listdir(PROJECTS_DIR)

    # Create a new Table object
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Project Name")
    table.add_column("Version")
    table.add_column("Tags")

    # For each project, load the projects-config.yaml file and get the project name, version, and tags
    for project in projects:
        with open(os.path.join(PROJECTS_DIR, project, 'project-config.json')) as f:
            project_config = json.load(f)
            project_name = project_config['project_name']
            project_version = project_config['version']
            project_tags = ', '.join(project_config['project_tags'])
            table.add_row(project_name, project_version, project_tags)

    # Print the table
    console = Console()
    console.print(table)

cli.add_command(list_projects)


if __name__ == '__main__':
    cli()


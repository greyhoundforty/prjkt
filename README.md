#  projekti

A [prm](https://github.com/EivindArvesen/prm) like utility but built in python. This is mainly a learning project for me, but if you find it usefull, please feel free to use it. If you hit a bug or have a feature request, please open an issue. I am not a developer by trade, so I am sure there are many things that could be done better.

## TLDR

`prjkt` is a utility to help manage multiple projects. It allows you to define a project and its start/stop scripts. It also allows you to define project templates that can be used to create new projects.

## Prjkt commands

These are the planned commands for the `prjkt` utility.

### define { project | template }

Use the `prjkt define` command to define/create a new ==project== or ==template==. This will create a new directory/files in the appropriate **prjkt** path 

#### project

```bash
--project / -p PROJECT_NAME FLAGS
```

Use the command `prjkt define --project --name PROJECT-NAME` to create a new project. This will create a new directory in the `~/.config/prjkt/projects/PROJECT-NAME` directory, add a default project configuration file and create project `start.sh` and `stop.sh` files in the new directory. These files will be used to `activate` and `deactivate` the project.

##### project flags

- `--name / -n` : The name of the project. This is required and will be used to create the project directory and files. If the name contains spaces, it should be quoted.
- `--base / -b`: base directory to place project files. This is optional and requires the full path. The default for new projects will be to put them in `~/.config/prjkt/projects/CONVERTED-PROJECT-NAME`
- `--tags`: key value pairs that will be added to the projects YAML config file. These tags will be used in the `list` sub command as well. 
- `--from-template`: instead of starting with the base start.sh / stop.sh populate new project dir with the files in named template directory. Syntax would be `--from-template TEMPLATE-NAME`

#### template

Use the `prjkt define --template --name TEMPLATE-NAME` to create a new template. This will create a new directory in the `~/.config/prjkt/templates/TEMPLATE-NAME` directory. 

```bash
--template / -p TEMPLATE_NAME FLAGS
```

##### template flags

- `--name / -n` : the name of the project
- `--base / -b`: base directory to place project files. This is optional and requires the full path. The default for new projects will be to put them in `~/.config/prjkt/templates/CONVERTED-TEMPLATE-NAME`
- `--copy-from`: the name of an existing template to use as the base for the new template files. 

### list

#### projects

List existing projects. This will list all projects in the `~/.config/prjkt/projects` directory. 

```bash
list --projects FLAGS
```

##### list projects flags

- `--tag / -t` : (optional) only display projects with the tag defined in its base YAML. 
- `--json / -j`: output the list of projects in JSON format matching this template:   

```json
{
  "project_name": project-name,
  "project_directory": project-base,
  "project_tags": [project-tags]
  "from_template": boolean
}
```

#### templates

List project templates. This will list all templates in the `~/.config/prjkt/templates` directory. 

```bash
list --templates FLAGS
```

##### list templates flags

- `--tag / -t` : (optional) only display templates with the tag defined in its base YAML.
- `--json / -j`: output the list of templates in JSON format

```json
{
  "template_name": template-name,
  "template_directory": template-base,
  "template_tags": [project-tags]
  "from_template": boolean
}
```

### start { project }

Activate a defined project. This will change in once projects base directory and invoke its start.sh file. 

### stop { project }

Deactivate a defined project. This will invoke its stop.sh file and then return the user to their home directory(or maybe previous directory before starting the project) 

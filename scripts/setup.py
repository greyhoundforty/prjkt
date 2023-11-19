"""Setup prjkt CLI configuration."""
# :license: MIT, see LICENSE for more details.

import configparser
import json
import os.path

CONFIG_DIR = os.path.expanduser('~/.config/prjkt')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yml')
PROJECTS_DIR = os.path.join(CONFIG_DIR, 'projects')
TEMPLATES_DIR = os.path.join(CONFIG_DIR, 'templates')

def main(env, config):
    # Ask for base directory to store prjkt config files
    base_dir = env.input('Base directory to store project files', default=defaults['~/.config/prjkt'] or '~/.prjkt')
    default_tags = defaults['prjkt']

    path = 'CONFIG_DIR/CONFIG_FILE'
    if env.config_file:
        path = env.config_file
    config_path = os.path.expanduser(path)

    env.out(env.fmt(config.config_table({'base_dir': base_dir,
                                         'default_tags': default_tags})))

    if not formatting.confirm('Are you sure you want to write settings to "%s"?' % config_path, default=True):
        raise exceptions.CLIAbort('Aborted.')

    parsed_config = configparser.RawConfigParser()
    parsed_config.read(config_path)
    try:
        parsed_config.add_section('softlayer')
    except configparser.DuplicateSectionError:
        pass

    parsed_config.set('prjkt', 'base_dir', base_dir)
    parsed_config.set('prjkt', 'default_tags', default_tags)

    config_fd = os.fdopen(os.open(config_path, (os.O_WRONLY | os.O_CREAT | os.O_TRUNC), 0o600), 'w')
    try:
        parsed_config.write(config_fd)
    finally:
        config_fd.close()

    env.fout("Configuration Updated Successfully")

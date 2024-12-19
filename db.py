#!/usr/bin/env python3

# Author: Ryan Tiffany
# Copyright (c) 2024
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import json
import logging
import sqlite3
import setup

config_dir, db_file = setup.get_config_paths()

DB_FILE = db_file

def create_connection():
    """Connect to the SQLite database file"""
    conn = sqlite3.connect(DB_FILE) 
    return conn

def init_db(conn, table_name='projects'):
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            language TEXT, 
            version TEXT,
            active INTEGER DEFAULT 0
        )
    ''')

def create_project(conn, name, path, language, version):
    """Add a new project to the database"""
    c = conn.cursor()
    c.execute("INSERT INTO projects (name, path) VALUES (?, ?)", (name, path))
    conn.commit()
    return c.lastrowid
    
def get_projects(conn):
    """Get all projects in the database"""
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    return c.fetchall()
    
def activate_project(conn, proj_id):
    """Activate a project by ID"""
    c = conn.cursor()
    c.execute("UPDATE projects SET active=1 WHERE id=?", (proj_id,))
    conn.commit()


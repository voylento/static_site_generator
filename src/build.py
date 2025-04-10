import sys
import os
import shutil
from pathlib import Path

from src.converters import generate_pages

def validate_dirs(source_dir, dest_dir):
    if not source_dir.exists():
        raise FileNotFoundError(f"Error: {source_dir} does not exist")
    elif not source_dir.is_dir():
        raise NotADirectoryError(f"Error: {source_dir} is not a directory")

    if dest_dir.exists():
        if not dest_dir.is_dir():
            raise NotADirectoryError(f"Error: {dest_dir} exists but is not a directory")

def create_dest(dest_dir):
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    Path.mkdir(dest_dir)

def create_build_path(build_path):
    build_path = Path(build_path)
    create_dest(build_path)

def copy_static_files(source_dir, dest_dir):
    source_dir, dest_dir = Path(source_dir), Path(dest_dir)

    for entry in source_dir.iterdir():
        if entry.is_dir():
            new_sub_dir = dest_dir.joinpath(entry.name)
            new_sub_dir.mkdir(exist_ok=True)
            copy_static_files(entry, new_sub_dir)
        else:
            dest_dir_copy = dest_dir
            dest_dir_copy.joinpath(entry.name)
            shutil.copy(entry, dest_dir_copy)

def generate_html_files(content_path, template, dest_path):
    generate_pages(content_path, template, dest_path)

    


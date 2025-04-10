import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # Add project root to path

from src.converters import (
        generate_pages,
    )
from src.build import (
        create_build_path,
        copy_static_files,
        generate_html_files,
    )

def copy_static_content(static_path, dest_path):
    static_path = "./static"
    dest_path = "./public"

    create_public(static_path, dest_path)

def main():
    static_path= "./static"
    content_path = "./content"
    build_path = "./public"
    template_file = "./template.html"

    create_build_path(build_path)
    copy_static_files(static_path, build_path)
    generate_html_files(content_path, template_file, build_path)

if __name__=="__main__":
    main()

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

def main(base_path):
    static_path = "./static"
    content_path = "./content"
    build_path = "./docs"
    template_file = "./template.html"

    if not base_path:
        base_path = "/"

    create_build_path(build_path)
    copy_static_files(static_path, build_path)
    generate_html_files(base_path, content_path, template_file, build_path)

if __name__=="__main__":
    main(sys.argv[1])

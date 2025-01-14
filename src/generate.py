from os.path import exists, isfile, join, dirname, splitext
from os import listdir, mkdir, makedirs
from shutil import rmtree, copy
from block_helpers import markdown_to_html_node


def copy_static(source, destination):
    if exists(destination):
        rmtree(destination)
    mkdir(destination)
    if isfile(source):
        copy(source, destination)
    else:
        contents = listdir(source)
        for item in contents:
            source_item, dest_item = join(source, item), join(destination, item)
            if isfile(source_item):
                copy(source_item, dest_item)
            else:
                copy_static(source_item, dest_item)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError("Document must have a top level heading")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown = md_file.read()
    with open(template_path) as tmpl_file:
        template = tmpl_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if not exists(dest_path):
        makedirs(dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


def generate_pages_recursive(content_path, template_path, dest_path):
    for item in listdir(content_path):
        content_item_path = join(content_path, item)

        if isfile(content_item_path):
            generate_page(
                content_item_path,
                template_path,
                join(dest_path, f"{splitext(item)[0]}.html"),
            )
        else:
            generate_pages_recursive(
                content_item_path, template_path, join(dest_path, item)
            )

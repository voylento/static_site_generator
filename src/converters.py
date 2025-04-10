import sys
import os
import shutil
from pathlib import Path
import re

from src.blocks import (
        BlockType,
    )
from src.htmlnode import (
        ParentNode,
        LeafNode,
    )
from src.textnode import (
        TextType,
        TextNode,
    )

heading_regex = r"^#{1,6} .+"
code_regex = r"^`{3}.+`{3}"
quote_regex = r"^>.+"
unordered_list_regex = r"^- .+"
ordered_list_regex = r"^1\. .+"

md_image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
md_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

############################################################
## Private Helper functions
############################################################

def get_indexes(text, delimiter):
    indexes = []
    length = len(delimiter)
    start = 0
    while True:
        index = text.find(delimiter, start)
        if index == -1:
            break
        indexes.append(index)
        start = index + length 

    return indexes

def is_multiline_code_block(lines):
    cnt = len(lines)
    cbd = "```"
    if lines[0][0:3] == cbd and lines[cnt-1][-3:] == cbd:
        return True
    return False

def code_block_to_html(lines):
    code_lines = lines[1:-1]
    code = "\n".join(code_lines)
    return ParentNode("pre", [LeafNode("code", code)])

def is_multiline_quote_block(lines):
    for line in lines:
        if line[0] != '>':
            return False
    return True

def quote_block_to_html(lines):
    result = ""
    for line in lines:
        text = line.lstrip('>').strip()
        if not text:
            text = "\n"
        result += text

    text_nodes = text_to_textnodes(result)
    html_nodes = text_nodes_to_html(text_nodes)
    return ParentNode("blockquote", html_nodes) 

def is_multiline_unordered_list_block(lines):
    for line in lines:
        if line[0:2] != "- ":
            return False
    return True

def unordered_list_to_html(lines):
    list_items = []
    for line in lines:
        list_item_text = line.lstrip("- ")
        text_nodes = text_to_textnodes(list_item_text)
        html_nodes = text_nodes_to_html(text_nodes)
        list_item_node = ParentNode("li", html_nodes)
        list_items.append(list_item_node)

    unordered_list = ParentNode("ul", list_items)
    return unordered_list

def is_multiline_ordered_list_block(lines):
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        prefix_length = len(prefix)
        if line[0:prefix_length] != prefix: 
            return False
    return True

def ordered_list_to_html(lines):
    list_items = []
    stripped_items = [re.sub(r'^\d+\.\s+', '', line) for line in lines]
    for item in stripped_items:
        text_nodes = text_to_textnodes(item)
        html_nodes = text_nodes_to_html(text_nodes)
        node = ParentNode("li", html_nodes)
        list_items.append(node)

    ordered_list = ParentNode("ol", list_items)
    return ordered_list

def split_image_link_node(node, regex_str, text_type):
    result = []
    node_str = node.text

    matches = list(re.finditer(regex_str, node_str))
    if not matches:
        return [node]
    
    current_pos = 0
    node_str_len = len(node_str)
    for match in matches:
        start_pos = match.start()
        end_pos = match.end()
        # If the match's starting position is after current position,
        # there is some regular text to put in a text node
        if current_pos < start_pos:
            txt_node = TextNode(node_str[current_pos:start_pos], TextType.TEXT)
            result.append(txt_node)

        # Now create the TextNode of type specified in argument with the regex match
        result.append(TextNode(match.group(1), text_type, url=match.group(2)))
        current_pos = end_pos

    # If there is text after the  last image match, put it into a TextNode of type TEXT
    if current_pos < node_str_len:
        result.append(TextNode(node_str[current_pos:node_str_len], TextType.TEXT))
    
    return result

################################################################
#               Public functions
################################################################

def split_node_text(text, delimiter, text_type):
    result = []
    if len(text) == 0:
        return []
    indexes = get_indexes(text, delimiter) 
    if len(indexes) == 0:
        return [TextNode(text, TextType.TEXT)]
    elif len(indexes) % 2 != 0:
        raise Exception(f"Error: non closing {delimiter} in string")
    cnt = len(delimiter)
    before = text[0:indexes[0]]
    inside = text[indexes[0]+cnt:indexes[1]]
    after = text[indexes[1]+cnt:]
    if before != '':
        result.append(TextNode(before, TextType.TEXT))
    if inside != '':
        result.append(TextNode(inside, text_type))
    result.extend(split_node_text(after, delimiter, text_type))
    return result

def text_nodes_to_html(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            props = {
                "src": text_node.url,
                "alt": text_node.text,
                }
            return LeafNode("img", "", props)
        case _:
            raise Exception(f"Invalid TextType: {text_node.text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_image_nodes(nodes)
    nodes = split_link_nodes(nodes)
    return nodes

def split_image_nodes(nodes):
    result = []

    for node in nodes:
        node_result_list = split_image_link_node(node, md_image_regex, TextType.IMAGE)
        result.extend(node_result_list)

    return result

def split_link_nodes(nodes):
    result = []

    for node in nodes:
        node_result = split_image_link_node(node, md_link_regex, TextType.LINK)
        result.extend(node_result)

    return result

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """ for now, assume old nodes are of type TextType:TEXT """
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # only dealing with splitting TEXT nodes now
            result.append(node)
            continue
        result.extend(split_node_text(node.text, delimiter, text_type))

    return result

def block_to_block_type(block_text):
    # Input is a block of text as created by markdown_to_blocks
    lines = block_text.split("\n")
    if len(lines) == 1:
        if re.search(heading_regex, block_text):
            return BlockType.HEADING
        if re.search(code_regex, block_text):
            return BlockType.CODE
        if re.search(quote_regex, block_text):
            return BlockType.QUOTE
        if re.search(unordered_list_regex, block_text):
            return BlockType.UNORDERED_LIST
        if re.search(ordered_list_regex, block_text):
            return BlockType.ORDERED_LIST
        
        return  BlockType.PARAGRAPH

    # Multi line case
    if is_multiline_code_block(lines):
        return BlockType.CODE
    if is_multiline_quote_block(lines):
        return BlockType.QUOTE
    if is_multiline_unordered_list_block(lines):
        return BlockType.UNORDERED_LIST
    if is_multiline_ordered_list_block(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    #blocks = [part_stripped for part in markdown.split("\n\n") if (part_stripped := part.strip())]
    return filtered_blocks

def paragraph_block_to_html(markdown):
    split_markdown = markdown.split("\n")
    text_nodes = []
    for p in split_markdown:
        text_nodes.extend(text_to_textnodes(p))
    html_nodes = text_nodes_to_html(text_nodes)
    parent_node = ParentNode("p", html_nodes)
    return parent_node

def heading_block_to_html(markdown):
    # 1. Count number of # at beginning of md string
    # 2. Strip # at beginning of string
    # 3. Create header based on number of #
    match = re.match(r'^(#+)', markdown)
    heading_level = len(match.group(1)) if match else 0
    if heading_level == 0:
        raise Exception("Invalid markdown heading block") 
    header_text = markdown.lstrip("#").strip()
    header_tag = f"h{heading_level}"
    return LeafNode(header_tag, header_text)

def markdown_to_html(markdown):
    child_elements = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match (block_type):
            case BlockType.PARAGRAPH:
                paragraph = paragraph_block_to_html(block.replace("\n", " "))
                child_elements.append(paragraph)
            case BlockType.HEADING:
                header = heading_block_to_html(block)
                child_elements.append(header)
            case BlockType.CODE:
                code = code_block_to_html(block.split("\n"))
                child_elements.append(code)
            case BlockType.QUOTE:
                lines = block.split("\n")
                quote = quote_block_to_html(lines)
                child_elements.append(quote)
            case BlockType.UNORDERED_LIST:
                ul = unordered_list_to_html(block.split("\n"))
                child_elements.append(ul)
            case BlockType.ORDERED_LIST:
                ol = ordered_list_to_html(block.split("\n"))
                child_elements.append(ol)
            case _:
                raise Exception("Unrecognized BlockType. Cannot convert markdown to html node")

    root_node = ParentNode("div", child_elements)
    return root_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    title = None

    for block in blocks:
        match = re.match(r'^#\s*([^#]+)', block)
        if match:
            title = match.group(1).strip()
            break

    if not title:
        raise Exception("missing title h1 element")

    return title

def save_generated_html(html, file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_page(from_path, template):
    print(f"generate page from {from_path} using {template}")

    with open(from_path, 'r') as md_file:
        markdown = md_file.read()

    with open(template, 'r') as template_file:
        templ = template_file.read()

    html_node = markdown_to_html(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    templ = templ.replace("{{ Title }}", title)
    templ = templ.replace("{{ Content }}", html)

    return templ

def generate_pages(content_path, template_path, dest_path):
    content_path, dest_path = Path(content_path), Path(dest_path)

    for entry in content_path.iterdir():
        if entry.is_dir():
            new_sub_path = dest_path.joinpath(entry.name)
            new_sub_path.mkdir(exist_ok=True)
            generate_pages(entry, template_path, new_sub_path)
        else:
            dest_filename = entry.name.replace(".md", ".html")
            dest_path_copy = dest_path
            html = generate_page(entry, template_path)
            save_generated_html(html, dest_path_copy.joinpath(dest_filename))


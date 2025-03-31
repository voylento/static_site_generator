import re
from .htmlnode import HtmlNode, ParentNode, LeafNode
from .textnode import TextNode, TextType

md_image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
md_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

################################################################
#               Private helper functions
################################################################

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

################################################################
#               Public functions
################################################################

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

def markdown_to_blocks(markdown):
    blocks = [part.strip() for part in markdown.split("\n\n")]
    return blocks

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            props = {
                "href": text_node.url,
                }
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {
                "src": text_node.url,
                "alt": text_node.text,
                }
            return LeafNode("img", "", props)
        case _:
            raise Exception("Invalid TextType")


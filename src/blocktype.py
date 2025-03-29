from enum import Enum
import re

heading_regex = r"^#{1,6} .+"
code_regex = r"^`{3}.+`{3}"
quote_regex = r"^>.+"
unordered_list_regex = r"^- .+"
ordered_list_regex = r"^1\. .+"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

def block_to_block_type(text):
    if re.search(heading_regex, text):
        return BlockType.HEADING

    lines = text.split("\n")
    if len(lines) == 1:
        if re.search(heading_regex, text):
            return BlockType.HEADING
        if re.search(code_regex, text):
            return BlockType.CODE
        if re.search(quote_regex, text):
            return BlockType.QUOTE
        if re.search(unordered_list_regex, text):
            return BlockType.UNORDERED_LIST
        if re.search(ordered_list_regex, text):
            return BlockType.ORDERED_LIST
        
        return  BlockType.PARAGRAPH

    # Multi line case
    if is_multi_line_code_block(lines):
        return BlockType.CODE
    if is_multi_line_quote_block(lines):
        return BlockType.QUOTE
    if is_multi_line_unordered_list_block(lines):
        return BlockType.UNORDERED_LIST
    if is_multi_line_ordered_list_block(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def is_multi_line_code_block(lines):
    cnt = len(lines)
    cbd = "```"
    if lines[0][0:3] == cbd and lines[cnt-1][-3:] == cbd:
        return True
    return False

def is_multi_line_quote_block(lines):
    for line in lines:
        if line[0] != '>':
            return False
    return True

def is_multi_line_unordered_list_block(lines):
    for line in lines:
        if line[0:2] != "- ":
            return False
    return True

def is_multi_line_ordered_list_block(lines):
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        prefix_length = len(prefix)
        if line[0:prefix_length] != prefix: 
            return False
    return True

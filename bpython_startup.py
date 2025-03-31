# Make sure project root is in the Python path
import sys
import os

from src.blocktype import BlockType, BlockNode, block_to_block_type
from src.textnode import TextType, TextNode
from src.htmlnode import HtmlNode, ParentNode, LeafNode
from src.utilities import split_nodes_delimiter, markdown_to_blocks, text_node_to_html_node
btbt = block_to_block_type
mdb = markdown_to_blocks
tnhn = text_node_to_html_node


md_text_1 = """
This is a **bolded** paragraph
Test in a p
tag here

This is another paragraph with _italic_text and `code`
"""

blocks = markdown_to_blocks(md_text_1)

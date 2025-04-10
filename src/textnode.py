from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        return (
            self.text_type == obj.text_type
            and self.text == obj.text
            and self.url == obj.url
        )

    def __repr__(self):
        str_repr = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return str_repr

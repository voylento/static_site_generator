from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        if self.text != obj.txt:
            return False
        if self.text_type != obj.text_type:
            return False
        if self.url != obj.url:
            return False
        return True

    def __repr__(self):
        str_repr = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return str_repr

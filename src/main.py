from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

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

def main():
    node = TextNode("foo bar baz", TextType.BOLD, "https://www.voylento.com") 
    print(f"{str(node)}")

if __name__=="__main__":
    main()

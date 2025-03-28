import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Image with URL", TextType.IMAGE, "https://example.com/image.jpg")
        node2 = TextNode("Image with URL", TextType.IMAGE, "https://example.com/image.jpg")

    def test_text_not_eq(self):
        node = TextNode("I am a little teapot", TextType.BOLD)
        node2 = TextNode("Short and stout", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("Testity test test", TextType.ITALIC)
        node2 = TextNode("Testity test test", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("Living on the severed floor", TextType.IMAGE, "https://example.com")
        node2 = TextNode("Living on the severed floort", TextType.IMAGE, "https://example.net")
        self.assertNotEqual(node, node2)

    def test_image_node_to_html(self):
        node = TextNode("alt text", TextType.IMAGE, "img.jpg")
        html_node = text_node_to_html_node(node)
        expected_html = (
            '<img src="img.jpg" alt="alt text"></img>'
            )
        actual_html = html_node.to_html()
        self.assertEqual(actual_html, expected_html)

    def test_text_node_to_html(self):
        node = TextNode("I am a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        expected_html = (
            'I am a text node'
            )
        actual_html = html_node.to_html()

        self.assertEqual(actual_html, expected_html)

    def text_bold_node_to_html(self):
        node = TextNode("I am bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected_html = (
            '<b>I am bold text</b>'
            )
        actual_html = html_node.to_html()

        self.assertEqual(actual_html, expected_html)

    def text_italic_node_to_html(self):
        node = TextNode("I am italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        expected_html = (
            '<b>I am italic text</b>'
            )
        actual_html = html_node.to_html()

        self.assertEqual(actual_html, expected_html)

    def text_code_node_to_html(self):
        node = TextNode("I am a code element", TextType.CODE)
        html_node = text_node_to_html_node(node)
        expected_html = (
            '<code>I am a code element</code>'
            )
        actual_html = html_node.to_html()

        self.assertEqual(actual_html, expected_html)

    def text_link_node_to_html(self):
        node = TextNode("I am an anchor tag", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        expected_html = (
            '<a href="https://www.google.com">I am an anchor tag</a>'
            )
        actual_html = html_node.to_html()

        self.assertEqual(actual_html, expected_html)

if __name__=="__main__":
    unittest.main()

import unittest
import textwrap

from textnode import TextNode, TextType
from utilities import split_nodes_delimiter, split_image_nodes, split_link_nodes, text_to_textnodes, markdown_to_blocks

class TestUtilities(unittest.TestCase):
    def test_no_nodes(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertTrue(result == [])

    def test_bold_no_delimiters(self):
        node = TextNode("Test convert bold with no bold results single text node", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue(len(result) == 1)
        self.assertEqual(result[0].text, "Test convert bold with no bold results single text node")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_single_bold_node_mixed(self):
        node = TextNode("**bold** normal **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue(len(result) == 3)
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[0].text, "bold")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, " normal ")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "bold")

    def test_double_bold_node_mixed(self):
        node = TextNode("**bold** normal", TextType.TEXT)
        node2 = TextNode("normal **bold text** ", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertTrue(len(result) == 5)
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[0].text, "bold")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, " normal")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "normal ")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "bold text")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, " ")

    def test_code_node(self):
        node = TextNode("`assert(1 == 2)` # code", TextType.TEXT)
        node2 = TextNode("code here: `result = []`", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertTrue(len(result) == 4)
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[0].text, "assert(1 == 2)")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, " # code")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "code here: ")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[3].text, "result = []")

    def test_italic_node(self):
        node = TextNode("_This_ is italic _text stuff_ and it should _work_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertTrue(len(result) == 5)
        self.assertEqual(result[0].text_type, TextType.ITALIC)
        self.assertEqual(result[0].text, "This")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, " is italic ")
        self.assertEqual(result[2].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "text stuff")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, " and it should ")
        self.assertEqual(result[4].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, "work")

    def test_extract_md_images_no_match(self):
        node = TextNode("text text text, no markdown images", TextType.TEXT)
        results = split_image_nodes([node])
        self.assertTrue(len(results) == 1)
        node = results[0]
        self.assertEqual(node.text, "text text text, no markdown images")
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_extract_md_image_one_node(self):
        node = TextNode("text text text ![alt text](img.webp) text after", TextType.TEXT)
        results = split_image_nodes([node])
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].text, "text text text ")
        self.assertEqual(results[0].text_type, TextType.TEXT)
        self.assertEqual(results[1].text, "alt text")
        self.assertEqual(results[1].url, "img.webp")
        self.assertEqual(results[1].text_type, TextType.IMAGE)
        self.assertEqual(results[2].text, " text after")
        self.assertEqual(results[2].text_type, TextType.TEXT)

    def test_extrat_md_image_two_nodes(self):
        node = TextNode("text text text ![alt text](img.webp)", TextType.TEXT)
        node2 = TextNode("![alt text](https://voylento.com/images/img.jpeg)", TextType.TEXT)
        result = split_image_nodes([node, node2])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text text text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].url, "img.webp")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[2].text, "alt text")
        self.assertEqual(result[2].url, "https://voylento.com/images/img.jpeg")
        self.assertEqual(result[2].text_type, TextType.IMAGE)

    def test_extract_md_link_no_match(self):
        node = TextNode("text text text, no markdown links", TextType.TEXT)
        result = split_image_nodes([node])
        self.assertTrue(len(result) == 1)
        node = result[0]
        self.assertEqual(node.text, "text text text, no markdown links")
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_extract_md_link_one_node(self):
        node = TextNode("text text text [link text](https://www.example.com) text after", TextType.TEXT)
        result = split_link_nodes([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text text text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link text")
        self.assertEqual(result[1].url, "https://www.example.com")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[2].text, " text after")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_extrat_md_link_two_nodes(self):
        node = TextNode("text text text [link text](http://x.com)", TextType.TEXT)
        node2 = TextNode("[link text](https://voylento.com/images/)", TextType.TEXT)
        result = split_link_nodes([node, node2])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text text text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link text")
        self.assertEqual(result[1].url, "http://x.com")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[2].text, "link text")
        self.assertEqual(result[2].url, "https://voylento.com/images/")
        self.assertEqual(result[2].text_type, TextType.LINK)

    def test_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        node = TextNode(text, TextType.TEXT)
        nodes_delimiters = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)
        result = split_image_nodes(split_link_nodes(nodes_delimiters))
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " with an ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " word and a ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code block")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " and an ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "obi wan image")
        self.assertEqual(result[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[8].text, " and a ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].url, "https://boot.dev")
        self.assertEqual(result[9].text_type, TextType.LINK)

    def test_markdown_to_blocks_simple(self):
        md = """
            ## This is a header
            """
        result = markdown_to_blocks(md)
        self.assertEqual(len(result), 1)
        self.assertEqual(
                result,
                [
                    "## This is a header",
                ],
            )

    def test_md_to_blocks_1(self):
        md = textwrap.dedent("""
            # Header 1

            Paragraph of text. It has some **bolded** and _italic_ text.

            `This is some code`

            ![alt image](my_img.jpeg)

            [link text](www.voylento.com)

            - List item 1
            - List item 2
            - List item 3
            """)

        result = markdown_to_blocks(md)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], "# Header 1")
        self.assertEqual(result[1], "Paragraph of text. It has some **bolded** and _italic_ text.")
        self.assertEqual(result[2], "`This is some code`")
        self.assertEqual(result[3], "![alt image](my_img.jpeg)")
        self.assertEqual(result[4], "[link text](www.voylento.com)")
        self.assertEqual(result[5], "- List item 1\n- List item 2\n- List item 3")

import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_value_only(self):
        node = HtmlNode(None, "Value Only Html Node")
        self.assertEqual(node.to_html(), "Value Only Html Node")

    def test_tag_no_attr_no_children(self):
        node = HtmlNode("p", "Simple paragraph tag")
        self.assertEqual(node.to_html(), "<p>Simple paragraph tag</p>")

    def test_tag_attr_no_children(self):
        props = {}
        props["href"] = "https://www.google.com"
        props["target"] = "_blank"
        node = HtmlNode("a", "This is a link", None, props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">This is a link</a>')

    def test_div_one_child(self):
        child_props = {
            "class": "main_header",
            }
        parent_props = {
            "id": "title",
            "class": "parent",
            }

        child_node = HtmlNode("h1", "Title Goes Here", None, child_props) 
        parent_node = HtmlNode("div", None, [child_node], parent_props)
        parent_node_str = parent_node.to_html()
        expected_rep = (
            '<div id="title" class="parent">'
            '<h1 class="main_header">Title Goes Here</h1>'
            '</div>'
            )
        self.assertEqual(parent_node_str, expected_rep)

    def test_dev_nested_children(self):
        grandchild_props =  {
            "class": "grandchild",
            "id": "grandchild",
            }
        child_props = {
            "class": "child",
            "id": "child",
            }
        node_props = {
            "class": "parent",
            "id": "parent",
            }

        grandchild_node = HtmlNode("p", "Grandchild", None, grandchild_props)
        child_node = HtmlNode("div", "Child", [grandchild_node], child_props)
        parent_node = HtmlNode("section", "", [child_node], node_props)

        expected_rep = (
            '<section class="parent" id="parent">'
            '<div class="child" id="child">Child'
            '<p class="grandchild" id="grandchild">Grandchild</p>'
            '</div></section>'
            )

        html_rep = parent_node.to_html()
        self.assertEqual(html_rep, expected_rep)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Paragraph tag")
        self.assertEqual(node.to_html(), "<p>Paragraph tag</p>")

    def test_leaf_with_props_to_html(self):
        props = {
            "id": "leaf_node",
            "class": "leaf_node",
            }
        value = "Leaf Node With Props"
        tag = "div"

        expected_html = (
            '<div id="leaf_node" class="leaf_node">Leaf Node With Props</div>'
            )

        leaf_node = LeafNode(tag, value, props)

        self.assertEqual(leaf_node.to_html(), expected_html)

    def test_leaf_to_html_img(self):
        props = {
                "id": "img_tag",
                "class": "img_tag",
                "alt": "Image tag alt text",
                "width": "500",
                "height": "600",
                "src": "img.jpg",
            }
        value = ""
        tag = "img"

        expected_html = (
            '<img id="img_tag" class="img_tag" '
            'alt="Image tag alt text" width="500" '
            'height="600" src="img.jpg"></img>'
            )

        node = LeafNode(tag, value, props)

        self.assertEqual(node.to_html(), expected_html)


class TestParentNode(unittest.TestCase):
    """ The HtmlNode test cases handle most of what I want to test here """
    def test_parent_with_multiple_leaves(self):
        tag = "div"
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "Normal text"),
            ]
        props = {
            "id": "parent_node",
            "class": "parent_node super_duper",
            }

        parent_node = ParentNode(tag, children, props)

        expected_html = (
            '<div id="parent_node" class="parent_node super_duper">'
            '<b>Bold text</b>Normal text<i>Italic text</i>Normal text'
            '</div>'
            )

        parent_node_html = parent_node.to_html()

        self.assertEqual(parent_node_html, expected_html)
        


if __name__=="__main__":
    unittest.main()

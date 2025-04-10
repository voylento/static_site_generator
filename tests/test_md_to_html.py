import unittest
import textwrap

from src.converters import (
        markdown_to_html,
    )

class TestConvertHtml(unittest.TestCase):

    def test_md_header_to_html(self):
        md = """
            ## This is a header
            """
        html_node = markdown_to_html(md)
        html_text = html_node.to_html()
        self.assertEqual(html_node.to_html(), "<div><h2>This is a header</h2></div>")


    def test_md_single_paragraph(self):
        md = r"""This is a paragraph with **bolded text** and _italicized text_ and nothing else."""

        expected_html = (
                '<div><p>This is a paragraph with <b>bolded text</b>'
                ' and <i>italicized text</i> and nothing else.</p></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()
        self.assertEqual(html_text, expected_html)

    def test_md_paragraph(self):
        md = """
This is a **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ and `code` here
"""

        expected_html = (
                '<div><p>This is a <b>bolded</b> paragraph text in a p '
                'tag here</p>'
                '<p>This is another paragraph with <i>italic</i> and <code>code</code> here</p></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()
        self.assertEqual(html_text, expected_html)

    def test_md_code_block(self):
        md = """
```
This is text that **should**
remain the _same_ even with
inline stuff
```
"""
        expected_html = (
                '<div><pre><code>'
                'This is text that **should**\nremain the _same_ '
                'even with\n'
                'inline stuff</code></pre></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()

        self.assertEqual(html_text, expected_html)
        

    def test_md_quote_block(self):
        md = """
>This is a quote from somebody
>who is famous, I suppose
>maybe like Jon Bon Jovi
"""
        expected_html = (
                '<div><blockquote><p>'
                'This is a quote from somebody\n'
                'who is famous, I suppose\n'
                'maybe like Jon Bon Jovi</p></blockquote></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()

        self.assertEqual(html_text, expected_html)
        

    def test_md_ul_block(self):
        md = """
- Item 1 in the list
- Item 2 in the list
- Item 3 in the list
"""
        expected_html = (
                '<div><ul><li>Item 1 in the list</li><li>Item 2 in the list</li><li>Item 3 in the list</li></ul></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()

        self.assertEqual(html_text, expected_html)
        
    def test_md_ol_block(self):
        md = """
1. Item 1 in the list
2. Item 2 in the list
3. Item 3 in the list
"""
        expected_html = (
                '<div><ol><li>Item 1 in the list</li><li>Item 2 in the list</li><li>Item 3 in the list</li></ol></div>'
            )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()

        self.assertEqual(html_text, expected_html)
        

    def test_md_complex(self):
        md = """
This is a paragraph with **bold** text and _italic_ text

1. Item 1 in an ordered list
2. Item 2 in an ordered list
3. Item 3 in an ordered list

```
my_list = ['abc', 'bcd', 'cat']
for item in my_list:
    print(f"{item}")
```

>He who codes without debugging is he
>who debugs without coding

- Item 1 in an unordered list
- Item 2 in an unordered list
"""
        expected_html = (
                '<div>'
                '<p>This is a paragraph with <b>bold</b> text and <i>italic</i> text</p>'
                '<ol><li>Item 1 in an ordered list</li><li>Item 2 in an ordered list</li><li>Item 3 in an ordered list</li></ol>'
                '<pre><code>'
                "my_list = ['abc', 'bcd', 'cat']\n"
                'for item in my_list:\n'
                '    print(f"{item}")</code></pre>'
                '<blockquote><p>He who codes without debugging is he\n'
                'who debugs without coding</p></blockquote>'
                '<ul><li>Item 1 in an unordered list</li><li>Item 2 in an unordered list</li></ul>'
                '</div>'
                )

        html_node = markdown_to_html(md)
        html_text = html_node.to_html()

        self.assertEqual(html_text, expected_html)
        

import unittest

from src.blocks import (
        BlockType, 
    )

from src.converters import (
        block_to_block_type,
    )

btbt = block_to_block_type

heading1_str = "# This is a markdown heading 1"
heading2_str = "## This is a markdown heading 2"
heading3_str = "### This is a markdown heading 3"
heading4_str = "#### This is a markdown heading 4"
heading5_str = "##### This is a markdown heading 5"
heading6_str = "###### This is a markdown heading 6"
heading7_str = "####### This is an invalid markdown heading"

code_single_line = "```my_str = 'This is a string'```"
code_multi_line = """
```
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def do_something(self):
        return x + y
```
""".strip()

quote_single_line = ">This is a quote line"
quote_multi_line = """
> The greatest day in my life was when I picked up the guitar
> The second greatest day was when I put it down
> --Bruce Springsteen
""".strip()

unordered_list_single_line = "- item 1"
unordered_list_multi_line = """
- item 1
- item 2
- item 3
- item 4
- item 5
""".strip()

ordered_list_single_line = "1. item 1"
ordered_list_multi_line = """
1. item 1
2. item 2
3. item 3
4. item 4
5. item 5
6. item 6
7. item 7
8. item 8
9. item 9
10. item 10
""".strip()

paragraph_single_line = "This is a single line paragraph"
paragraph_multi_line ="""
This is a multi-line
paragraph
""".strip()

class TestBlockType(unittest.TestCase):
    
    def test_empty_str(self):
        self.assertEqual(btbt(""), BlockType.PARAGRAPH)

    def test_heading_1(self):
        self.assertEqual(btbt(heading1_str), BlockType.HEADING)

    def test_heading_2(self):
        self.assertEqual(btbt(heading2_str), BlockType.HEADING)

    def test_heading_3(self):
        self.assertEqual(btbt(heading3_str), BlockType.HEADING)

    def test_heading_4(self):
        self.assertEqual(btbt(heading4_str), BlockType.HEADING)

    def test_heading_5(self):
        self.assertEqual(btbt(heading5_str), BlockType.HEADING)

    def test_heading_6(self):
        self.assertEqual(btbt(heading6_str), BlockType.HEADING)

    def test_heading_7(self):
        self.assertEqual(btbt(heading7_str), BlockType.PARAGRAPH)

    def test_single_line_quote(self):
        self.assertEqual(btbt(quote_single_line), BlockType.QUOTE)

    def test_multi_line_quote(self):
        self.assertEqual(btbt(quote_multi_line), BlockType.QUOTE)

    def test_single_line_code(self):
        self.assertEqual(btbt(code_single_line), BlockType.CODE)

    def test_multi_line_code(self):
        self.assertEqual(btbt(code_multi_line), BlockType.CODE)

    def test_single_line_ordered_list(self):
        self.assertEqual(btbt(ordered_list_single_line), BlockType.ORDERED_LIST)

    def test_multi_line_ordered_list(self):
        self.assertEqual(btbt(ordered_list_multi_line), BlockType.ORDERED_LIST)
    
    def test_single_line_unordered_list(self):
        self.assertEqual(btbt(unordered_list_single_line), BlockType.UNORDERED_LIST)

    def test_multi_line_unordered_list(self):
        self.assertEqual(btbt(unordered_list_multi_line), BlockType.UNORDERED_LIST)

    def test_single_line_paragraph(self):
        self.assertEqual(btbt(paragraph_single_line), BlockType.PARAGRAPH)

    def test_multi_line_paragraph(self):
        self.assertEqual(btbt(paragraph_multi_line), BlockType.PARAGRAPH)
    

if __name__=="__main__":
    unittest.main()

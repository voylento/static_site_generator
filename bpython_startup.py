from src.blocktype import BlockType, BlockNode, block_to_block_type
btbt = block_to_block_type
heading1_str = "# This is a markdown heading 1"
heading2_str = "## This is a markdown heading 2"
heading3_str = "### This is a markdown heading 3"
heading4_str = "#### This is a markdown heading 4"
heading5_str = "##### This is a markdown heading 5"
heading6_str = "###### This is a markdown heading 6"
heading7_str = "####### This is an invalid markdown heading"

code_str_single_line = "```my_str = 'This is a string'```"
code_str_multi_line = """
```
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def do_something(self):
        return x + y
```
""".strip()

unordered_list = """
- item 1
- item 2
- item 3
- item 4
- item 5
""".strip()

ordered_list = """
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

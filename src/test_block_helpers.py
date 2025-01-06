import unittest
from block_helpers import markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_heading_and_paragraph(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_list_block(self):
        markdown = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected_blocks = [
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_blocks(self):
        markdown = """# This is a heading

This is a paragraph.

* List item 1
* List item 2"""
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph.",
            """* List item 1
* List item 2""",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_empty_document(self):
        markdown = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_whitespace_only(self):
        markdown = "\n\n   \n"
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type(
                """```
def hello():
    print("Hello, world!")
```"""
            ),
            "code",
        )

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type("> This is a quote block\n> It spans multiple lines"),
            "quote",
        )

    def test_unordered_list_block(self):
        self.assertEqual(
            block_to_block_type(
                """* Item 1
* Item 2
* Item 3"""
            ),
            "unordered_list",
        )
        self.assertEqual(
            block_to_block_type(
                """- Item A
- Item B
- Item C"""
            ),
            "unordered_list",
        )

    def test_ordered_list_block(self):
        self.assertEqual(
            block_to_block_type(
                """1. First item
2. Second item
3. Third item"""
            ),
            "ordered_list",
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type(
                "This is a normal paragraph. It contains text but no Markdown block syntax."
            ),
            "paragraph",
        )

    def test_mixed_content(self):
        self.assertEqual(block_to_block_type("#HeadingWithoutSpace"), "paragraph")
        self.assertEqual(block_to_block_type(">Quote without leading space"), "quote")
        self.assertEqual(block_to_block_type("1.ItemWithoutSpace"), "paragraph")

    def test_edge_cases(self):
        # Empty block should not match any block type
        self.assertEqual(block_to_block_type(""), "paragraph")

        # Single backticks should not match a code block
        self.assertEqual(block_to_block_type("`Not a code block`"), "paragraph")

        # Invalid ordered list (non-incrementing numbers)
        self.assertEqual(
            block_to_block_type(
                """1. Item 1
3. Item 3"""
            ),
            "paragraph",
        )

        # Invalid ordered list (incorrect starting number)
        self.assertEqual(
            block_to_block_type(
                """2. First item
3. Second item"""
            ),
            "paragraph",
        )


if __name__ == "__main__":
    unittest.main()

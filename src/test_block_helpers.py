import unittest
from block_helpers import markdown_to_blocks


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

    if __name__ == "__main__":
        unittest.main()

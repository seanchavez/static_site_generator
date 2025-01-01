import unittest
from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_valid_delimiter_single_asterisk(self):
        old_nodes = [TextNode("Hello*world*again", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "again")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_valid_delimiter_double_asterisk(self):
        old_nodes = [TextNode("Start**middle**end", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Start")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "end")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_valid_delimiter_backticks(self):
        old_nodes = [TextNode("Code`example`snippet", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Code")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "example")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "snippet")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_invalid_delimiter(self):
        old_nodes = [TextNode("No|splitting|here", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "|", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No|splitting|here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_non_normal_text_type(self):
        old_nodes = [TextNode("This text is bold", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This text is bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_empty_text_node(self):
        old_nodes = [TextNode("", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_no_splits(self):
        old_nodes = [TextNode("No delimiter here", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_mixed_delimiters(self):
        old_nodes = [TextNode("Mix**bold**and*italic*styles", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        print(f"RESULT: {result}")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Mix")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "and*italic*styles")
        self.assertEqual(result[2].text_type, TextType.NORMAL)


if __name__ == "__main__":
    unittest.main()

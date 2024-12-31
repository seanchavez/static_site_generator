import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from text_to_html import text_node_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode(text="Hello", text_type=TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello")

    def test_text_type_bold(self):
        text_node = TextNode(text="Bold Text", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")

    def test_text_type_italic(self):
        text_node = TextNode(text="Italic Text", text_type=TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic Text")

    def test_text_type_code(self):
        text_node = TextNode(text="Code Snippet", text_type=TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code Snippet")

    def test_text_type_link(self):
        text_node = TextNode(
            text="OpenAI", text_type=TextType.LINK, url="https://openai.com"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "OpenAI")
        self.assertEqual(html_node.props, {"href": "https://openai.com"})

    def test_text_type_image(self):
        text_node = TextNode(
            text="Image Alt Text",
            text_type=TextType.IMAGE,
            url="https://example.com/image.jpg",
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.jpg", "alt": "Image Alt Text"},
        )

    def test_invalid_text_type(self):
        text_node = TextNode(text="Invalid", text_type="UNKNOWN")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()

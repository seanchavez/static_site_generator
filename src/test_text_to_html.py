import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from text_node_to_html_node import text_node_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text(self):
        text_node = TextNode("Hello", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertIsNone(html_node.props)

    def test_bold_text(self):
        text_node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")
        self.assertIsNone(html_node.props)

    def test_italic_text(self):
        text_node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")
        self.assertIsNone(html_node.props)

    def test_code_text(self):
        text_node = TextNode("Code", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code")
        self.assertIsNone(html_node.props)

    def test_link_text(self):
        text_node = TextNode("Example", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_text(self):
        text_node = TextNode("Image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": "Image"}
        )

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()

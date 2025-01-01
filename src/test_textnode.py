import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_initialization(self):
        node = TextNode("Hello", TextType.NORMAL)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.NORMAL)
        self.assertIsNone(node.url)

    def test_initialization_with_url(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Example")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_equality_same_nodes(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_equality_different_text(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hi", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_equality_different_text_type(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_equality_different_url(self):
        node1 = TextNode("Example", TextType.LINK, "https://example.com")
        node2 = TextNode("Example", TextType.LINK, "https://another.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Hello", TextType.NORMAL)
        representation = repr(node)
        self.assertEqual(representation, "TextNode(Hello, TextType.NORMAL, None)")

    def test_repr_with_url(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        representation = repr(node)
        self.assertEqual(
            representation, "TextNode(Example, TextType.LINK, https://example.com)"
        )


if __name__ == "__main__":
    unittest.main()

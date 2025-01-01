import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        node = LeafNode("p", "Hello, world!", {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props, {"class": "text"})

    def test_initialization_defaults(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.props)

    def test_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "text"})
        html = node.to_html()
        self.assertEqual(html, "<p class=text>Hello, world!</p>")

    def test_to_html_without_props(self):
        node = LeafNode("p", "Hello, world!")
        html = node.to_html()
        self.assertEqual(html, "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        html = node.to_html()
        self.assertEqual(html, "Hello, world!")

    def test_to_html_missing_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()

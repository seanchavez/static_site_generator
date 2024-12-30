import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        node = LeafNode(tag="span", value="Hello", props={"class": "highlight"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"class": "highlight"})

    def test_initialization_defaults(self):
        node = LeafNode(tag="span", value="World")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "World")
        self.assertIsNone(node.props)

    def test_to_html_with_props(self):
        node = LeafNode(tag="div", value="Content", props={"id": "main"})
        html = node.to_html()
        self.assertEqual(html, "<div id=main>Content</div>")

    def test_to_html_without_props(self):
        node = LeafNode(tag="p", value="Text")
        html = node.to_html()
        self.assertEqual(html, "<p>Text</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Plain Text")
        html = node.to_html()
        self.assertEqual(html, "Plain Text")

    def test_to_html_missing_value(self):
        node = LeafNode(tag="span", value=None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()

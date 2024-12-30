import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_initialization_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="div",
            value="Hello",
            children=[],
            props={"class": "container", "id": "main"},
        )
        html_attributes = node.props_to_html()
        self.assertEqual(html_attributes, " class=container id=main")

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        html_attributes = node.props_to_html()
        self.assertEqual(html_attributes, "")

    def test_props_to_htnl_none(self):
        node = HTMLNode()
        html_attributes = node.props_to_html()
        self.assertEqual(html_attributes, "")

    def test_repr(self):
        node = HTMLNode(
            tag="p", value="Text", children=[], props={"style": "color:red;"}
        )
        repr_output = repr(node)
        self.assertEqual(repr_output, "HTMLNode(p, Text, [], {'style': 'color:red;'})")

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()

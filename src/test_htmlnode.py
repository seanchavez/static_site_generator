import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode("div", "Content", None, {"id": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"id": "main"})

    def test_initialization_defaults(self):
        node = HTMLNode("div", "Content")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html(self):
        node = HTMLNode("div", "Content", None, {"class": "container", "id": "main"})
        html_props = node.props_to_html()
        self.assertEqual(html_props, " class=container id=main")

    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Content")
        html_props = node.props_to_html()
        self.assertEqual(html_props, "")

    def test_repr(self):
        node = HTMLNode("div", "Content", None, {"id": "main"})
        representation = repr(node)
        self.assertEqual(representation, "HTMLNode(div, Content, None, {'id': 'main'})")


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


class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "World")
        node = ParentNode("div", [child1, child2], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.props, {"class": "container"})

    def test_initialization_no_props(self):
        child = LeafNode("p", "Content")
        node = ParentNode("section", [child])
        self.assertEqual(node.tag, "section")
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.props)

    def test_to_html_with_children(self):
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2")
        node = ParentNode("div", [child1, child2])
        html = node.to_html()
        self.assertEqual(html, "<div><span>Child 1</span><span>Child 2</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("i", "grandchild")
        child = ParentNode("span", [grandchild])
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><span><i>grandchild</i></span></div>")

    def test_to_html_no_tag(self):
        child = LeafNode("p", "Content")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()

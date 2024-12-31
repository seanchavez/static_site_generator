import unittest
from htmlnode import HTMLNode
from parentnode import ParentNode


class MockLeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        return f"<{self.tag}>{self.value}</{self.tag}>"


class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        child1 = MockLeafNode(tag="span", value="Hello")
        child2 = MockLeafNode(tag="span", value="World")
        node = ParentNode(
            tag="div", children=[child1, child2], props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.props, {"class": "container"})

    def test_initialization_no_props(self):
        child = MockLeafNode(tag="p", value="Content")
        node = ParentNode(tag="section", children=[child])
        self.assertEqual(node.tag, "section")
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.props)

    def test_to_html_with_children(self):
        child1 = MockLeafNode(tag="span", value="Child 1")
        child2 = MockLeafNode(tag="span", value="Child 2")
        node = ParentNode(tag="div", children=[child1, child2])
        html = node.to_html()
        self.assertEqual(html, "<div><span>Child 1</span><span>Child 2</span></div>")

    def test_to_html_no_tag(self):
        child = MockLeafNode(tag="p", value="Content")
        node = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()

import unittest
from parentnode import ParentNode
from leafnode import LeafNode


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

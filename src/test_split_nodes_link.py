import unittest
from textnode import TextType, TextNode
from split_nodes_link import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) to learn backend development.",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.NORMAL),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" to learn backend development.", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "Here are links to [Google](https://google.com) and [YouTube](https://youtube.com).",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Here are links to ", TextType.NORMAL),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("YouTube", TextType.LINK, "https://youtube.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [node]  # No splitting needed
        self.assertEqual(result, expected)

    def test_text_with_only_links(self):
        node = TextNode(
            "[Link1](https://link1.com)[Link2](https://link2.com)", TextType.NORMAL
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Link1", TextType.LINK, "https://link1.com"),
            TextNode("Link2", TextType.LINK, "https://link2.com"),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("Non-text node", TextType.CODE)
        result = split_nodes_link([node])
        expected = [node]  # Should return as-is
        self.assertEqual(result, expected)

    def test_text_with_nested_brackets(self):
        node = TextNode(
            "Text with [nested [brackets]](https://example.com).", TextType.NORMAL
        )
        result = split_nodes_link([node])
        expected = [
            node
        ]  # Should return as-is since nested brackets aren't valid Markdown links
        self.assertEqual(result, expected)

    def test_malformed_markdown(self):
        node = TextNode(
            "Malformed [link](https://link.com with missing parentheses.",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        expected = [node]  # No valid links found, return as-is
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

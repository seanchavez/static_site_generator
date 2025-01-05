import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_mixed_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_plain_text(self):
        text = "This is plain text without any Markdown."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is plain text without any Markdown.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_only_bold(self):
        text = "**bold text**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold text", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_only_italic(self):
        text = "*italic text*"
        result = text_to_textnodes(text)
        expected = [TextNode("italic text", TextType.ITALIC)]
        self.assertEqual(result, expected)

    def test_only_code(self):
        text = "`code block`"
        result = text_to_textnodes(text)
        expected = [TextNode("code block", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_only_image(self):
        text = "![alt text](https://example.com/image.jpg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(result, expected)

    def test_only_link(self):
        text = "[link text](https://example.com)"
        result = text_to_textnodes(text)
        expected = [TextNode("link text", TextType.LINK, "https://example.com")]
        self.assertEqual(result, expected)

    def test_combination_of_formats(self):
        text = "This is *italic* and **bold** and a `code`."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

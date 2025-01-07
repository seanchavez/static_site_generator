import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_helpers import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_valid_delimiter_single_asterisk(self):
        old_nodes = [TextNode("Hello*world*again", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "again")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_valid_delimiter_double_asterisk(self):
        old_nodes = [TextNode("Start**middle**end", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Start")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "end")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_valid_delimiter_backticks(self):
        old_nodes = [TextNode("Code`example`snippet", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Code")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "example")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "snippet")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_invalid_delimiter(self):
        old_nodes = [TextNode("No|splitting|here", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "|", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No|splitting|here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_non_normal_text_type(self):
        old_nodes = [TextNode("This text is bold", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This text is bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_empty_text_node(self):
        old_nodes = [TextNode("", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_no_splits(self):
        old_nodes = [TextNode("No delimiter here", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_mixed_delimiters(self):
        old_nodes = [TextNode("Mix**bold**and*italic*styles", TextType.NORMAL)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        print(f"RESULT: {result}")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Mix")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "and*italic*styles")
        self.assertEqual(result[2].text_type, TextType.NORMAL)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_valid_images(self):
        text = "![alt text](https://example.com/image1.jpg) and ![logo](https://example.com/logo.png)"
        result = extract_markdown_images(text)
        expected = [
            ("alt text", "https://example.com/image1.jpg"),
            ("logo", "https://example.com/logo.png"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = "This is a text without images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_partial_markdown(self):
        text = "![alt text](https://example.com/image.jpg"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_multiple_images(self):
        text = "![image1](url1) some text ![image2](url2) more text ![image3](url3)"
        result = extract_markdown_images(text)
        expected = [
            ("image1", "url1"),
            ("image2", "url2"),
            ("image3", "url3"),
        ]
        self.assertEqual(result, expected)

    def test_empty_alt_text(self):
        text = "![](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "https://example.com/image.jpg")])

    def test_empty_url(self):
        text = "![alt text]()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "")])

    def test_malformed_syntax(self):
        text = "![alt text]https://example.com/image.jpg"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_valid_links(self):
        text = "[Google](https://google.com) and [Example](https://example.com)"
        result = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("Example", "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_ignore_images(self):
        text = "![Image](https://example.com/image.jpg) [Link](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("Link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = "This text contains no links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_malformed_links(self):
        text = "[Google(https://google.com) [Example](example.com"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_mixed_content(self):
        text = (
            "![Image](https://example.com/image.jpg) "
            "[Valid Link](https://example.com) "
            "Some text ![Another Image](https://example.com/another.jpg) "
            "[Another Link](https://example.org)"
        )
        result = extract_markdown_links(text)
        expected = [
            ("Valid Link", "https://example.com"),
            ("Another Link", "https://example.org"),
        ]
        self.assertEqual(result, expected)

    def test_empty_alt_text(self):
        text = "[]() and [Empty URL]()"
        result = extract_markdown_links(text)
        expected = [
            ("", ""),
            ("Empty URL", ""),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is a text with an image ![alt text](https://example.com/image.jpg).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is a text with an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode(
            "Text with multiple images: ![image1](https://example.com/image1.jpg) and ![image2](https://example.com/image2.jpg).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with multiple images: ", TextType.NORMAL),
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.jpg"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("This is a plain text without any images.", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [node]  # No splitting needed
        self.assertEqual(result, expected)

    def test_non_normal_text_node(self):
        node = TextNode("This is code: `![image](url)`", TextType.CODE)
        result = split_nodes_image([node])
        expected = [node]  # Non-normal text node is returned as is
        self.assertEqual(result, expected)

    def test_malformed_image_syntax(self):
        node = TextNode(
            "This is malformed: ![alt text](https://example.com/image.jpg",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [node]  # Malformed image syntax is ignored
        self.assertEqual(result, expected)

    def test_text_with_adjacent_images(self):
        node = TextNode(
            "Images: ![image1](https://example.com/image1.jpg)![image2](https://example.com/image2.jpg).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Images: ", TextType.NORMAL),
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.jpg"),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.jpg"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_text_with_empty_alt_text(self):
        node = TextNode(
            "Here is an image: ![](https://example.com/image.jpg).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an image: ", TextType.NORMAL),
            TextNode("", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)


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

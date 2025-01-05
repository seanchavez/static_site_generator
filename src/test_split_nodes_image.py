import unittest
from textnode import TextType, TextNode
from split_nodes_image import split_nodes_image


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


if __name__ == "__main__":
    unittest.main()

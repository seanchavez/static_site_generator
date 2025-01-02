import unittest
import re
from extract_markdown_images import extract_markdown_images


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


if __name__ == "__main__":
    unittest.main()

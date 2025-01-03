import unittest
import re
from extract_markdown_links import extract_markdown_links


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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


if __name__ == "__main__":
    unittest.main()

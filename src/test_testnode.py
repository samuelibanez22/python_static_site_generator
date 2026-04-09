import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url_none_vs_set(self):
        node = TextNode("Click me", TextType.LINK)
        node2 = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("Plain text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node),
            "TextNode(This is some anchor text, link, https://www.boot.dev)",
        )

if __name__ == "__main__":
    unittest.main()

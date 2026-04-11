import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.boot.dev">Click me</a>',
        )

    def test_image(self):
        node = TextNode("A cute cat", TextType.IMAGE, "https://example.com/cat.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/cat.jpg", "alt": "A cute cat"},
        )

    def test_invalid_type_raises(self):
        node = TextNode("Oops", TextType.TEXT)
        node.text_type = "not a real type"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()

import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.boot.dev", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello, world!", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_values(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.boot.dev"},
        )
        repr_str = repr(node)
        self.assertIn("a", repr_str)
        self.assertIn("Click me", repr_str)
        self.assertIn("href", repr_str)

if __name__ == "__main__":
    unittest.main()

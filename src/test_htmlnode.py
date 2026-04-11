import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev">Click me!</a>',
        )

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" target="_blank">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some raw text.")
        self.assertEqual(node.to_html(), "Just some raw text.")

    def test_leaf_to_html_different_tags(self):
        self.assertEqual(LeafNode("h1", "Heading").to_html(), "<h1>Heading</h1>")
        self.assertEqual(LeafNode("b", "Bold").to_html(), "<b>Bold</b>")
        self.assertEqual(LeafNode("i", "Italic").to_html(), "<i>Italic</i>")
        self.assertEqual(LeafNode("span", "Span").to_html(), "<span>Span</span>")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        repr_str = repr(node)
        self.assertIn("LeafNode", repr_str)
        self.assertIn("p", repr_str)
        self.assertIn("Hello", repr_str)
        self.assertNotIn("children", repr_str)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_deeply_nested(self):
        innermost = LeafNode("b", "deep")
        level3 = ParentNode("i", [innermost])
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(),
            "<div><span><i><b>deep</b></i></span></div>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "hi")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>hi</span></div>',
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "hi")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_mixed_leaf_and_parent_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode(None, "Some "), LeafNode("b", "bold"), LeafNode(None, " text.")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Some <b>bold</b> text.</p></div>",
        )


if __name__ == "__main__":
    unittest.main()

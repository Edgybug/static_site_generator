import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
      
        def test_to_html_props(self):
            node = HTMLNode(
                "div",
                "Hello, world!",
                None,
                {"class": "greeting", "href": "https://boot.dev"},
            )
            self.assertEqual(
                node.props_to_html(),
                ' class="greeting" href="https://boot.dev"',
            )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, {'class': 'primary'}, None)",
        )

    def test_eq(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode("a", "Click me!", {"href": "https://www.bing.com"})
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_leafnode_with_tag_and_value(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leafnode_without_tag(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), 'Just text')

    def test_leafnode_without_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_with_props(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image"></img>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )

    def test_parent_node_with_props(self):
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>Hello</span></div>'
        )

    def test_nested_parent_nodes_with_props(self):
        innermost = LeafNode("span", "Text", {"class": "highlight"})
        middle = ParentNode("div", [innermost], {"id": "content"})
        outer = ParentNode("section", [middle], {"class": "wrapper"})
        self.assertEqual(
            outer.to_html(),
            '<section class="wrapper"><div id="content"><span class="highlight">Text</span></div></section>'
        )

    def test_parent_node_with_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_node_with_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_node_with_none_tag(self):
        child = LeafNode("p", "Paragraph")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

        
if __name__ == "__main__":
    unittest.main()
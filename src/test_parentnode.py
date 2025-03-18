import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()

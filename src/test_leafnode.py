import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()

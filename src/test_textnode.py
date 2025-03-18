import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        node3 = TextNode("This is a text node", TextType.TEXT)
        node31 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node41 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.CODE)
        node51 = TextNode("This is a text node", TextType.CODE)
        node6 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev/tracks/backend")
        node61 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev/tracks/backend")
        node7 = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/tracks/backend")
        node71 = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/tracks/backend")
        
        self.assertEqual(node, node2)
        self.assertEqual(node3, node31)
        self.assertEqual(node4, node41)
        self.assertEqual(node5, node51)
        self.assertEqual(node6, node61)
        self.assertEqual(node7, node71)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bolded text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bolded text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_img(self):
        node = TextNode(None, TextType.IMAGE, props={"src": "https://example.com/image.png", "alt": "An example image"})
        html_node = node.text_node_to_html_node()
        # Ensure the tag is "img"
        self.assertEqual(html_node.tag, "img")
        # Ensure the value is empty
        self.assertEqual(html_node.value, "")
        # Ensure the props dictionary includes correct keys and values
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "An example image")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, props={"href": "https://example.com"})
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://example.com")

    # Additional failure cases for robustness
    def test_image_missing_props(self):
        node = TextNode(None, TextType.IMAGE)  # No props provided
        with self.assertRaises(Exception):
            node.text_node_to_html_node()

    def test_link_missing_props(self):
        node = TextNode("This is a link node", TextType.LINK)  # No props provided
        with self.assertRaises(Exception):
            node.text_node_to_html_node()
        
    
      
if __name__ == "__main__":
    unittest.main()
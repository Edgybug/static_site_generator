import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType

class TestExtractOfImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        assert new_nodes == [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
        ]
    
    def test_no_images(self):
        node = TextNode("This is plain text with no images at all.", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [TextNode("This is plain text with no images at all.", TextType.TEXT)],
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Text before the first image ", TextType.TEXT),
            TextNode("![First](https://example.com/first.png)", TextType.TEXT),
            TextNode(" and some text after the first image.", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(nodes)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Text before the first image ", TextType.TEXT),
                TextNode("First", TextType.IMAGE, "https://example.com/first.png"),
                TextNode(" and some text after the first image.", TextType.TEXT),
            ],
        )

    def test_only_image(self):
        node = TextNode("![JustImage](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [TextNode("JustImage", TextType.IMAGE, "https://example.com/image.png")],
        )

    def test_no_links(self):
        node = TextNode("This is plain text without any links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is plain text without any links.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_single_link(self):
        node = TextNode("Click [here](https://example.com) to visit the website.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to visit the website.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links(self):
        node = TextNode("Visit [Boot.dev](https://www.boot.dev) and [YouTube](https://www.youtube.com).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links(self):
        node = TextNode("Visit [Boot.dev](https://www.boot.dev) and [YouTube](https://www.youtube.com).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("[Link](https://example.com)", TextType.TEXT),
            TextNode(" after link.", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("Link", TextType.LINK, "https://example.com"),
            TextNode(" after link.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes(self):
        nodes = [
            TextNode("Some text with no links.", TextType.TEXT),
            TextNode("Already processed link", TextType.LINK, "https://example.com"),
            TextNode("And an image node", TextType.IMAGE, "https://image.link/image.png")
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, nodes)  # Nothing should change here


    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):

        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)


if __name__ == '__main__':
    unittest.main()

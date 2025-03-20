import re

from enum import Enum
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    split_images_list = []

    for node in old_nodes:
        text = node.text

        if not extract_markdown_images(text):
            # No images, append the single text node
            split_images_list.append(TextNode(node.text, node.text_type))
        else:
            # Repeatedly process images within the text
            while extract_markdown_images(text):
                images = extract_markdown_images(text)
                image = images[0]  # Process the first image
                alt = image[0]
                link = image[1]

                # Split text at this image's markdown
                sections = text.split(f"![{alt}]({link})", 1)

                # Add the text BEFORE the image
                if sections[0]:
                    split_images_list.append(TextNode(sections[0], TextType.TEXT))

                # Add the image node itself
                split_images_list.append(TextNode(alt, TextType.IMAGE, link))

                # Continue processing the remaining text AFTER the image
                text = sections[1]

            # After the loop, add the remaining text (if any) as a node
            if text:
                split_images_list.append(TextNode(text, TextType.TEXT))

    return split_images_list
            
   

def split_nodes_link(old_nodes):
    split_link_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_link_list.append(node)
            continue
        text = node.text

        if not extract_markdown_links(text):
            # No links, append the single text node
            split_link_list.append(TextNode(node.text, node.text_type))
        else:
            # Repeatedly process links within the text
            while extract_markdown_links(text):
                links = extract_markdown_links(text)
                link = links[0]  # Process the first link
                link_text = link[0]
                link_url = link[1]

                # Split text at this link's markdown
                sections = text.split(f"[{link_text}]({link_url})", 1)
                
                # Add the text BEFORE the link
                if sections[0]:
                    split_link_list.append(TextNode(sections[0], TextType.TEXT))

                # Add the link node itself
                split_link_list.append(TextNode(link_text, TextType.LINK, link_url))

                # Continue processing the remaining text AFTER the link
                text = sections[1]

            # After the loop, add the remaining text (if any) as a node
            if text:
                split_link_list.append(TextNode(text, TextType.TEXT))

    return split_link_list
                    
                          
def extract_markdown_images(text):
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return match

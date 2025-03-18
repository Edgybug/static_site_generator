from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
        TEXT = "text"
        BOLD = "bold"
        ITALIC = "italic"
        CODE = "code"
        LINK = "link"
        IMAGE = "image"
       
class TextNode():
    def __init__(self, text, text_type, props = None):
        self.text = text
        self.text_type = text_type
        self.props = props or {}
    
    def text_node_to_html_node(self):
        """
            Converts a TextNode into a LeafNode, handling specific TextType values.

            Supported TextTypes:
            - TEXT: Returns a raw text LeafNode (no tag).
            - BOLD: Returns a LeafNode with a "b" tag and text value.
            - ITALIC: Returns a LeafNode with an "i" tag and text value.
            - CODE: Returns a LeafNode with a "code" tag and text value.
            - IMAGE: Requires 'src' and 'alt' in props. Returns a LeafNode with "img" tag and props.
            - LINK: Requires 'href' in props. Returns a LeafNode with an "a" tag, text value, and props.

            Raises:
            - ValueError: If required props are missing for IMAGE or LINK.
            - Exception: For unsupported TextTypes.
        """
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text , None)
            case TextType.BOLD:
                return LeafNode("b", self.text, None)
            case TextType.ITALIC:
                return LeafNode("i", self.text, None)
            case TextType.CODE:
                return LeafNode("code", self.text, None)
            case TextType.IMAGE:
            # Validate 'url' and 'text' (for alt)
                if "src" not in self.props or "alt" not in self.props:
                    raise ValueError(f"IMAGE nodes require 'src' (url) and 'alt' (text). Props provided: {self.props}")
                return LeafNode("img", "", self.props)
            case TextType.LINK:
            # Validate required properties in props
                if "href" not in self.props:
                    raise ValueError(f"LINK nodes require 'href' property. Props provided: {self.props}")
                return LeafNode("a", self.text, self.props)
            case _: 
                raise Exception("Type not supported")
            
            
    def __eq__(self, other):
         return self.text == other.text and self.text_type == other.text_type and self.props == other.props
    
    def __repr__(self):
         return f"TextNode({self.text}, {self.text_type.value}, {self.props})"
    
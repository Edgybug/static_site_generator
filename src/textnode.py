from htmlnode import LeafNode
from enum import Enum

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
    
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.children = []
    
    def to_html(self):

        if self.value == None:
            raise ValueError("A LeafNode must have a value to render as HTML.")
        if self.tag == None:
            return self.value
        
        props_string = self.props_to_html()

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
        

#node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
#print(node.to_html())
        
        
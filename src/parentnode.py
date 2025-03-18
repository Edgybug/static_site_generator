from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, props)
        self.children = children
        #tag and children are required
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("A ParentNode must have a tag to render as HTML.")
        if not self.children:
            raise ValueError("A ParentNode must have children to render as HTML.")
        
        props_string = self.props_to_html()
       
        #Handle opening tag
        if self.props:
            html_string = f"<{self.tag}{props_string}>"
        else:
            html_string = f"<{self.tag}>"
        
        #Process the children:
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        #add closing tag
        closing_tag = f"</{self.tag}>"
        
        return html_string + children_html + closing_tag
    

       
    
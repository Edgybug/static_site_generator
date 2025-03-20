

class HTMLNode():
    def __init__(self, tag = None, value = None, props = None, children = None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_html = ""

        for key in self.props:
            props_html += f' {key}="{self.props[key]}"'
        return props_html
    
    def __repr__(self):
      return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
         return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


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
    

       
    
        


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


#
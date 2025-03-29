class HtmlNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        if props == None:
            self.props = {}
        else:
            self.props = props

        assert self.tag != None or self.value != None
        assert self.value != None or self.children != None

    def to_html(self):
        result = ""
        if self.children == None:
            # This is a LeafNode, can we get here???
            if self.tag == None:
                return str(self.value)
            result += self.open_tag_to_html()
            if self.value != None:
                result += self.value
            result += self.close_tag_to_html()
        else:
            result += self.open_tag_to_html()
            if self.value != None:
                result += self.value
            for child in self.children:
                result += str(child)
            result += self.close_tag_to_html()
            
        return result

    def props_to_html(self):
        result = ""
        for k,v in self.props.items():
            result += f' {k}="{v}"'

        return result

    def open_tag_to_html(self):
        result = ""
        if self.tag != None:
            result += f"<{self.tag}"
            result += self.props_to_html()
            result += f">"
        
        return result

    def close_tag_to_html(self):
        if self.tag != None:
            return f"</{self.tag}>"

        return ""

    def __repr__(self):
        return self.to_html()

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if tag == None or tag == "":
            raise ValueError("ParentNode must have tag")
        if children == None or children == []:
            raise ValueError("ParentNode must have children")

        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("ParentNode must have tag")
        if self.children == None or self.children == []:
            raise ValueError("ParentNode must have children")

        return super().to_html()



class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if value == None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")

        return super().to_html()



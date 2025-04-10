class HtmlNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

        assert self.tag != None or self.value != None
        assert self.value != None or self.children != None

    def to_html(self):
        result = ""
        if self.children == None:
            # This is a LeafNode, can we get here???
            if self.tag == None:
                return f"{self.value}"
            result += self.open_tag_to_html()
            if self.value != None:
                result += self.value
            result += self.close_tag_to_html()
        else:
            result += self.open_tag_to_html()
            if self.value != None:
                result += self.value
            for child in self.children:
                result += child.to_html()
            result += self.close_tag_to_html()
            
        return result

    def props_to_html(self):
        props_html = ""
        if self.props:
            for prop in self.props:
                props_html += f' {prop}="{self.props[prop]}"'

        return props_html

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
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if tag == None or tag == "":
            raise ValueError("ParentNode must have tag")
        if children == None or children == []:
            raise ValueError("ParentNode must have children")

        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")

        children_html = []
        for child in self.children:
            children_html.append(child.to_html())


        return f"<{self.tag}{self.props_to_html()}>{"".join(children_html)}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"



class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



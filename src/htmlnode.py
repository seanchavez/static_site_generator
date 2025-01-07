class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_attributes = ""
        for prop in self.props:
            html_attributes += f" {prop}={self.props[prop]}"
        return html_attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value)
        self.props = props

    def to_html(self):
        if not self.value:
            raise (ValueError("LeafNode must have a value"))
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children)
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}>{child_html}</{self.tag}>"

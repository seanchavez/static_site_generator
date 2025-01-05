from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image import split_nodes_image
from split_nodes_link import split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text):
    split_nodes = [TextNode(text, TextType.NORMAL)]
    for delimiter, text_type in [
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
        ("`", TextType.CODE),
    ]:
        split_nodes = split_nodes_delimiter(split_nodes, delimiter, text_type)
    return split_nodes_image(split_nodes_link(split_nodes))

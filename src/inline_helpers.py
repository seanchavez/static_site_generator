import re
from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise (ValueError("Not a valid text type"))


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ("*", "**", "`"):
        return old_nodes
    text_nodes = []
    for node in old_nodes:
        if not node.text or node.text_type != TextType.NORMAL:
            text_nodes.append(node)
        else:
            splits = node.text.split(delimiter)
            new_nodes = []
            for i in range(len(splits)):
                if not splits[i]:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(splits[i], TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(splits[i], text_type))
            text_nodes.extend(new_nodes)
    return text_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
                continue
            remaining_text = node.text
            for image_text, image_url in matches:
                parts = remaining_text.split(
                    f"![{image_text}]({image_url})", maxsplit=1
                )
                if parts[0].strip():
                    new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
                remaining_text = parts[1] if len(parts) > 1 else ""
            if remaining_text.strip():
                new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
                continue
            remaining_text = node.text
            for link_text, link_url in matches:
                parts = remaining_text.split(f"[{link_text}]({link_url})", maxsplit=1)
                if parts[0].strip():
                    new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                remaining_text = parts[1] if len(parts) > 1 else ""
            if remaining_text.strip():
                new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text):
    split_nodes = [TextNode(text, TextType.NORMAL)]
    for delimiter, text_type in [
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
        ("`", TextType.CODE),
    ]:
        split_nodes = split_nodes_delimiter(split_nodes, delimiter, text_type)
    return split_nodes_image(split_nodes_link(split_nodes))

from textnode import TextType, TextNode
from extract_markdown_images import extract_markdown_images


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

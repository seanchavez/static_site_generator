from textnode import TextType, TextNode


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

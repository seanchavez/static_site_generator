from htmlnode import ParentNode
from inline_helpers import text_to_textnodes, text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(None, map(str.strip, blocks)))


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if block.startswith("1. "):
        type = "ordered_list"
    elif block.startswith(("* ", "- ")):
        type = "unordered_list"
    elif block.startswith(">"):
        type = "quote"
    else:
        return "paragraph"
    lines = block.splitlines()
    for n in range(1, len(lines)):
        match type:
            case "ordered_list":
                if not lines[n].startswith(f"{n + 1}. "):
                    return "paragraph"
            case "unordered_list":
                if not lines[n].startswith(("* ", "- ")):
                    return "paragraph"
            case "quote":
                if not lines[n].startswith(">"):
                    return "paragraph"
    return type


def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                level = get_heading_level(block[1:6])
                children.append(
                    ParentNode(f"h{level}", text_to_children(block[level + 1 :]))
                )
            case "code":
                children.append(
                    ParentNode(
                        "pre",
                        [ParentNode("code", text_to_children(block.strip()[3:-3]))],
                    )
                )
            case "ordered_list":
                list_items = []
                for li in block.splitlines():
                    list_items.append(ParentNode("li", text_to_children(li[3:])))
                children.append(ParentNode("ol", list_items))
            case "unordered_list":
                list_items = []
                for li in block.splitlines():
                    list_items.append(ParentNode("li", text_to_children(li[2:])))
                children.append(ParentNode("ul", list_items))
            case "quote":
                children.append(
                    ParentNode(
                        "blockquote",
                        text_to_children(
                            " ".join(
                                map(
                                    lambda line: line.lstrip(">").strip(),
                                    block.splitlines(),
                                )
                            )
                        ),
                    )
                )
            case "paragraph":
                children.append(
                    ParentNode("p", text_to_children(" ".join(block.splitlines())))
                )
    return ParentNode("div", children)


def get_heading_level(prefix):
    level = 1
    for c in prefix:
        if c != "#":
            return level
        level += 1
    return level


def text_to_children(text):
    children = []
    for text_node in text_to_textnodes(text):
        children.append(text_node_to_html_node(text_node))
    return children

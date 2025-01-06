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

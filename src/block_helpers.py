def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(None, map(str.strip, blocks)))

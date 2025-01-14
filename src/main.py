from generate import copy_static, generate_pages_recursive, generate_page


def main():
    copy_static("static/", "public/")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")
    # generate_page(
    #     "content/majesty/index.md", "template.html", "public/majesty/index.html"
    # )


if __name__ == "__main__":
    main()

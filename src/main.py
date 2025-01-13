from generate import copy_static, generate_page


def main():
    copy_static("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()

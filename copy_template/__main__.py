import argparse
import json
import os

from .utils import list_templates, copy_template

data_path = os.path.join(os.path.dirname(__file__), "data.json")

class Config:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                data = json.load(f)
        else:
            data = {}

        return data

    def save(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f)

def main():
    parser = argparse.ArgumentParser(
        prog="copy-template",
        description="Shortcut to Copier"
    )
    parser.add_argument("--author", help="GitHub username")
    parser.add_argument("--repo", help="GitHub repository")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("template", nargs="?", help="Template name")
    parser.add_argument("dst_path", nargs="?", help="Destination path")
    args = parser.parse_args()

    config = Config(data_path)
    data = config.load()

    # config
    if args.author or args.repo:
        if args.author:
            data["author"] = args.author
        if args.repo:
            data["repo"] = args.repo

        config.save(data)
        saved = ", ".join(f"{k}={v}" for k, v in {"author": args.author, "repo": args.repo}.items() if v)
        print(f"saved: {saved}")
        return

    author, repo = data.get("author"), data.get("repo")
    if not (author and repo):
        parser.error("author/repo not set. use --author and --repo")
        return

    # list
    if args.list:
        templates = list_templates(author, repo)
        print("\n".join(templates))
        return

    # template
    if not args.template or not args.dst_path:
        parser.print_help()
        return

    copy_template(author, repo, args.template, args.dst_path)

if __name__ == "__main__":
    main()
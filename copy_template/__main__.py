import argparse
import json
import os

from .utils import list_templates, copy_template

data_path = os.path.join(os.path.dirname(__file__), "data.json")

def load_data(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
    else:
        data = {}

    return data

def save_data(data):
    with open(data_path, "w") as f:
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

    if not any(vars(args).values()):
        parser.print_help()
        return

    data = load_data(data_path)

    if args.author:
        data["author"] = args.author
    if args.repo:
        data["repo"] = args.repo

    if args.author or args.repo:
        save_data(data)
        saved = ", ".join(f"{k}={v}" for k, v in {"author": args.author, "repo": args.repo}.items() if v)
        print(f"saved: {saved}")
        return

    if not data.get("author") or not data.get("repo"):
        print("error: author/repo not set. use --author and --repo")
        return

    if args.list:
        templates = list_templates(data["author"], data["repo"])
        print("\n".join(templates))
        return

    copy_template(data["author"], data["repo"], args.template, args.dst_path)

if __name__ == "__main__":
    main()
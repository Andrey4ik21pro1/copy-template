import argparse
import json
from pathlib import Path

from . import __version__
from .utils import (
    get_app_dir,
    list_templates,
    update_templates,
    copy_template
)

class Config:
    def __init__(self, filename: Path):
        self.filename = filename

    def load(self) -> dict:
        if self.filename.exists():
            try:
                with open(self.filename) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save(self, data: dict) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f)

def main():
    parser = argparse.ArgumentParser(
        prog="copy-template",
        description="Shortcut to Copier"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument("--author", help="GitHub username")
    parser.add_argument("--repo", help="GitHub repository")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--update", action="store_true", help="Clone or pull the templates repository")
    parser.add_argument("template", nargs="?", help="Template name")
    parser.add_argument("dst_path", nargs="?", help="Destination path")
    args = parser.parse_args()

    app_dir = get_app_dir()
    data_path = app_dir / "data.json"

    config = Config(data_path)
    data = config.load()

    # config
    if args.author or args.repo:
        if args.author:
            data["author"] = args.author
        if args.repo:
            data["repo"] = args.repo

        data["templates"] = []

        config.save(data)
        saved = ", ".join(f"{k}={v}" for k, v in {"author": args.author, "repo": args.repo}.items() if v)
        print(f"Saved: {saved}")
        return

    author, repo = data.get("author"), data.get("repo")
    if not (author and repo):
        parser.error("author/repo not set. use --author and --repo")
        return

    templates_dir = app_dir / author / repo

    # update
    if args.update:
        print(f"Updating templates from {author}/{repo}...")
        update_templates(author, repo, templates_dir)

        fresh_templates = list_templates(templates_dir)
        data["templates"] = fresh_templates
        config.save(data)

        print("✓ Templates successfully updated!")
        return

    if not templates_dir.exists():
        parser.error("templates is not downloaded. use --update")
        return

    # list
    if args.list:
        templates = data.get("templates")

        if not templates:
            templates = list_templates(templates_dir)
            data["templates"] = templates
            config.save(data)

        if not templates:
            print("No templates found.")
        else:
            print("\n".join(templates))
        return

    # template
    if not args.template or not args.dst_path:
        parser.print_help()
        return

    templates = data.get("templates") or list_templates(templates_dir)

    if args.template not in templates:
        parser.error(f"template '{args.template}' not found.")
        if templates:
            print("Available templates:\n  " + "\n  ".join(templates))
        return

    copy_template(templates_dir, args.template, args.dst_path)

if __name__ == "__main__":
    main()
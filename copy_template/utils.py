import subprocess
import shutil
from pathlib import Path
from copier import run_copy
from platformdirs import user_data_path

def clone_repo(author: str, repo: str, dst_path: str) -> None:
    repo_url = f"https://github.com/{author}/{repo}.git"
    subprocess.run(
        ["git", "clone", "--quiet", repo_url, dst_path],
        check=True
    )

def pull_repo(dst_path: str) -> None:
    subprocess.run(
        ["git", "pull", "--quiet"],
        cwd=dst_path,
        check=True
    )

def get_app_dir() -> Path:
    return user_data_path(appname="copy-template", appauthor=False, ensure_exists=True)

def list_templates(templates_dir: Path) -> list[str]:
    if not templates_dir.exists():
        return []

    return [d.name for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith(".")] # list

def update_templates(author: str, repo: str, templates_dir: Path) -> None:
    if templates_dir.exists() and not templates_dir.joinpath(".git").exists():
        shutil.rmtree(templates_dir)

    if templates_dir.joinpath(".git").exists():
        pull_repo(str(templates_dir))
    else:
        templates_dir.parent.mkdir(parents=True, exist_ok=True)
        clone_repo(author, repo, str(templates_dir))

def copy_template(templates_dir: Path, template: str, dst_path: str) -> None:
    template_dir = templates_dir / template

    run_copy(
        src_path=str(template_dir),
        dst_path=dst_path,
        unsafe=True
    )
from copier import run_copy
import subprocess
import tempfile

def download_repo(author, repo, dst_path):
    repo_url = f"https://github.com/{author}/{repo}.git"
    subprocess.run(
        ["git", "clone", "--quiet", repo_url, dst_path],
        check=True
    )

def list_templates(author, repo):
    with tempfile.TemporaryDirectory() as dir:
        download_repo(author, repo, dir)

        output = subprocess.check_output(
            ["git", "ls-tree", "--name-only", "-d", "HEAD"],
            cwd=dir,
            text=True
        )
        list = [f for f in output.splitlines() if not f.startswith(".")]
        return list # list

def copy_template(author, repo, template, dst_path):
    with tempfile.TemporaryDirectory() as dir:
        download_repo(author, repo, dir)

        run_copy(
            src_path=f"{dir}/{template}",
            dst_path=dst_path,
            unsafe=True
        )
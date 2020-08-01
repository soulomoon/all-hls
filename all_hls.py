import gzip
import json
import os
import platform
import shutil
import sys
import urllib.request
from pathlib import Path

cache_folder = Path("cache/")


def download(bin_dir: Path):
    github_os = get_github_os_version()
    if not github_os:
        print(f"os not support binary: {github_os}")
        exit(1)
    github_os = get_github_os_version()
    if not github_os:
        print("release os not supported")
        exit(1)

    with urllib.request.urlopen("https://api.github.com/repos/haskell/haskell-language-server/releases") as fd:
        releases = json.loads(fd.read().decode())
        release = next(obj for obj in releases if not obj["prerelease"])
        assets = [a["browser_download_url"] for a in release["assets"] if github_os in a["name"]]
        path_list = []
        for link in assets:
            file_path = download_file(link)
            path_list.append(file_path)
            print(f"download success: {file_path}")
        # copy them to bin dir
        for path in path_list:
            # remove os
            name = path.name.replace(f"-{github_os}", "")
            # windows need exe
            if github_os == "Windows":
                name += ".exe"
            shutil.copy2(path, bin_dir.joinpath(name))


def download_file(link: str) -> Path:
    os.makedirs(cache_folder, exist_ok=True)
    local_filename = cache_folder.joinpath(link.split("/")[-1])
    # remove its suffix
    unzip_filename = local_filename.parent.joinpath(local_filename.stem)
    if unzip_filename.exists():
        return unzip_filename
    _, headers = urllib.request.urlretrieve(link, local_filename)
    with gzip.open(local_filename, 'rb') as f:
        with open(unzip_filename, 'wb') as f_out:
            shutil.copyfileobj(f, f_out)
            os.chmod(unzip_filename, 0o775)
    os.remove(local_filename)
    return unzip_filename


def get_github_os_version():
    pf = platform.system().lower()
    os_table = {
        "darwin": "macOS",
        "linux": "Linux",
        "windows": "Windows",
    }
    if pf not in os_table:
        return None
    return os_table[pf]


def main():
    if len(sys.argv) < 2:
        print("need to specify binary dir")
        exit(1)
    bin_dir = Path(sys.argv[1])
    if not bin_dir.is_dir():
        print("binary dir path is not a directory")
        exit(1)
    download(bin_dir)


if __name__ == "__main__":
    main()

import gzip
import json
import os
import platform
import shutil
import tempfile
import urllib.request


def download():
    github_os = get_github_os_version()
    if not github_os:
        print(f"os not support binary: {github_os}")
        exit(1)
    github_os = get_github_os_version()
    # for ghc_version in inversions:
    # serverName = f"haskell-language-server-{tag_name}-{github_os}-${ghcVersion}${exe_ext}"
    if not github_os:
        print("release os not supported")
        exit(1)

    tmp = tempfile.gettempdir()

    with urllib.request.urlopen("https://api.github.com/repos/haskell/haskell-language-server/releases") as fd:
        releases = json.loads(fd.read().decode())
        release = next(obj for obj in releases if not obj["prerelease"])
        assets = [a["browser_download_url"] for a in release["assets"] if github_os in a["name"]]
        # wrapper_link = next(obj for obj in assets if "wrapper" in obj)
        # print(f"download success: {download_file(wrapper_link)}")
        for link in assets:
            print(f"download success: {download_file(link)}")


def download_file(link: str) -> str:
    folder = "data/"
    os.makedirs(folder, exist_ok=True)
    local_filename, headers = urllib.request.urlretrieve(link, folder + link.split("/")[-1])
    unzip_filename = ".".join(local_filename.split(".")[:-1])
    with gzip.open(local_filename, 'rb') as f:
        with open(unzip_filename, 'wb') as f_out:
            shutil.copyfileobj(f, f_out)
            os.chmod(unzip_filename, 0o775)
    os.remove(local_filename)
    return unzip_filename

def get_github_os_version():
    pf = platform.system().lower()
    if pf == "darwin":
        return "macOS"
    elif pf == "linux":
        return "Linux"
    elif pf == "windows":
        return "Windows"
    else:
        return None


if __name__ == "__main__":
    download()

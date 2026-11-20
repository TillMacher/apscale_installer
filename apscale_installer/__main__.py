import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import requests
from tqdm import tqdm

TOOLS = {
    "Windows": [
        ("blast+", "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.16.0/ncbi-blast-2.16.0+-x64-win64.tar.gz"),
        ("vsearch", "https://github.com/torognes/vsearch/releases/download/v2.30.0/vsearch-2.30.0-win-x86_64.zip"),
        ("swarm", "https://github.com/torognes/swarm/releases/download/v3.1.5/swarm-3.1.5-win-x86_64.zip"),
    ],
    "Darwin": [
        # blast+ is only available for Intel Macs (runs on Apple Silicon via Rosetta)
        ("blast+", "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.16.0/ncbi-blast-2.16.0+-x64-macosx.tar.gz"),
        # "universal" builds run natively on Intel and Apple Silicon
        ("vsearch", "https://github.com/torognes/vsearch/releases/download/v2.30.0/vsearch-2.30.0-macos-universal.tar.gz"),
        ("swarm", "https://github.com/torognes/swarm/releases/download/v3.1.5/swarm-3.1.5-macos-universal.tar.gz"),
    ],
}


def env_bin():
    """Return the bin folder of the conda environment that runs this script."""
    return Path(sys.prefix) / "bin"


def download(url, file_name):
    """Download a file with a tqdm progress bar."""
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with open(file_name, "wb") as file, tqdm(
                total=total, unit="B", unit_scale=True, unit_divisor=1024, desc="Downloading", leave=False
        ) as bar:
            for chunk in response.iter_content(chunk_size=256 * 1024):
                bar.update(file.write(chunk))


def install(name, url, env_path):
    file_name = url.split("/")[-1]

    # Folder name inside the archive (blast+ unpacks to e.g. "ncbi-blast-2.16.0+")
    if name == "blast+":
        folder = file_name.split("+-")[0] + "+"
    else:
        folder = file_name
        for ext in (".tar.gz", ".tgz", ".tar.bz2", ".tar.xz", ".zip"):
            folder = folder.removesuffix(ext)

    # Work in a temporary folder, so nothing is left behind if something fails
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp, file_name)
        download(url, archive)
        shutil.unpack_archive(archive, tmp)

        bin_files = [f for f in Path(tmp, folder, "bin").glob("*") if f.is_file()]
        if not bin_files:
            raise RuntimeError(f"no program files found in {file_name}")

        for file in bin_files:
            target = env_path / file.name
            shutil.copy(file, target)
            target.chmod(target.stat().st_mode | 0o755)  # make sure it is executable

    print(f"  [ok] {name}: {len(bin_files)} files installed")


def main():
    tools = TOOLS.get(platform.system())

    print('Welcome to the APSCALE installer!\n')
    print('The following tools will be installed into your current conda environment:')
    print('  - blast+\n  - vsearch\n  - swarm\n  - playwright (browser for BOLDigger3)\n')

    # "-y" skips the question (used by the automatic installers)
    if "-y" not in sys.argv:
        while True:
            response = input('Proceed ([y]/n)?: ').strip().lower()
            if response in ('', 'y', 'n'):
                break
            print('Please type y or n.')

        if response == 'n':
            print('Installation cancelled.')
            return

    failed = []

    if tools:
        env_path = env_bin()
        env_path.mkdir(parents=True, exist_ok=True)
        print(f"Installing to: {env_path}\n")

        for name, url in tools:
            print(name)
            try:
                install(name, url, env_path)
            except Exception as error:
                print(f"  [x] {name} could not be installed: {error}")
                failed.append(name)
    else:
        print("Linux: please install blast+, vsearch and swarm with conda:")
        print("  conda install -c bioconda blast vsearch swarm\n")

    # boldigger3 needs the playwright browsers
    print("playwright")
    result = subprocess.run([sys.executable, "-m", "playwright", "install"])
    if result.returncode == 0:
        print("  [ok] playwright: browsers installed")
    else:
        print("  [x] playwright: browsers could not be installed")
        failed.append("playwright")

    if failed:
        print(f"\nFinished with problems. Not installed: {', '.join(failed)}")
        print("Check your internet connection and run 'apscale_installer' again.")
        sys.exit(1)

    print("\nAll done!")


if __name__ == "__main__":
    main()

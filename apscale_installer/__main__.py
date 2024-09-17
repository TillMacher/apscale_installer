import glob
import shutil
import requests
import os
import tarfile
import subprocess
import json
import platform
from pathlib import Path

def download_blast(url, file_name):
    ########################################################################################################################
    ## Download

    ## download the tar.gz file
    response = requests.get(url)
    with open(file_name, "wb") as file:
        file.write(response.content)

    print("Download complete!")

    ########################################################################################################################
    ## Extract

    extract_path = os.path.dirname(file_name)

    # Extract the file based on its extension
    if file_name.endswith('.tar.gz') or file_name.endswith('.tgz'):
        shutil.unpack_archive(file_name, extract_path, 'gztar')
        folder = file_name.replace('.tar.gz', '').replace('.tgz', '')
    elif file_name.endswith('.tar.bz2') or file_name.endswith('.tbz'):
        shutil.unpack_archive(file_name, extract_path, 'bztar')
        folder = file_name.replace('.tar.bz2', '').replace('.bztar', '')
    elif file_name.endswith('.tar.xz') or file_name.endswith('.txz'):
        shutil.unpack_archive(file_name, extract_path, 'xztar')
        folder = file_name.replace('.tar.xz', '').replace('.xztar', '')
    elif file_name.endswith('.zip'):
        shutil.unpack_archive(file_name, extract_path, 'zip')
        folder = file_name.replace('.zip', '')

    print("Unpacking complete!")

    ########################################################################################################################
    ## Find install directory

    print(os.environ['PATH'])

    # Run the conda info command
    result = subprocess.run('conda info --json', shell=True, stdout=subprocess.PIPE)
    # Parse the JSON output
    conda_info = json.loads(result.stdout)
    # Get the current environment path
    env_path = Path(conda_info['default_prefix'] + '/bin')
    print(f'Installing to: {env_path}')

    ## create bin folder if necessary
    os.makedirs(env_path, exist_ok=True)

    ########################################################################################################################
    ## Move files to bin

    # Collect files
    folder = file_name.split('+-')[0] + '+'
    bin_files = glob.glob(str(Path(f'./{extract_path}/{folder}/bin/*')))

    # Move files
    for file in bin_files:
        moved_file = env_path.joinpath(Path(file).name)
        shutil.copy(file, moved_file)
    print("Copied files!")

    ########################################################################################################################
    ## Update PATH

    os.environ["PATH"] += os.pathsep + str(env_path)
    print("Finished installation!")

def download_vsearch(url, file_name):
    ########################################################################################################################
    ## Download

    ## download the tar.gz file
    response = requests.get(url)
    with open(file_name, "wb") as file:
        file.write(response.content)

    print("Download complete!")

    ########################################################################################################################
    ## Extract

    extract_path = os.path.dirname(file_name)

    # Extract the file based on its extension
    if file_name.endswith('.tar.gz') or file_name.endswith('.tgz'):
        shutil.unpack_archive(file_name, extract_path, 'gztar')
        folder = file_name.replace('.tar.gz', '').replace('.tgz', '')
    elif file_name.endswith('.tar.bz2') or file_name.endswith('.tbz'):
        shutil.unpack_archive(file_name, extract_path, 'bztar')
        folder = file_name.replace('.tar.bz2', '').replace('.bztar', '')
    elif file_name.endswith('.tar.xz') or file_name.endswith('.txz'):
        shutil.unpack_archive(file_name, extract_path, 'xztar')
        folder = file_name.replace('.tar.xz', '').replace('.xztar', '')
    elif file_name.endswith('.zip'):
        shutil.unpack_archive(file_name, extract_path, 'zip')
        folder = file_name.replace('.zip', '')

    print("Unpacking complete!")

    ########################################################################################################################
    ## Find install directory

    # Run the conda info command
    result = subprocess.run('conda info --json', shell=True, stdout=subprocess.PIPE)
    # Parse the JSON output
    conda_info = json.loads(result.stdout)
    # Get the current environment path
    env_path = Path(conda_info['default_prefix'] + '/bin')
    print(f'Installing to: {env_path}')

    ## create bin folder if necessary
    os.makedirs(env_path, exist_ok=True)

    ########################################################################################################################
    ## Move files to bin

    # Collect files
    bin_files = glob.glob(str(Path(f'./{extract_path}/{folder}/bin/*')))

    # Move files
    for file in bin_files:
        moved_file = env_path.joinpath(Path(file).name)
        shutil.copy(file, moved_file)
    print("Copied files!")

    ########################################################################################################################
    ## Update PATH

    os.environ["PATH"] += os.pathsep + str(env_path)
    print("Finished installation!")

def main():
    ## OS-specific download
    current_os = platform.system()

    if current_os == "Windows":
        # blastn+
        print('\nInstalling blast+:')
        url = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.16.0/ncbi-blast-2.16.0+-x64-win64.tar.gz"
        file_name = url.split('/')[-1]
        download_blast(url, file_name)

        ## vsearch
        print('\nInstalling vsearch:')
        url = 'https://github.com/torognes/vsearch/releases/download/v2.28.1/vsearch-2.28.1-win-x86_64.zip'
        file_name = url.split('/')[-1]
        download_vsearch(url, file_name)

    elif current_os == "Darwin":
        # blastn+
        print('\nInstalling blast+:')
        url = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.16.0/ncbi-blast-2.16.0+-x64-macosx.tar.gz"
        file_name = url.split('/')[-1]
        download_blast(url, file_name)

        ## vsearch
        print('\nInstalling vsearch:')
        url = 'https://github.com/torognes/vsearch/releases/download/v2.28.1/vsearch-2.28.1-macos-aarch64.tar.gz'
        file_name = url.split('/')[-1]
        download_vsearch(url, file_name)

if __name__ == "__main__":
    main()

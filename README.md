# Apscale Installer

## Installation Tutorial for the Apscale Metabarcoding Workflow

### Introduction

The easiest way to install the apscale metabarcoding workflow is by using [Miniconda3](https://docs.anaconda.com/miniconda/#). Miniconda will create an isolated environment with all the suggested versions of each tool.

> **Note:** Currently, [vsearch](https://github.com/torognes/vsearch) and [blast+](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html) cannot be automatically installed via conda. For now, the easiest solution is the installation through the apscale-installer script. We will update this Wiki when vsearch and blast+ are available via conda. Linux users can install vsearch and blast+ already now using conda.

This tutorial will install the following tools:
* [Apscale](https://github.com/DominikBuchner/apscale)
* [Apscale_blast](https://github.com/TillMacher/apscale_blast)
* [Boldigger2](https://github.com/DominikBuchner/BOLDigger2)
* [Demultiplexer](https://github.com/DominikBuchner/demultiplexer)
* TaxonTableTool2 (coming soon)

### Miniconda Installation

1. Install Miniconda by following the instructions.

2. Open a new Anaconda (Miniconda3) terminal.
   - **Windows**: Type 'Anaconda' in your search bar and select 'Anaconda Powershell Prompt (miniconda3)'.
   - **MacOS**: Open a new terminal. You will see the (base) environment before your user name.

3. Download the respective environment installation file for [Windows](https://github.com/TillMacher/apscale_installer/blob/main/environments/metabarcoding_env_windows_x64.yml) or [MacOS](https://github.com/TillMacher/apscale_installer/blob/main/environments/metabarcoding_env_macos_aarch64.yml).

5. Install the metabarcoding environment by typing:
   ```sh
   conda env create -f environment_XXX.yml
   
6. Ensure you provide the correct path, for example:
   ```sh
   conda env create -f /Users/tillmacher/Downloads/metabarcoding_env_macos_aarch64.yml
   
7. This should automatically install all dependencies. After the installation, activate the environment:
   ```sh
   conda activate metabarcoding

8. For Windows and MacOS users run the apscale-installer script:
   ```sh
   apscale_installer

9. For Linux and MacOS (intel) users can use conda:
   ```sh
   conda install vsearch
   conda install blast

10. Verify your installations:
   ```sh
   vsearch --help
   blastn -h

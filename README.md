# apscale_installer

## Installation tutorial for the apscale metabarcoding workflow
### Introduction

The easiest way to install the apscale metabarcoding workflow is by using [Miniconda3](https://docs.anaconda.com/miniconda/).
Miniconda will create an isolated environment with all the suggested versions of each tool.

Currently, [vsearch](https://github.com/torognes/vsearch) and [blast+](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html) cannot be automatically installed via conda. For now, the easiest solution is the installation through the apscale-installer script. We will update this Wiki when vsearch and blast+ will be available via conda. Linux users can install vsearch and blast+ already now using conda.

This tutorial will install the following tools:
* [Apscale](https://github.com/DominikBuchner/apscale)
* [Apscale_blast](https://github.com/TillMacher/apscale_blast)
* [Boldigger2](https://github.com/DominikBuchner/BOLDigger2)
* [Demultiplexer](https://github.com/DominikBuchner/demultiplexer)
* TaxonTableTool2 (comming soon)

### Miniconda installation

* Install [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) by following the instructions.
* Open a new Anaconda (Miniconda3) terminal.
* Windows: Simply type 'Anaconda' in your search bar and select 'Anaconda Powershell Prompt (miniconda3)'.
* MacOS: Open a new terminal. You will see the (base) environment before your user name.
* Download the respective environment installation file for [Windows](https://github.com/TillMacher/apscale_installer/blob/main/environments/metabarcoding_env_windows_x64.yml) or [MacOS](https://github.com/TillMacher/apscale_installer/blob/main/environments/metabarcoding_env_macos_aarch64.yml).
* Install the metabarcoding environment by typing:

  `conda env create -f environment_XXX.yml` (replace the XXX with your specific version).

* Make sure that you provide the correct path, for example:

  `conda env create -f /Users/tillmacher/Downloads/metabarcoding_env_macos_aarch64.yml`

* This should automatically install all dependencies. After the installation, activate the environment:

  `conda activate metabarcoding`

* For Windows and MacOS users run the apscale-installer script:

  `apscale_installer`

* This will automatically download vsearch and blast+ and add them to your PATH.
* Verify your installations:

  `vsearch --help`
  
  `blastn -h`





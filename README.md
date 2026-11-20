# APSCALE Installer

Install the complete APSCALE DNA metabarcoding toolbox with a **double-click**, on Windows and macOS.

The installer creates a conda environment called `apscale4` (Python 3.12) with:

* [APSCALE](https://github.com/DominikBuchner/apscale) – raw-data processing
* [APSCALE-GUI](https://github.com/TillMacher/apscale_gui) – graphical interface for APSCALE
* [APSCALE-blast](https://github.com/TillMacher/apscale_blast) – taxonomic assignment
* [APSCALE-Nanopore](https://github.com/TillMacher/apscale_nanopore) – Nanopore metabarcoding
* [BOLDigger3](https://github.com/DominikBuchner/BOLDigger3) – BOLD identification engine
* [Demultiplexer2](https://github.com/DominikBuchner/demultiplexer2) – demultiplexing
* the command-line tools **vsearch**, **swarm** and **blast+**

A second installer sets up [TaxonTableTools2](https://github.com/TillMacher/TaxonTableTools2) in its own environment called `TTT`.

> **News (22.08.2025):** APSCALE4 is now part of APSCALE-GUI. The old `apscale` environment (Python 3.10) is outdated – please switch to `apscale4`. See [Removing the old environment](#removing-the-old-environment).

---

## Quick start (recommended)

### Step 1 – Install Miniconda (once)

Download and install Miniconda for your system:

* **Windows:** [Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
* **macOS (Apple Silicon, M1–M4):** [Miniconda3-latest-MacOSX-arm64.pkg](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg)
* **macOS (Intel):** [Miniconda3-latest-MacOSX-x86_64.pkg](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg)
* All other versions: [Miniconda download page](https://www.anaconda.com/download/success?reg=skipped)

Use the default settings. If you already have Miniconda or Anaconda, skip this step.

### Step 2 – Download the installers

Download **[env_installers.zip](https://github.com/TillMacher/apscale_installer/raw/main/env_installers.zip)** and unzip it.
It contains:

| System  | APSCALE                        | TaxonTableTools2           |
|---------|--------------------------------|----------------------------|
| Windows | `W11/Install_apscale4.bat`     | `W11/Install_TTT.bat`      |
| macOS   | `Mac/Install_apscale4.command` | `Mac/Install_TTT.command`  |

> Please download the **zip file**. A single `.command` file downloaded through the browser loses its permission to run on macOS.

### Step 3 – Run the installer

**Windows:** double-click `Install_apscale4.bat`.
If Windows shows *"Windows protected your PC"*, click **More info → Run anyway**.

**macOS:** double-click `Install_apscale4.command`.
If macOS says the file *"cannot be opened"*, **right-click → Open → Open**.
(Alternative: open Terminal and type `bash ` followed by dragging the file into the window, then press Enter.)

The installer will

1. find your Miniconda installation,
2. ask you to confirm (type `y`),
3. download the latest environment file and create the `apscale4` environment,
4. install vsearch, swarm, blast+ and the browser needed by BOLDigger3,
5. check that everything works.

This takes about **5–15 minutes** and needs about **3 GB** of disk space and an internet connection.

### Step 4 – Start APSCALE

Open a new terminal
(**Windows:** search for *"Anaconda Powershell Prompt (miniconda3)"*; **macOS:** open *Terminal*) and type:

```sh
conda activate apscale4
apscale_gui
```

For TaxonTableTools2:

```sh
conda activate TTT
taxontabletools2
```

---

## Updating

Simply **run the installer again**. It detects the existing environment and updates all packages to the latest version.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| *"Miniconda was not found"* | Install Miniconda (Step 1). If it is installed in an unusual folder, start the installer from the Anaconda Prompt / a terminal where `conda` works. |
| The installation stopped with an error | Check your internet connection and run the installer again. It continues where it stopped. |
| `blastn` does not start on a Mac with Apple Silicon (M1/M2/M3/M4) | blast+ is only available for Intel Macs and needs Rosetta. Install it once in Terminal: `softwareupdate --install-rosetta --agree-to-license` |
| vsearch, swarm or blast+ is missing | Activate the environment and run `apscale_installer` again. |
| Check if the tools work | `conda activate apscale4`, then `vsearch --version`, `swarm --version`, `blastn -version` |
| `apscale_gui` stops with `TypeError: UpdateChecker.check() takes 1 positional argument but 3 were given` | Your APSCALE-GUI is outdated. Run the installer again to update everything (or `pip install --upgrade apscale_gui apscale_nanopore` in the activated environment). |
| `ModuleNotFoundError: No module named '...'` (e.g. `stqdm`) | Run the installer again. Quick fix: `pip install <module name>` in the activated environment. |
| `RequestsDependencyWarning: urllib3 ... or chardet ... doesn't match a supported version` | Only a warning. To remove it: `pip install --upgrade requests urllib3 charset-normalizer "chardet<6"` in the activated environment. |
| APSCALE-GUI opens in Edge / another browser than expected | APSCALE-GUI always opens in your **default** browser. Change the default browser in your system settings, or copy the address shown in the terminal (e.g. `http://localhost:8501`) into the browser you want. |
| I don't want the Playwright browsers | They are only needed by BOLDigger3. Remove them with `playwright uninstall --all` in the activated environment (BOLDigger3 will then not work). |

---

## Removing the old environment

The old `apscale` environment (Python 3.10) is no longer supported. To delete it:

```sh
conda remove -n apscale --all
```

---

## Manual installation (advanced)

Only needed if the automatic installer does not work for you, or if you use **Linux**.

<details>
<summary>Option A – from the environment file</summary>

1. Download [apscale_env.yml](https://github.com/TillMacher/apscale_installer/raw/main/environments/apscale_env.yml).
2. Open the Anaconda Prompt (Windows) or Terminal (macOS/Linux), go to the folder where you saved the file, and create the environment:

   ```sh
   cd Downloads
   conda env create -f apscale_env.yml
   conda activate apscale4
   ```

   Alternatively, give the full path to the file, e.g. `conda env create -f "C:\Users\<you>\Downloads\apscale_env.yml"` (Windows) or `conda env create -f ~/Downloads/apscale_env.yml` (macOS/Linux).

3. Install vsearch, swarm, blast+ and the BOLDigger3 browser:
   * **Windows / macOS:**
     ```sh
     apscale_installer
     ```
   * **Linux:**
     ```sh
     conda install -c bioconda vsearch swarm blast
     playwright install
     ```

</details>

<details>
<summary>Option B – with pip</summary>

```sh
conda create -n apscale4 python=3.12 ipython
conda activate apscale4
pip install apscale apscale_gui apscale_blast apscale_nanopore boldigger3 demultiplexer2 apscale_installer
apscale_installer
```

Linux users replace the last line with the Linux commands from Option A, step 3.

</details>

<details>
<summary>What does the <code>apscale_installer</code> command do?</summary>

vsearch, swarm and blast+ are not available through conda on every system. `apscale_installer` downloads the official
releases and copies them into the active conda environment, so they are available whenever the environment is active.
It also installs the browser that BOLDigger3 needs (`playwright install`). Use `apscale_installer -y` to skip the confirmation question.

</details>

---

## Usage

See the documentation of each program:

* [APSCALE](https://github.com/DominikBuchner/apscale/tree/main?tab=readme-ov-file#how-to-use)
* [APSCALE-GUI](https://github.com/TillMacher/apscale_gui)
* [APSCALE-blast](https://github.com/TillMacher/apscale_blast?tab=readme-ov-file#how-to-use)
* [APSCALE-Nanopore](https://github.com/TillMacher/apscale_nanopore)
* [BOLDigger3](https://github.com/DominikBuchner/BOLDigger3?tab=readme-ov-file#installation-and-usage)
* [Demultiplexer2](https://github.com/DominikBuchner/demultiplexer2)
* [TaxonTableTools2](https://github.com/TillMacher/TaxonTableTools2)

## Video tutorial

A [YouTube tutorial](https://www.youtube.com/watch?v=c6pm0FhcINI) shows the installation on Windows and macOS
(recorded with the older manual installation).

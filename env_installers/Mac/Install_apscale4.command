#!/usr/bin/env bash
# Double-click this file in Finder to install the apscale4 conda environment.
# Linux: run "bash <this file>" in a terminal.

# --------------------------------------------------------------------------
#  Settings
# --------------------------------------------------------------------------
ENV_NAME="apscale4"
ENV_URL="https://raw.githubusercontent.com/TillMacher/apscale_installer/main/environments/apscale_env.yml"
POST_CMD="apscale_installer -y"
CHECK_MODULE="apscale"
START_CMD="apscale_gui"
DISK_SPACE="3 GB"
TOOLS="APSCALE, APSCALE-GUI, APSCALE-blast, BOLDigger3, Demultiplexer2"

fail() {
    echo
    echo "[x] $1"
    echo
    echo "Installation did not complete."
    read -r -p "Press Enter to close this window..."
    exit 1
}

echo "============================================================"
echo "  Installing the $ENV_NAME conda environment"
echo "============================================================"
echo

# --------------------------------------------------------------------------
#  1. Find Miniconda / Anaconda
# --------------------------------------------------------------------------
ROOT=""
if [ -n "$CONDA_EXE" ] && [ -x "$CONDA_EXE" ]; then
    ROOT="$(cd "$(dirname "$CONDA_EXE")/.." && pwd)"
fi
for d in "$HOME/miniconda3" "$HOME/anaconda3" "$HOME/miniforge3" "$HOME/opt/miniconda3" "$HOME/opt/anaconda3" \
         "/opt/miniconda3" "/opt/anaconda3" \
         "/opt/homebrew/Caskroom/miniconda/base" "/usr/local/Caskroom/miniconda/base" \
         "/opt/homebrew/Caskroom/miniforge/base" "/usr/local/Caskroom/miniforge/base"; do
    if [ -z "$ROOT" ] && [ -f "$d/etc/profile.d/conda.sh" ]; then
        ROOT="$d"
    fi
done
[ -n "$ROOT" ] || fail "Miniconda was not found. Please install Miniconda first:
    Apple Silicon (M1-M4): https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg
    Intel:                 https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg"

echo "[+] Found conda in: $ROOT"

# --------------------------------------------------------------------------
#  Disclaimer
# --------------------------------------------------------------------------
echo
echo "------------------------------------------------------------"
echo "  Before you continue"
echo "------------------------------------------------------------"
echo "  This will install: $TOOLS"
echo
echo "  Disk space needed:  about $DISK_SPACE"
echo "  Install location:   $ROOT/envs/$ENV_NAME"
echo "  Internet:           required during the installation"
echo "  Duration:           about 5-15 minutes"
echo
echo "  The software is provided \"as is\", without warranty of any kind."
echo "------------------------------------------------------------"
echo
while true; do
    read -r -p "Do you want to continue? [y/n]: " answer
    case "$answer" in
        [Yy]|[Yy][Ee][Ss]) break ;;
        [Nn]|[Nn][Oo])
            echo
            echo "Installation cancelled. Nothing was changed."
            echo
            read -r -p "Press Enter to close this window..."
            exit 0 ;;
        *) echo "Please type y or n." ;;
    esac
done
echo
# shellcheck disable=SC1091
source "$ROOT/etc/profile.d/conda.sh"

# --------------------------------------------------------------------------
#  2. Download the latest environment file
# --------------------------------------------------------------------------
YML="${TMPDIR:-/tmp}/${ENV_NAME}_env.yml"
echo "[+] Downloading the environment file..."
curl -fsSL "$ENV_URL" -o "$YML" || fail "Download failed. Please check your internet connection."

# --------------------------------------------------------------------------
#  3. Create or update the environment
# --------------------------------------------------------------------------
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "[+] The environment already exists. Updating it. This can take a few minutes..."
    echo
    conda env update -n "$ENV_NAME" -f "$YML" --prune || fail "Updating the environment failed. See the messages above. Tip: simply run the installer again."
else
    echo "[+] Creating the environment. This can take 5-15 minutes..."
    echo
    conda env create -n "$ENV_NAME" -f "$YML" || fail "Creating the environment failed. See the messages above. Tip: simply run the installer again."
fi

# --------------------------------------------------------------------------
#  4. Extra setup step (optional)
# --------------------------------------------------------------------------
if [ -n "$POST_CMD" ]; then
    echo
    echo "[+] Running: $POST_CMD"
    # shellcheck disable=SC2086
    conda run --no-capture-output -n "$ENV_NAME" $POST_CMD || echo "[!] \"$POST_CMD\" reported a problem. See the messages above."
fi

# --------------------------------------------------------------------------
#  5. Check the installation
# --------------------------------------------------------------------------
conda run -n "$ENV_NAME" python -c "import $CHECK_MODULE" >/dev/null 2>&1 \
    || fail "The environment was created, but $CHECK_MODULE could not be loaded."

rm -f "$YML"
echo
echo "============================================================"
echo "  Done! The $ENV_NAME environment is ready."
echo
echo "  To start, open a new Terminal window and type:"
echo
echo "      conda activate $ENV_NAME"
echo "      $START_CMD"
echo "============================================================"
echo
read -r -p "Press Enter to close this window..."

# 5CM522 Coursework Setup Guide

This README only covers what you need to get up and running:
- software installation
- environment setup
- which files matter
- what data gets generated

---

## ⚠️ Important: What to Edit

**Only edit `notebook.ipynb`**.

All other files are:
- `generate_data.py` — do not modify
- `environment.yml` — do not modify
- `base_data/`, `README.md` — reference only

Do not rename any files or create new files. 

---

## 1) Install required software

### VS Code
Install Visual Studio Code:
- https://code.visualstudio.com/

### Conda (Anaconda or Miniconda)

**Option A: If you already have Anaconda installed** ✅
- Skip this step, use your existing installation
- Anaconda includes everything you need

**Option B: If you don't have Conda installed** 
- Download Miniconda (lightweight alternative to Anaconda):
- https://docs.conda.io/en/latest/miniconda.html
- Miniconda works on Windows, macOS, Linux (no admin rights needed)

---

## 2) Create the environment

Even if you have full Anaconda, **create an isolated environment** from the provided `environment.yml`:
- Keeps your work separate from other projects
- Ensures reproducibility
- Prevents package conflicts
- Installs all packages, including a MIP solver

Open Anaconda Prompt on your computer and then navigate to the local repository (folder).

For example, if your folder was stored at `C:\Users\<your-name>\Documents\GitHub\5cm522-or-cw-2-<your-github-username>` then you would enter the following into the prompt to change directories (cd).

```bash
cd C:\Users\<your-name>\Documents\GitHub\5cm522-or-cw-2-<your-github-username>
```

Then enter the following command. Please note that this will take about 5-10 minutes to complete, go and make a cup of tea! Please just let it complete, do not close down the prompt.

```bash
conda env create -f environment.yml
```

- Then open `notebook.ipynb` in VS Code.
- Click "Select Kernel" in the top right corner
- Click "Install/Enable suggested extensions Python + Jupyter
- Once installed, click "Select Kernel" again
- Click "Python Environments..."
- Select 5cm522

---

> **Just want to look before setting up?** This notebook also runs on the course website
> (<https://invariantum.github.io/operational_research/>, folder
> `Assignments/02-coursework-part-b/starter`) with nothing to install.
> Do your coursework here in your own repository, though: work done on the website is not saved to GitHub.

---

## 3) What you need to do first

At the top of `notebook.ipynb`, set:

```python
STUDENT_ID = "XXXXXXXX"
```

Replace with your own student number, then run the first cell to generate your personalised dataset.

---

## 4) Files in this repository

**You edit:**
- `notebook.ipynb` ← Your working file

**Provided (do not edit):**
- `generate_data.py` — creates your personalised data
- `environment.yml` — conda environment definition
- `base_data/` — base input data used by generate_data.py
- `README.md` — setup instructions

---

## 5) Data generated after running the first notebook cell

Running data generation creates a `data/` folder with:

- `zones.csv`: Zone features and `historical_sales` (with missing values to forecast)
- `stores.csv`: Store locations, capacities, and opening costs
- `zone_store_dist.csv`: Distance matrix between each zone and store
- `margins.json`: Economic parameters (`margin_per_unit`, `service_cost_per_km`)
- `manifest.json`: Metadata for reproducibility

---

## 6) Quick troubleshooting

- **Kernel not visible**: Restart VS Code, then select interpreter/kernel `5cm522` again.
- **Environment already exists but broken**:

```bash
conda env remove -n 5cm522
conda env create -f environment.yml
```

- **Other issues**: Speak with Dr O'Neill. It is your responsibility to get your environment set up. If in doubt, please ask.
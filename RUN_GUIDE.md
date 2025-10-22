# Getting Started

## 1. Clone the Repository
```bash
git clone https://github.com/justin9668/cs506-final-project
cd cs506-final-project
````

## 2. Create and Activate a Python Environment

Using conda:

```bash
conda create -n nba python=3.11 -y
conda activate nba
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.1 Install Kernel (for running notebooks on VSCode)

```bash
pip install ipykernel
python -m ipykernel install --user --name nba --display-name "Python (nba)"
```

## 4. Pull Raw NBA Data

This step downloads the 2023–24 regular season game logs via the NBA API.

```bash
make pull SEASON="2023-24"
```

**Output file created:** `data/raw/team_gamelogs.csv`
If there’s a timeout warning, just re-run the same command.

## 5. Clean and Process the Data

Adds engineered features such as `home`, `rest_days`, and opponent stats.

```bash
make clean_data
```

**Output file created:** `data/processed/team_games_clean.csv`

## 6. Verify the Data

Sanity check:

```bash
make verify
```

This prints dataset shape, date range, missing values, etc.

## 7. Run Notebooks

Open in VS Code (use the kernel you installed in step 3.1) or Jupyter and run all cells:

* `notebooks/01_data_prep.ipynb` (prep verification + quick plot)
* `notebooks/02_EDA.ipynb` (EDA placeholders)
* `notebooks/03_regression.ipynb` (regression placeholders)

For more advanced tasks later on, consider switching to Colab to use GPUs for efficiency. You can also connect repos to Colab.

## 8. View Results

* Clean dataset → `data/processed/team_games_clean.csv`
* Prep visualization → `img/prep_pts_hist.png`
* Team summary → `data/processed/team_summary.csv`
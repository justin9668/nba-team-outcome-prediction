PY=python

setup:
	$(PY) -m pip install -r requirements.txt

pull:
	$(PY) src/data_pull.py --season "2023-24" --season_type "Regular Season"

clean_data:
	$(PY) src/data_clean.py --infile "data/raw/team_gamelogs.csv" --outfile "data/processed/team_games_clean.csv"

verify:
	python src/verify.py


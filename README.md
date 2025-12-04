[View Final Report](final_report.md)  
[View Midterm Report](MIDTERM_REPORT.md)

# NBA Team Outcome Prediction Project

## Project Description
We will use the [nba_api](https://github.com/swar/nba_api) to collect team-level data in order to **predict each team’s final score** for a game. From these score predictions, we will derive the **winner** by comparing totals.  

This design gives us both a **regression task** (predicting team scores) and a **classification task** (predicting winners), while keeping the scope clear, focused, and manageable.  

---

## Project Goals
- Predict team total points scored in a game (regression).  
- Derive the game winner from predicted scores (classification).  
- Benchmark predictions against simple baselines:  
  - **Regression baseline**: team season average points.  
  - **Classification baseline**: higher season win percentage.  
- Visualize team performance trends and prediction accuracy across a season.  
- Ensure the workflow is fully reproducible from our GitHub repository.  

---

## Data Collection
We will use:  
- **nba_api**:  
  - Team box scores (points, FG%, 3P%, rebounds, turnovers, pace).  
  - Game context (home/away, rest days, back-to-backs).  
  - Historical game results.  

- **Scope**: One NBA season.  
- **Split**: Train on the first 80% of games, test on the last 20% to simulate real-world forecasting.  

---

## Modeling Plan
- **Regression (team scores)**: Linear Regression, Ridge/Lasso, Random Forest Regressor.  
- **Classification (winners)**: Derived from regression predictions, with optional direct models (Logistic Regression, Random Forest).  
- **Exploration**: K-Means clustering to explore team styles (e.g., pace-and-space vs. defensive).  

---

## Visualization
We will produce visualizations to better understand trends and model performance:  
- Scatter plots of predicted vs. actual team scores.  
- Rolling error plots showing model error across the season.  
- Heatmaps of team-level over- and under-performance.  
- Win probability plots comparing predicted winners with outcomes.  

---

## Test Plan
- **Train/Test Split**: First 80% of games for training, last 20% for testing (chronological, to avoid data leakage).  
- **Metrics**:  
  - Regression: MAE, RMSE compared to season average baseline.  
  - Classification: Accuracy compared to season win percentage baseline.  
- **Goal**: Achieve lower regression error and higher win prediction accuracy than the baselines.  

---

## Group Members
- Alim (ackura@bu.edu)  
- Ash (payaalayushman@gmail.com)  
- Jonah (jonahr@bu.edu)  
- Justin (justin1@bu.edu)  
- Shawn (xianghu0605@gmail.com)  

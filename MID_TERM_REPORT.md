## **Midterm Report Outline - _NBA Team Outcome Prediction_**

### **Introduction**

The goal of this project is to build a data-driven model that predicts the outcome of NBA games using publicly available team-level statistics. Specifically, we aim to predict each team's total points scored in a given game and then determine the winner based on those predicted scores. This design allows us to treat the problem as both a regression task (predicting numeric scores) and a classification task (predicting winners), providing a richer and more interpretable analysis of game outcomes.

Predicting team outcomes in the NBA is an interesting problem because basketball results depend on a combination of team skill, pace, fatigue, home-court advantage, and randomness. Understanding these factors can reveal meaningful patterns in team performance and may also have practical applications for forecasting and strategy analysis. By modeling team performance statistically, we can evaluate which features most influence scoring and winning, and we can compare our models' predictive power against simple historical baselines.

Our project adopts a two-stage design. First, we use regression models to predict the total points each team will score in a specific matchup. Then, we compare the two predicted scores to infer the game winner, effectively creating a derived classification prediction. This structure simplifies the modeling process, keeps the data consistent across tasks, and enables us to analyze both quantitative accuracy and win prediction accuracy within one unified framework.

### **Data Description**

We obtain our data directly from the NBA's official statistics API through the open-source Python package **nba_api**. This API provides access to detailed game-level information for all teams and games in a given season. Using the LeagueGameFinder endpoint, we collect data for every regular-season game in the 2023-24 NBA season.

Each observation in our dataset represents a single team's performance in one game. The dataset includes both outcome variables (such as total points scored) and explanatory variables describing team performance and game context. The key features include field goal percentage (FG%), three-point percentage (3P%), total rebounds (REB), assists (AST), turnovers (TOV), and pace. In addition, we incorporate contextual information such as whether the team was playing at home or away, how many rest days they had since their previous game, and whether the game was part of a back-to-back sequence.

The scope of our data is limited to one complete NBA regular season to ensure consistency and manageability. This allows us to train models that learn from the majority of games and then test their ability to generalize to unseen games within the same season. Each team-game pair forms one row in the dataset, resulting in approximately twice as many rows as total games played in the season.

### **Data Processing**

Our data collection pipeline begins with automated retrieval of game-level statistics using the nba_api.stats.endpoints.leaguegamefinder function. We specify the season and season type ("Regular Season") to ensure consistent data coverage. The raw API output is converted into a Pandas DataFrame for further processing.

The data cleaning stage includes several key steps. We standardize column names and data types, ensuring that fields such as GAME_ID and team identifiers are stored as strings for consistency across merges. Missing values are handled through imputation based on team season averages or by forward-filling recent values where appropriate. We also verify that duplicated entries and canceled games are removed.

For normalization, numerical features such as shooting percentages, rebounds, and turnovers are scaled or standardized where needed to support model training. We also create additional engineered features to capture contextual effects. For example, a binary variable indicates whether the team played at home or away, another feature encodes the number of rest days since the previous game, and a categorical indicator flags back-to-back situations.

Finally, we split the dataset chronologically to simulate real-world forecasting conditions. The first 80 percent of games (by date) are used for model training, while the final 20 percent are reserved for testing. This prevents data leakage from future games and provides a realistic evaluation of model performance on unseen matchups.

### **Preliminary Visualizations**

To gain an initial understanding of our dataset, we conducted exploratory data analysis (EDA) to identify general scoring patterns and relationships among key variables. The following visualizations summarize the main trends observed so far.

**Points Distribution**

![Points Distribution](img/points_distribution.png)

The distribution of total team points per game shows that most teams score between approximately 100 and 120 points. This suggests that the overall scoring environment in the NBA is relatively consistent across teams and games, with only a few outliers that likely correspond to overtime or exceptionally low-scoring matches.

**Home vs. Away Performance**

![home_vs_away_analysis](img/home_vs_away_analysis.png)

Teams tend to perform slightly better when playing at home. The average team score is a few points higher in home games than in away games, supporting the commonly observed home-court advantage in professional basketball.

**Rest Days and Performance**

![rest_days_analysis](img/rest_days_analysis.png)

Although we examined the relationship between rest days and team performance, the results suggest that the effect of rest is limited at the team level. Across different rest-day categories, both total points and field goal percentages remain relatively stable, indicating that teams tend to maintain consistent performance even during back-to-back games. This may reflect the NBA's deep rosters and player management strategies that mitigate fatigue effects.

**Feature Correlations**

![coorelation_heatmap](img/correlation_heatmap.png)

The correlation heatmap provides an overview of how different statistical variables relate to each other and to total team points. As expected, field goal percentage (FG%) and field goals made (FGM) show the strongest positive correlations with total points scored (0.73 and 0.86 respectively). Three-point percentage (fg3_pct) and assists (AST) are also positively correlated with scoring, indicating that efficient shooting and ball movement are key contributors to offensive performance.

Turnovers (TOV) display a weak negative correlation with points scored (-0.17), suggesting that teams with better ball control tend to achieve higher scores. Rebounds (REB) have only a weak positive relationship with scoring, which may reflect that high rebounding numbers can result from missed shots rather than purely successful offense.

Among opponent-related variables, strong correlation (0.79) between opponent turnovers and steals occurs because most opponent turnovers result directly from successful steals. In other words, steals are a primary source of forced turnovers in basketball. The negative correlation (-0.54) between opponent rebounds and field goal percentage suggests that teams with higher shooting efficiency allow fewer opponent rebounds. When a team makes more of its shots, there are fewer missed attempts available for the opposing team to rebound.

### **Modeling Methods**

To improve stability and reduce the potential influence of multicollinearity among correlated features, we then trained a Ridge Regression model with a regularization parameter of α = 1.0. No Lasso regression or other nonlinear models were applied at this stage. Missing feature values were handled by dropping incomplete rows, and no scaling or pipeline preprocessing was applied, as both Linear and Ridge Regression are generally robust to moderate differences in feature scale.

Model performance was evaluated on a held-out test set using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). Both regression models were compared against a simple baseline, which predicts each team's score using its season-average points. The results show a substantial improvement over the baseline: Linear Regression achieved an MAE of 4.12 and an RMSE of 5.18, while Ridge Regression achieved an MAE of 4.14 and an RMSE of 5.20 on the test set. These errors are less than half those of the baseline (MAE 9.91, RMSE 12.35), indicating that even simple linear models can effectively capture meaningful relationships in the data.

To further interpret model performance, we generated several visualizations, including model comparison bar charts, predicted vs. actual scatter plots, and error distribution plots by team. These results confirm that the regression models are both consistent and interpretable, providing a solid foundation for the next stage of analysis.

### **Preliminary Results**

We evaluated our regression models on a held-out test set using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) as the main performance metrics. Both Linear and Ridge Regression were compared against a simple baseline that predicts each team's score using its season-average points. The results are summarized below.

| **Model**             | **MAE** | **RMSE** |
| --------------------------- | ------------- | -------------- |
| Baseline (Team Average)     | 9.91          | 12.35          |
| Linear Regression           | 4.12          | 5.18           |
| Ridge Regression (α = 1.0) | 4.14          | 5.20           |

The results show that both linear models significantly outperform the baseline, reducing the mean absolute error by more than half. The nearly identical performance between Linear and Ridge Regression suggests that regularization provides limited additional benefit at this stage, possibly because the dataset does not exhibit strong multicollinearity or overfitting.

Several visualizations were generated to assess model behavior.



![model_comparison](img/model_comparison.png)

The figure compares the Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) of the baseline, Linear Regression, and Ridge Regression models on the test set. Both regression models achieve substantially lower errors than the baseline, reducing MAE from 9.91 to about 4.1 and RMSE from 12.35 to about 5.2. The nearly identical results between Linear and Ridge Regression indicate that regularization has minimal effect at this stage, suggesting the dataset is well-behaved without severe multicollinearity. Overall, the models demonstrate strong predictive accuracy relative to the simple season-average baseline.

![model_comparison](img/predicted_vs_actual.png)

The scatter plots compare predicted and actual team scores on the test set for both Linear and Ridge Regression models. Each point represents one team's score in a single game, with the red dashed line indicating perfect prediction. The data points are tightly clustered around the diagonal, showing that both models accurately capture general scoring trends. The MAE and RMSE values are low and nearly identical (MAE ≈ 4.1, RMSE ≈ 5.2), suggesting that the regularization applied in Ridge Regression provides minimal benefit over the standard linear model at this stage. Overall, the results demonstrate that a simple linear framework can already model team scoring with strong accuracy.

Overall, these preliminary results confirm that our data pipeline and regression framework are functioning correctly and producing meaningful predictions. The models already outperform simple baselines by a wide margin, establishing a strong foundation for extending our analysis to classification models and more advanced regression techniques in the next phase.

![error_analysis](img/error_analysis.png)



The left panel shows the overall distribution of prediction errors, calculated as the difference between actual and predicted team points. The distribution is approximately centered around zero, with most errors falling within ±10 points, indicating that the regression models do not exhibit strong bias toward over- or under-prediction.

The right panel presents the **average prediction error by team**. While most teams have near-zero mean errors, a few teams show small consistent deviations, suggesting that certain play styles or scoring patterns are not yet fully captured by the current linear model. High-scoring, fast-paced teams tend to be slightly underpredicted, whereas more defensive teams are slightly overpredicted. Overall, the model errors are well balanced and confirm that the regression framework performs reliably across teams.

### **Code Implementation**

Our codebase is organized to ensure a clear and reproducible workflow from data collection to model evaluation. All code and instructions are available in our GitHub repository.

Data collection and preprocessing are handled in the src directory, which contains modular scripts for retrieving and preparing NBA game data. The main data retrieval process uses the nba_api library through the data_pull.py script, which fetches game-level statistics and constructs the feature dataset. Supporting functions for data cleaning and feature engineering are defined in utils.py.

Exploratory data analysis (EDA) and modeling are performed in Jupyter notebooks located in the notebooks folder.

- 02_EDA.ipynb includes initial descriptive analysis and visualizations such as score distributions, home/away performance, rest-day effects, and correlation heatmaps.
- 03_Regression.ipynb implements Linear and Ridge Regression models, evaluates performance metrics, and generates visualizations of model results and error analysis.

All visual outputs are automatically saved to the /img directory for easy reference and integration into the report.
Dependencies are listed in requirements.txt, and the RUN_GUIDE.md file provides step-by-step instructions for reproducing results, including environment setup and dataset generation. The Makefile further simplifies execution by automating key steps such as data fetching and notebook execution.

This structure ensures that any user can reproduce the full data pipeline and modeling process from a clean environment, verifying both data integrity and model results.

**Next Steps**

In the next stage, we will implement direct winner prediction by deriving outcomes from regression scores and adding a Logistic Regression classifier for comparison. We plan to tune the Ridge α parameter, introduce time-aware cross-validation, and test additional features such as team pace, defensive metrics, and interaction terms. Further work will focus on improving model interpretability with coefficient and feature importance analysis, expanding error analysis by team and over time, and cleaning the notebooks and source code for consistency and clarity.

### **References**

Boston University, Department of Computer Science. (n.d.). _CS506: Data Science Tools and Applications - Course website_. Retrieved October 26, 2025, from [https://gallettilance.github.io/](https://gallettilance.github.io/)

Boston University, Department of Computer Science. (n.d.). _CS506 Final Project - Guidelines and deliverables_. Retrieved October 26, 2025, from [https://gallettilance.github.io/final_project/](https://gallettilance.github.io/final_project/)

Swar, G., et al. (n.d.). _nba_api: An API client package to access the NBA Stats API_ \[GitHub repository\]. Retrieved October 26, 2025, from [https://github.com/swar/nba_api](https://github.com/swar/nba_api)

National Basketball Association. (n.d.). _NBA Stats - Official statistics portal_. Retrieved October 26, 2025, from [https://www.nba.com/stats/](https://www.nba.com/stats/)


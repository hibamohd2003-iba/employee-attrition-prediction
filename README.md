# Employee Attrition Prediction

Predicting employee attrition using SQL, Python Machine Learning, and Industrial Engineering analysis on the IBM HR Analytics dataset.

## Project Overview
Employee attrition costs companies 6–9 months of an employee's salary in recruitment and training costs. This project builds an end-to-end system to predict which employees are likely to leave, and quantifies the business impact using Industrial Engineering frameworks.

## Tools and Technologies
- **Python** — data preprocessing, ML model training
- **SQLite** — database storage and SQL feature engineering
- **Scikit-learn** — Logistic Regression, Random Forest
- **XGBoost** — best performing model
- **Matplotlib / Seaborn** — data visualization
- **VS Code** — development environment

## Dataset
IBM HR Analytics Employee Attrition dataset — 1,470 employee records, 35 features.  
Source: Kaggle

## Project Structure
├── attrition.py          # Load CSV into SQLite database
├── sql_queries.py        # SQL feature engineering queries
├── ml_model.py           # Train and evaluate ML models
├── charts.py             # Generate visualizations
├── ie_analysis.py        # Industrial Engineering analysis
├── feature_importance.png
├── dept_attrition_chart.png
├── risk_pie_chart.png

## SQL Analysis Results
| Department | Attrition Rate |
|------------|---------------|
| Sales | 20.63% |
| Human Resources | 19.05% |
| Research & Development | 13.84% |

Key finding: Employees who left earned an average of Rs 4,787/month vs Rs 6,832 for those who stayed.

## ML Model Results
| Model | Accuracy | AUC Score |
|-------|----------|-----------|
| Logistic Regression | 86.7% | 0.777 |
| Random Forest | 84.4% | 0.789 |
| XGBoost | 86.1% | **0.791** |

XGBoost selected as the final model based on highest AUC score.

## Industrial Engineering Analysis
- **Predicted attrition cost:** Rs 3,85,182
- **Employees at risk:** 18
- **Total hiring needed:** 91 (18 replacements + 73 for 5% growth)
- **Highest risk department:** Sales (13.4% predicted attrition)

## Key Insights
1. Monthly income is the strongest predictor of attrition
2. Employees working overtime are significantly more likely to leave
3. Sales department requires immediate HR intervention
4. Early identification of 79 high-risk employees can save Rs 3.85 lakh in attrition costs

## Author
Hiba — Industrial Engineering Student, College of Engineering Trivandrum  
GitHub: hibamohd2003-iba

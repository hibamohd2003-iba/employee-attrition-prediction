import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# Load data
conn = sqlite3.connect(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\attrition.db')
df = pd.read_sql("SELECT * FROM employees", conn)

# Prepare model
df_model = df.copy()
df_model['Attrition'] = df_model['Attrition'].map({'Yes': 1, 'No': 0})
df_model['OverTime'] = df_model['OverTime'].map({'Yes': 1, 'No': 0})
df_model['Gender'] = df_model['Gender'].map({'Male': 1, 'Female': 0})

le = LabelEncoder()
for col in ['Department', 'JobRole', 'MaritalStatus', 'EducationField', 'BusinessTravel']:
    df_model[col] = le.fit_transform(df_model[col])

df_model.drop(['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'], axis=1, inplace=True)

X = df_model.drop('Attrition', axis=1)
y = df_model['Attrition']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42, eval_metric='logloss')
xgb.fit(X_train, y_train)

# Add predictions
df_test = df.loc[X_test.index].copy()
df_test['predicted_attrition'] = xgb.predict(X_test)
df_test['risk_probability'] = xgb.predict_proba(X_test)[:,1]

# IE Calculation 1 - Attrition Cost
at_risk = df_test[df_test['predicted_attrition'] == 1]
cost_per_employee = at_risk['MonthlyIncome'] * 6
total_cost = cost_per_employee.sum()

print("=" * 50)
print("IE ANALYSIS - ATTRITION COST")
print("=" * 50)
print(f"Employees predicted to leave: {len(at_risk)}")
print(f"Total estimated cost: Rs {total_cost:,.0f}")
print(f"Average cost per leaver: Rs {total_cost/len(at_risk):,.0f}")

# IE Calculation 2 - Capacity Planning
current_strength = len(df)
predicted_leavers = int(df_test['predicted_attrition'].sum())
growth_hiring = int(current_strength * 0.05)
total_hiring = predicted_leavers + growth_hiring

print("\n" + "=" * 50)
print("IE ANALYSIS - CAPACITY PLANNING")
print("=" * 50)
print(f"Current headcount: {current_strength}")
print(f"Predicted to leave: {predicted_leavers}")
print(f"Hiring needed for 5% growth: {growth_hiring}")
print(f"Total hiring needed: {total_hiring}")

# IE Calculation 3 - Department wise risk
print("\n" + "=" * 50)
print("IE ANALYSIS - DEPARTMENT RISK SUMMARY")
print("=" * 50)
dept_risk = df_test.groupby('Department')['predicted_attrition'].agg(['sum', 'count'])
dept_risk.columns = ['predicted_leavers', 'total']
dept_risk['risk_pct'] = (dept_risk['predicted_leavers'] / dept_risk['total'] * 100).round(1)
print(dept_risk)

# Save results
df_test[['Department', 'MonthlyIncome', 'predicted_attrition', 'risk_probability']].to_csv(
    r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\ie_results.csv', index=False)
print("\nIE results saved!")
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# Load data
conn = sqlite3.connect(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\attrition.db')
df = pd.read_sql("SELECT * FROM employees", conn)

# Prepare model to get feature importance
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

# Chart 1 - Feature Importance
feat_imp = pd.DataFrame({
    'Feature': X.columns,
    'Importance': xgb.feature_importances_
}).sort_values('Importance', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=feat_imp, x='Importance', y='Feature', palette='Blues_r')
plt.title('Top 10 Factors That Predict Employee Attrition')
plt.tight_layout()
plt.savefig(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\feature_importance.png', dpi=150)
plt.show()
print("Chart 1 saved!")

# Chart 2 - Attrition by Department
dept = df.groupby('Department')['Attrition'].apply(
    lambda x: (x == 'Yes').mean() * 100).reset_index()
dept.columns = ['Department', 'Attrition_Rate']

plt.figure(figsize=(8, 5))
sns.barplot(data=dept, x='Department', y='Attrition_Rate', palette='coolwarm')
plt.title('Attrition Rate by Department (%)')
plt.ylabel('Attrition Rate %')
plt.tight_layout()
plt.savefig(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\dept_attrition_chart.png', dpi=150)
plt.show()
print("Chart 2 saved!")

# Chart 3 - Risk Level Pie Chart
risk_counts = pd.Series({'HIGH RISK': 79, 'MEDIUM RISK': 578, 'LOW RISK': 813})
plt.figure(figsize=(7, 7))
plt.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%',
        colors=['#ff4444', '#ffaa00', '#44bb44'])
plt.title('Employee Risk Level Distribution')
plt.tight_layout()
plt.savefig(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\risk_pie_chart.png', dpi=150)
plt.show()
print("Chart 3 saved!")

print("\nAll 3 charts saved to your folder!")
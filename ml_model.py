import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Connect to database
conn = sqlite3.connect(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\attrition.db')
df = pd.read_sql("SELECT * FROM employees", conn)

# Clean and encode data
df_model = df.copy()
df_model['Attrition'] = df_model['Attrition'].map({'Yes': 1, 'No': 0})
df_model['OverTime'] = df_model['OverTime'].map({'Yes': 1, 'No': 0})
df_model['Gender'] = df_model['Gender'].map({'Male': 1, 'Female': 0})

le = LabelEncoder()
for col in ['Department', 'JobRole', 'MaritalStatus', 'EducationField', 'BusinessTravel']:
    df_model[col] = le.fit_transform(df_model[col])

df_model.drop(['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'], axis=1, inplace=True)

# Split data
X = df_model.drop('Attrition', axis=1)
y = df_model['Attrition']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# Train 3 models
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

xgb = XGBClassifier(n_estimators=100, learning_rate=0.1,
                     max_depth=5, random_state=42, eval_metric='logloss')
xgb.fit(X_train, y_train)

# Compare results
for name, model in [('Logistic Regression', lr),
                    ('Random Forest', rf),
                    ('XGBoost', xgb)]:
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
    print(f"\n{name}: Accuracy={acc:.3f}, AUC={auc:.3f}")
    print(classification_report(y_test, pred))
import pandas as pd
import sqlite3

conn = sqlite3.connect(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\attrition.db')

# Query 1 - Attrition by Department
query1 = """
SELECT Department, COUNT(*) AS total_employees,
SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS people_left,
ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_percent
FROM employees GROUP BY Department ORDER BY attrition_rate_percent DESC
"""
result1 = pd.read_sql(query1, conn)
print("Query 1 - Attrition by Department:")
print(result1)
result1.to_csv(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\dept_attrition.csv', index=False)
import pandas as pd
import sqlite3

conn = sqlite3.connect(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\attrition.db')

# Query 1 - Attrition by Department
query1 = """
SELECT Department, COUNT(*) AS total_employees,
SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS people_left,
ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_percent
FROM employees GROUP BY Department ORDER BY attrition_rate_percent DESC
"""
result1 = pd.read_sql(query1, conn)
print("Query 1 - Attrition by Department:")
print(result1)
result1.to_csv(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\dept_attrition.csv', index=False)
print("Saved!\n")

# Query 2 - Salary vs Attrition
query2 = """
SELECT Attrition,
ROUND(AVG(MonthlyIncome), 2) AS avg_salary,
ROUND(AVG(JobSatisfaction), 2) AS avg_satisfaction,
ROUND(AVG(YearsAtCompany), 2) AS avg_years
FROM employees GROUP BY Attrition
"""
result2 = pd.read_sql(query2, conn)
print("Query 2 - Salary vs Attrition:")
print(result2)
result2.to_csv(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\salary_attrition.csv', index=False)
print("Saved!\n")

# Query 3 - High Risk Employee Flag
query3 = """
SELECT EmployeeNumber, Department, MonthlyIncome, JobSatisfaction, OverTime,
CASE
    WHEN JobSatisfaction <= 2 AND OverTime = 'Yes' AND MonthlyIncome < 5000 THEN 'HIGH RISK'
    WHEN JobSatisfaction = 3 OR DistanceFromHome > 20 THEN 'MEDIUM RISK'
    ELSE 'LOW RISK'
END AS attrition_risk_level
FROM employees
"""
result3 = pd.read_sql(query3, conn)
print("Query 3 - Risk Levels:")
print(result3['attrition_risk_level'].value_counts())
result3.to_csv(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\risk_levels.csv', index=False)
print("Saved!\n")

# Query 4 - Utilization Rate
query4 = """
SELECT Department, COUNT(*) AS total,
SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) AS overworked,
ROUND(100.0 * SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS utilization_rate_pct
FROM employees GROUP BY Department
"""
result4 = pd.read_sql(query4, conn)
print("Query 4 - Utilization Rate:")
print(result4)
result4.to_csv(r'C:\Users\hibam\OneDrive\Desktop\IBM HR Employee  Attrition\utilization_rate.csv', index=False)
print("Saved!\n")

print("All 4 queries done! CSVs saved to your folder.")
conn.close()
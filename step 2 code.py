import pandas as pd
import re
from tabulate import tabulate

# Sample attendance streak data from Step 1
df_streaks = pd.DataFrame({
    "student_id": [101, 102, 103],
    "absence_start_date": ["2024-01-01", "2024-02-01", "2024-03-05"],
    "absence_end_date": ["2024-01-04", "2024-02-04", "2024-03-09"],
    "total_absent_days": [4, 4, 5]
})

df_streaks["absence_start_date"] = pd.to_datetime(df_streaks["absence_start_date"])
df_streaks["absence_end_date"] = pd.to_datetime(df_streaks["absence_end_date"])

# Sample student data
students = pd.DataFrame({
    "student_id": [101, 102, 103, 104],
    "student_name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "David Lee"],
    "parent_email": ["alice.parent@example.com", "bob.parent@example.com", "invalid_email.com", "invalid@email.com"]
})

# Function to validate emails
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Merge attendance streaks with student data
df_merged = df_streaks.merge(students, on="student_id", how="left")

# Validate emails
df_merged["valid_email"] = df_merged["parent_email"].apply(is_valid_email)

# Generate messages for valid emails
df_merged["msg"] = df_merged.apply(lambda row: f"Dear Parent, Your child {row['student_name']} was absent from {row['absence_start_date'].strftime('%d-%m-%Y')} to {row['absence_end_date'].strftime('%d-%m-%Y')} for {row['total_absent_days']} days. Please ensure their attendance improves." if row["valid_email"] else "", axis=1)

# Keep only required columns
df_final = df_merged[["student_id", "absence_start_date", "absence_end_date", "total_absent_days", "parent_email", "msg"]]

# Filter out students with invalid emails
df_final = df_final[df_final["msg"] != ""]

# Print output in tabular format
print(tabulate(df_final, headers='keys', tablefmt='grid'))

import pandas as pd
import mysql.connector

df = pd.read_csv("budget_master.csv", encoding="latin1")

df = df.iloc[:, :13]
df = df.fillna("")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="learningt"
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS budget")

cursor.execute("""
CREATE TABLE budget (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_type TEXT,
    vendor_name TEXT,
    vendor_type TEXT,
    line_of_business TEXT,
    programme_name TEXT,
    job_code TEXT,
    batch_semester TEXT,
    batches TEXT,
    training TEXT,
    paper_name TEXT,
    training_hours TEXT,
    rate_per_hour TEXT,
    total TEXT
)
""")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO budget (
            business_type,
            vendor_name,
            vendor_type,
            line_of_business,
            programme_name,
            job_code,
            batch_semester,
            batches,
            training,
            paper_name,
            training_hours,
            rate_per_hour,
            total
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(str(x) for x in row.tolist()))

conn.commit()
cursor.close()
conn.close()

print("Imported successfully!")
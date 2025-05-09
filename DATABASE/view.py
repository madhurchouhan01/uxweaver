import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("task_management.db")
cursor = conn.cursor()

# Create Task table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Task (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    task_description TEXT,
    user_preference TEXT,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium'
);
""")

# Create TaskBreakdown table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TaskBreakdown (
    breakdown_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    spike TEXT,
    user_story TEXT,
    FOREIGN KEY (task_id) REFERENCES Task(task_id) ON DELETE CASCADE
);
""")

# Commit and close the connection
conn.commit()
conn.close()

print("Tables created successfully.")

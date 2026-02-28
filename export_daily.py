#!/usr/bin/env python3
import sqlite3
import json
import os
from datetime import datetime


def export_today_data(db_path="github_trending.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_start = f"{today} 00:00:00"
    
    cursor.execute('''
        SELECT name, description, language, stars, forks, today_stars, 
               url, created_at, updated_at, fetched_at
        FROM projects
        WHERE fetched_at >= ?
        ORDER BY fetched_at DESC, stars DESC
    ''', (today_start,))
    
    rows = cursor.fetchall()
    conn.close()
    
    projects = []
    for row in rows:
        projects.append({
            "name": row[0],
            "description": row[1],
            "language": row[2],
            "stars": row[3],
            "forks": row[4],
            "today_stars": row[5],
            "url": row[6],
            "created_at": row[7],
            "updated_at": row[8],
            "fetched_at": row[9]
        })
    
    if not projects:
        print("No data fetched today")
        return
    
    os.makedirs("datas", exist_ok=True)
    filename = f"datas/{today}.json"
    
    data = {
        "date": today,
        "count": len(projects),
        "projects": projects
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Exported {len(projects)} projects to {filename}")


if __name__ == "__main__":
    export_today_data()

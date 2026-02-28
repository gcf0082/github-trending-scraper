#!/usr/bin/env python3
import sqlite3
import json


def export_latest(db_path="github_trending.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, description, language, stars, forks, today_stars, 
               url, created_at, updated_at, fetched_at
        FROM projects
        ORDER BY fetched_at DESC
        LIMIT 100
    ''')
    
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
    
    with open("datas/latest.json", "w", encoding="utf-8") as f:
        json.dump({
            "count": len(projects),
            "projects": projects
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Exported {len(projects)} projects to datas/latest.json")


if __name__ == "__main__":
    export_latest()

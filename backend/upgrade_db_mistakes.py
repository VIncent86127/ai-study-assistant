#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 数据库升级脚本
新增错题集功能相关表
"""

import sqlite3

DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'


def upgrade_database():
    """升级数据库，新增错题集相关表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("正在升级数据库...")
    
    # 1. 错题主表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL DEFAULT 'default',
            subject_id INTEGER,
            grade_id INTEGER,
            chapter_id INTEGER,
            question_text TEXT NOT NULL,
            correct_answer TEXT,
            user_answer TEXT,
            mistake_type TEXT DEFAULT 'unknown',
            difficulty TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (grade_id) REFERENCES grades(id),
            FOREIGN KEY (chapter_id) REFERENCES chapters(id)
        )
    ''')
    print("✓ 创建 mistakes 表")
    
    # 2. 错题-知识点关联表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mistake_knowledge_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mistake_id INTEGER NOT NULL,
            knowledge_type TEXT NOT NULL,
            knowledge_id INTEGER NOT NULL,
            relevance_score REAL DEFAULT 1.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (mistake_id) REFERENCES mistakes(id) ON DELETE CASCADE
        )
    ''')
    print("✓ 创建 mistake_knowledge_links 表")
    
    # 3. 生僻词解析表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mistake_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            meaning TEXT,
            phonetic TEXT,
            example_usage TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (mistake_id) REFERENCES mistakes(id) ON DELETE CASCADE
        )
    ''')
    print("✓ 创建 vocabulary_notes 表")
    
    # 4. 用户备注表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mistake_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mistake_id INTEGER NOT NULL,
            note_type TEXT NOT NULL DEFAULT 'text',
            content TEXT NOT NULL,
            voice_duration INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (mistake_id) REFERENCES mistakes(id) ON DELETE CASCADE
        )
    ''')
    print("✓ 创建 mistake_notes 表")
    
    # 5. 复习记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS review_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mistake_id INTEGER NOT NULL,
            review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            result TEXT NOT NULL DEFAULT 'wrong',
            review_notes TEXT,
            FOREIGN KEY (mistake_id) REFERENCES mistakes(id) ON DELETE CASCADE
        )
    ''')
    print("✓ 创建 review_records 表")
    
    # 创建索引以优化查询
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mistakes_user ON mistakes(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mistakes_subject ON mistakes(subject_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mistakes_status ON mistakes(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mistakes_created ON mistakes(created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vocab_mistake ON vocabulary_notes(mistake_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_notes_mistake ON mistake_notes(mistake_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_review_mistake ON review_records(mistake_id)')
    print("✓ 创建索引")
    
    conn.commit()
    
    # 验证表结构
    print("\n=== 数据库表结构验证 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print(f"当前表: {[t[0] for t in tables]}")
    
    # 显示新增表的字段
    print("\n=== 新增表字段详情 ===")
    new_tables = ['mistakes', 'mistake_knowledge_links', 'vocabulary_notes', 'mistake_notes', 'review_records']
    for table in new_tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\n【{table}】")
        for col in columns:
            print(f"  {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else ''}")
    
    conn.close()
    print("\n✅ 数据库升级完成！")


if __name__ == '__main__':
    upgrade_database()
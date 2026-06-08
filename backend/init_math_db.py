#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化初中数学知识点数据库
覆盖七年级、八年级、九年级全部内容
"""

import sqlite3
from datetime import datetime

def get_db():
    return sqlite3.connect('knowledge.db')

def create_math_tables():
    """创建数学相关表"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 数学章节表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade TEXT NOT NULL,
            semester TEXT NOT NULL,
            chapter_name TEXT NOT NULL,
            chapter_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 数学概念/公式表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            concept_name TEXT NOT NULL,
            concept_type TEXT DEFAULT 'concept',
            definition TEXT,
            formula TEXT,
            properties TEXT,
            examples TEXT,
            difficulty INTEGER DEFAULT 1,
            keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chapter_id) REFERENCES math_chapters(id)
        )
    ''')
    
    # 数学定理/法则表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_theorems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            theorem_name TEXT NOT NULL,
            content TEXT NOT NULL,
            proof TEXT,
            application TEXT,
            examples TEXT,
            difficulty INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chapter_id) REFERENCES math_chapters(id)
        )
    ''')
    
    # 数学解题方法表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            method_name TEXT NOT NULL,
            description TEXT,
            steps TEXT,
            applicable_types TEXT,
            examples TEXT,
            tips TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chapter_id) REFERENCES math_chapters(id)
        )
    ''')
    
    # 数学易错点表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_common_mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            topic TEXT NOT NULL,
            mistake_type TEXT,
            wrong_approach TEXT,
            correct_approach TEXT,
            reason TEXT,
            examples TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chapter_id) REFERENCES math_chapters(id)
        )
    ''')
    
    # 数学常见题型表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_question_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            type_name TEXT NOT NULL,
            description TEXT,
            solution_strategy TEXT,
            difficulty_level INTEGER DEFAULT 1,
            exam_frequency TEXT,
            examples TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chapter_id) REFERENCES math_chapters(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("数学数据表创建完成")

def init_math_chapters():
    """初始化数学章节"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 清空现有数据
    cursor.execute('DELETE FROM math_chapters')
    
    chapters = [
        # 七年级上册
        ('七年级', '上册', '有理数', 1),
        ('七年级', '上册', '整式的加减', 2),
        ('七年级', '上册', '一元一次方程', 3),
        ('七年级', '上册', '几何图形初步', 4),
        
        # 七年级下册
        ('七年级', '下册', '相交线与平行线', 1),
        ('七年级', '下册', '实数', 2),
        ('七年级', '下册', '平面直角坐标系', 3),
        ('七年级', '下册', '二元一次方程组', 4),
        ('七年级', '下册', '不等式与不等式组', 5),
        ('七年级', '下册', '数据的收集、整理与描述', 6),
        
        # 八年级上册
        ('八年级', '上册', '三角形', 1),
        ('八年级', '上册', '全等三角形', 2),
        ('八年级', '上册', '轴对称', 3),
        ('八年级', '上册', '整式的乘除与因式分解', 4),
        ('八年级', '上册', '分式', 5),
        
        # 八年级下册
        ('八年级', '下册', '二次根式', 1),
        ('八年级', '下册', '勾股定理', 2),
        ('八年级', '下册', '平行四边形', 3),
        ('八年级', '下册', '一次函数', 4),
        ('八年级', '下册', '数据的分析', 5),
        
        # 九年级上册
        ('九年级', '上册', '一元二次方程', 1),
        ('九年级', '上册', '二次函数', 2),
        ('九年级', '上册', '旋转', 3),
        ('九年级', '上册', '圆', 4),
        ('九年级', '上册', '概率初步', 5),
        
        # 九年级下册
        ('九年级', '下册', '反比例函数', 1),
        ('九年级', '下册', '相似', 2),
        ('九年级', '下册', '锐角三角函数', 3),
        ('九年级', '下册', '投影与视图', 4),
    ]
    
    for grade, semester, name, order in chapters:
        cursor.execute('''
            INSERT INTO math_chapters (grade, semester, chapter_name, chapter_order)
            VALUES (?, ?, ?, ?)
        ''', (grade, semester, name, order))
    
    conn.commit()
    conn.close()
    print(f"已初始化 {len(chapters)} 个数学章节")

if __name__ == '__main__':
    create_math_tables()
    init_math_chapters()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成数学错题测试数据
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_math_mistakes():
    """生成数学错题测试数据"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取数学学科ID
    cursor.execute("SELECT id FROM subjects WHERE name = '数学'")
    math_id = cursor.fetchone()['id']
    
    # 数学错题数据
    math_mistakes = [
        # 七年级 - 有理数
        {
            'grade': '初一',
            'type': '计算题',
            'difficulty': 2,
            'question': '计算：(-2)³ + 3 × (-4) - (-5)²',
            'answer': '(-2)³ + 3 × (-4) - (-5)² = -8 + (-12) - 25 = -45',
            'notes': '注意运算顺序：先算乘方，再算乘除，最后算加减'
        },
        {
            'grade': '初一',
            'type': '选择题',
            'difficulty': 1.5,
            'question': '下列各数中，绝对值最小的数是（ ）\nA. -3  B. -1  C. 0  D. 2',
            'answer': 'C\n|-3|=3，|-1|=1，|0|=0，|2|=2，最小的是0',
            'notes': '绝对值表示到原点的距离，非负数'
        },
        
        # 七年级 - 方程
        {
            'grade': '初一',
            'type': '计算题',
            'difficulty': 2,
            'question': '解方程：2(x-3) = 4 - (x+1)',
            'answer': '去括号：2x - 6 = 4 - x - 1\n移项：2x + x = 4 - 1 + 6\n合并：3x = 9\n系数化为1：x = 3',
            'notes': '去括号时注意符号变化'
        },
        {
            'grade': '初一',
            'type': '应用题',
            'difficulty': 2.5,
            'question': '小明从家到学校，去时每分钟走50米，回来时每分钟走40米，来回共用了18分钟。问小明家到学校的距离是多少米？',
            'answer': '设家到学校距离为x米\n去时时间：x/50 分钟\n回来时间：x/40 分钟\n方程：x/50 + x/40 = 18\n解得：x = 400 米',
            'notes': '列方程解应用题的关键是找等量关系'
        },
        
        # 八年级 - 三角形
        {
            'grade': '初二',
            'type': '证明题',
            'difficulty': 3,
            'question': '已知：如图，在△ABC中，AB=AC，D是BC的中点，DE⊥AB于E，DF⊥AC于F。求证：DE=DF。',
            'answer': '证明：\n∵ AB=AC，D是BC中点\n∴ AD是等腰△ABC底边上的中线\n∴ AD平分∠BAC（三线合一）\n∵ DE⊥AB，DF⊥AC\n∴ DE=DF（角平分线上的点到角两边距离相等）',
            'notes': '利用等腰三角形三线合一和角平分线性质'
        },
        {
            'grade': '初二',
            'type': '计算题',
            'difficulty': 2,
            'question': '在△ABC中，∠A=50°，∠B比∠C大10°，求∠B和∠C的度数。',
            'answer': '设∠C=x°，则∠B=(x+10)°\n三角形内角和：50 + x + (x+10) = 180\n解得：x = 60\n所以∠B=70°，∠C=60°',
            'notes': '三角形内角和为180°'
        },
        
        # 八年级 - 勾股定理
        {
            'grade': '初二',
            'type': '计算题',
            'difficulty': 2.5,
            'question': '一个直角三角形的两条直角边分别是6cm和8cm，求斜边上的高。',
            'answer': '斜边 = √(6² + 8²) = √100 = 10 cm\n面积 = (1/2) × 6 × 8 = 24 cm²\n斜边上的高 = 2 × 面积 ÷ 斜边 = 2 × 24 ÷ 10 = 4.8 cm',
            'notes': '利用面积法求斜边上的高'
        },
        
        # 八年级 - 函数
        {
            'grade': '初二',
            'type': '综合题',
            'difficulty': 3,
            'question': '已知一次函数y=kx+b的图象经过点A(1,3)和点B(-1,1)，求：\n(1) k和b的值\n(2) 当x=2时，y的值',
            'answer': '(1) 代入点A(1,3)：k+b=3\n    代入点B(-1,1)：-k+b=1\n    解方程组得：k=1，b=2\n(2) y = x + 2，当x=2时，y=4',
            'notes': '用待定系数法求一次函数解析式'
        },
        
        # 九年级 - 一元二次方程
        {
            'grade': '初三',
            'type': '计算题',
            'difficulty': 2,
            'question': '解方程：x² - 4x + 3 = 0',
            'answer': '方法一（因式分解）：\n(x-1)(x-3) = 0\nx₁=1，x₂=3\n\n方法二（公式法）：\nΔ = 16 - 12 = 4\nx = (4±2)/2\nx₁=1，x₂=3',
            'notes': '因式分解法最简便'
        },
        {
            'grade': '初三',
            'type': '应用题',
            'difficulty': 3,
            'question': '某商品原价100元，经过两次降价后售价为81元。如果两次降价的百分率相同，求每次降价的百分率。',
            'answer': '设每次降价x%\n100(1-x/100)² = 81\n(1-x/100)² = 0.81\n1-x/100 = 0.9\nx = 10\n每次降价10%',
            'notes': '增长率问题：原价×(1-降价率)^次数=现价'
        },
        
        # 九年级 - 二次函数
        {
            'grade': '初三',
            'type': '综合题',
            'difficulty': 4,
            'question': '已知二次函数y = x² - 4x + 3，求：\n(1) 函数图象的顶点坐标\n(2) 函数图象与x轴的交点坐标\n(3) 当x为何值时，y有最小值，最小值是多少？',
            'answer': '(1) y = (x-2)² - 1，顶点坐标(2, -1)\n(2) 令y=0，x²-4x+3=0，(x-1)(x-3)=0\n    交点坐标为(1,0)和(3,0)\n(3) 因为a=1>0，开口向上\n    当x=2时，y有最小值-1',
            'notes': '配方化为顶点式，或用顶点坐标公式'
        },
        
        # 九年级 - 圆
        {
            'grade': '初三',
            'type': '计算题',
            'difficulty': 3,
            'question': '已知圆的半径为5cm，一条弦的长度为8cm，求这条弦的弦心距。',
            'answer': '弦心距 = √(半径² - (弦长/2)²)\n       = √(5² - 4²)\n       = √9\n       = 3 cm',
            'notes': '利用垂径定理，弦心距、半径、半弦构成直角三角形'
        },
        {
            'grade': '初三',
            'type': '计算题',
            'difficulty': 2.5,
            'question': '已知扇形的半径为6cm，圆心角为120°，求扇形的面积和弧长。',
            'answer': '扇形面积 = 120×π×6²/360 = 12π cm²\n弧长 = 120×π×6/180 = 4π cm',
            'notes': '扇形面积公式：S=nπR²/360，弧长公式：l=nπR/180'
        },
        
        # 九年级 - 相似
        {
            'grade': '初三',
            'type': '证明题',
            'difficulty': 3.5,
            'question': '如图，在△ABC中，D是AB边上一点，DE∥BC交AC于E，AE=2，EC=3，AB=10，求AD的长。',
            'answer': '∵ DE∥BC\n∴ △ADE∽△ABC\n∴ AD/AB = AE/AC\n∵ AE=2，EC=3\n∴ AC=5\n∴ AD/10 = 2/5\n∴ AD = 4',
            'notes': '平行于三角形一边的直线截得的三角形与原三角形相似'
        },
        
        # 九年级 - 锐角三角函数
        {
            'grade': '初三',
            'type': '计算题',
            'difficulty': 2,
            'question': '在Rt△ABC中，∠C=90°，AC=3，BC=4，求sinA、cosA、tanA的值。',
            'answer': '斜边AB = √(3²+4²) = 5\nsinA = BC/AB = 4/5\ncosA = AC/AB = 3/5\ntanA = BC/AC = 4/3',
            'notes': '记住定义：sin=对边/斜边，cos=邻边/斜边，tan=对边/邻边'
        },
        
        # 概率
        {
            'grade': '初三',
            'type': '计算题',
            'difficulty': 2,
            'question': '一个袋子里有3个红球和2个白球，从中随机摸出1个球，求摸到红球的概率。',
            'answer': '球的总数 = 3 + 2 = 5\n红球数 = 3\nP(摸到红球) = 3/5',
            'notes': '概率 = 所求情况数 / 总情况数'
        },
    ]
    
    # 插入数据
    grade_map = {'初一': 1, '初二': 2, '初三': 3}
    
    added = 0
    for m in math_mistakes:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO mistakes 
            (user_id, subject_id, grade_id, question_text, correct_answer, mistake_type, difficulty, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
        ''', ('test_user', math_id, grade_map[m['grade']], m['question'], m['answer'], m['type'], m['difficulty'], now, now))
        
        mistake_id = cursor.lastrowid
        
        # 添加备注
        if m.get('notes'):
            cursor.execute('''
                INSERT INTO mistake_notes (mistake_id, note_type, content, created_at)
                VALUES (?, 'text', ?, ?)
            ''', (mistake_id, m['notes'], now))
        
        added += 1
    
    conn.commit()
    conn.close()
    
    print(f"已添加 {added} 条数学错题")

if __name__ == '__main__':
    generate_math_mistakes()

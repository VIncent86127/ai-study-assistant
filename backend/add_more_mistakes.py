#!/usr/bin/env python3
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db')
cursor = conn.cursor()

# 获取学科和年级ID
cursor.execute("SELECT id FROM subjects WHERE name = '英语'")
subject_id = cursor.fetchone()[0]

cursor.execute("SELECT id, name FROM grades")
grade_map = {row[1]: row[0] for row in cursor.fetchall()}

# 额外的错题数据
extra_questions = [
    ('choice', "The boy _____ is standing there is my brother.\nA. who  B. which  C. whom  D. whose", "A. who", "B. which", '初三', 3, "grammar:定语从句"),
    ('choice', "I don't know if he _____ tomorrow. If he _____, I will tell you.\nA. comes; comes  B. will come; comes  C. comes; will come  D. will come; will come", "B. will come; comes", "A. comes; comes", '初三', 4, "grammar:if引导的条件状语从句"),
    ('choice', "The number of students in our school _____ about 2000.\nA. are  B. is  C. have  D. has", "B. is", "A. are", '初二', 2.5, "grammar:主谓一致"),
    ('choice', "He has _____ friends here, so he feels lonely.\nA. few  B. a few  C. little  D. a little", "A. few", "B. a few", '初二', 2, "grammar:不定代词"),
    ('choice', "_____ useful book it is!\nA. What  B. What a  C. How  D. How a", "B. What a", "A. What", '初二', 2, "grammar:感叹句"),
    ('choice', "He said he _____ the movie before.\nA. has seen  B. had seen  C. saw  D. sees", "B. had seen", "A. has seen", '初三', 3.5, "grammar:过去完成时"),
    ('choice', "The bridge _____ last year.\nA. built  B. was built  C. is built  D. builds", "B. was built", "A. built", '初三', 3, "grammar:被动语态"),
    
    ('cloze', "完形填空：\n\nWhen I was young, I _____(use) to play football every day. But now I _____(prefer) reading books.", "used; prefer", "use; prefering", '初三', 3, "grammar:used to, grammar:一般现在时"),
    ('cloze', "完形填空：\n\nThe story _____(happen) in a small village. A poor boy _____(live) there with his mother.", "happened; lived", "happen; live", '初二', 2, "grammar:一般过去时"),
    
    ('reading', "阅读理解：\n\nPollution is a serious problem today. Many rivers and lakes are polluted. We should do something to protect our environment.\n\n问题：What should we do according to the passage?", "We should do something to protect our environment.", "We should pollute rivers.", '初三', 2.5, ""),
    ('reading', "阅读理解：\n\nLast week, Tom went to the library. He borrowed three books. He likes reading very much.\n\n问题：How many books did Tom borrow?", "Three books.", "Two books.", '初一', 1.5, ""),
    ('reading', "阅读理解：\n\nMobile phones are very useful. We can use them to make calls, send messages and take photos. But some students use phones too much.\n\n问题：What can we do with mobile phones?", "We can make calls, send messages and take photos.", "We can only make calls.", '初二', 2, ""),
    
    ('vocabulary', "用所给词的适当形式填空：\n\nShe made a _____(decide) to study harder.", "decision", "decide", '初二', 2, "grammar:词性转换"),
    ('vocabulary', "根据首字母提示：\n\nBeijing is the c_____ of China.", "capital", "city", '初一', 1, ""),
    ('vocabulary', "用所给词的适当形式填空：\n\nHe is a _____(success) businessman.", "successful", "success", '初三', 2.5, "grammar:词性转换"),
    ('vocabulary', "用所给词的适当形式填空：\n\nThe _____(twelve) month of the year is December.", "twelfth", "twelve", '初一', 1.5, "grammar:序数词"),
    ('vocabulary', "用所给词的适当形式填空：\n\nIt is _____(danger) to swim in the river alone.", "dangerous", "danger", '初二', 2, "grammar:词性转换"),
    
    ('grammar_blank', "语法填空：\n\nI wonder _____ she will come tomorrow.", "if/whether", "that", '初三', 3, "grammar:宾语从句"),
    ('grammar_blank', "语法填空：\n\nThe man _____ you met yesterday is my uncle.", "who/whom/that", "which", '初三', 3, "grammar:定语从句"),
    ('grammar_blank', "语法填空：\n\nNeither Tom nor I _____(be) interested in math.", "am", "is", '初三', 3.5, "grammar:主谓一致"),
    ('grammar_blank', "语法填空：\n\nHe runs as _____(fast) as his brother.", "fast", "faster", '初二', 2, "grammar:同级比较"),
    ('grammar_blank', "语法填空：\n\nThere _____(be) a book and two pens on the desk.", "is", "are", '初二', 2.5, "grammar:there be句型"),
    
    ('writing', "书面表达：写一篇介绍你最好朋友的短文，包括外貌、性格和爱好。", "My Best Friend - My best friend is Lucy. She has long black hair and big eyes. She is kind and helpful. She likes reading books and playing the piano.", "My friend is Lucy. She has hair and eyes. She like reading.", '初二', 3, ""),
    
    ('translation', "翻译句子：\n\n直到他回来，我才离开。", "I didn't leave until he came back.", "I leave until he come back.", '初三', 3, "grammar:not...until"),
    ('translation', "翻译句子：\n\n你认为这部电影怎么样？", "What do you think of this movie? / How do you like this movie?", "What do you think this movie?", '初二', 2, "phrase:think of"),
    ('translation', "翻译句子：\n\n我听说他通过了考试。", "I heard that he had passed the exam.", "I hear he pass the exam.", '初三', 3.5, "grammar:宾语从句, grammar:过去完成时"),
    ('translation', "翻译句子：\n\n她太年轻了，不能独自旅行。", "She is too young to travel alone.", "She too young travel alone.", '初二', 2.5, "grammar:too...to"),
    
    ('task_reading', "任务型阅读：\n\n阅读短文，完成信息表。Tom is 12 years old. He likes playing basketball. His favorite subject is English.", "Name: Tom, Age: 12, Hobby: playing basketball, Favorite subject: English", "Tom is boy. He like basketball.", '初二', 2.5, ""),
    
    ('listening', "听力理解：\n\n根据听到的对话，选择正确答案。\nW: What time do you get up every day?\nM: I get up at 6:30.\n\n问题：What time does the man get up?", "At 6:30.", "At 7:00.", '初一', 1.5, ""),
]

# 插入额外错题
count = 0
for q in extra_questions:
    days_ago = random.randint(0, 30)
    created_at = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    grade_id = grade_map.get(q[4], 2)
    
    cursor.execute('''
        INSERT INTO mistakes (user_id, subject_id, grade_id, question_text, 
                              correct_answer, user_answer, mistake_type, 
                              difficulty, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'test_user',
        subject_id,
        grade_id,
        q[1],
        q[2],
        q[3],
        q[0],
        q[5],
        random.choice(['pending', 'pending', 'pending', 'mastered']),
        created_at,
        created_at
    ))
    count += 1

conn.commit()

# 统计总数
cursor.execute("SELECT COUNT(*) FROM mistakes WHERE user_id = 'test_user'")
total = cursor.fetchone()[0]

conn.close()
print(f"✓ 新增 {count} 条错题")
print(f"✓ 总共 {total} 条错题测试数据")
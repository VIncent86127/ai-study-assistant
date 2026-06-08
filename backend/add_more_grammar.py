#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充更多初二英语语法点
"""

import sqlite3

def get_db():
    return sqlite3.connect('knowledge.db')

def add_grammar_points():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM chapters LIMIT 20")
    chapter_ids = [row[0] for row in cursor.fetchall()]
    
    new_grammar = [
        ('被动语态', 'be + 过去分词', 
         '被动语态表示主语是动作的承受者。',
         'English is spoken by many people. The book was written by Mo Yan.'),
        
        ('宾语从句', '主句 + that/if/whether + 从句',
         '宾语从句在复合句中作主句的宾语。',
         'I think (that) you are right. I do not know if he will come.'),
        
        ('定语从句', '先行词 + 关系词 + 从句',
         '定语从句修饰前面的名词或代词。',
         'The man who is speaking is my teacher.'),
        
        ('状语从句', '主句 + 连词 + 从句',
         '状语从句修饰主句中的动词、形容词或副词。',
         'I will call you when I arrive.'),
        
        ('倒装句', '谓语部分提到主语前面',
         '倒装句分为全部倒装和部分倒装。',
         'There is a book on the desk. Here comes the bus.'),
        
        ('感叹句', 'What/How引导',
         '感叹句表示强烈的感情。',
         'What a nice day it is! How beautiful the flower is!'),
        
        ('反意疑问句', '前句 + 简短问句',
         '反意疑问句遵循前肯后否，前否后肯原则。',
         'You are a student, are not you?'),
        
        ('主谓一致', '主语和谓语保持一致',
         '主语和谓语在人称和数上保持一致。',
         'The number of students is 50.'),
        
        ('名词所有格', '所有格形式',
         's所有格用于有生命的事物，of所有格用于无生命的事物。',
         'Toms book. The door of the room.'),
        
        ('冠词用法', 'a/an/the',
         '不定冠词泛指，定冠词特指。',
         'I have a dog. The dog is cute.'),
        
        ('介词短语', '介词 + 名词',
         '常用介词：at, on, in, for, since, during等。',
         'I get up at 6:00. The book is on the desk.'),
        
        ('时态综合', '八大时态',
         '一般现在时、一般过去时、一般将来时等。',
         'I study English every day.'),
    ]
    
    added = 0
    for i, (name, rule, usage, examples) in enumerate(new_grammar):
        chapter_id = chapter_ids[i % len(chapter_ids)] if chapter_ids else None
        try:
            cursor.execute('''
                INSERT INTO grammar_points (chapter_id, grammar_name, grammar_rule, usage_notes, examples)
                VALUES (?, ?, ?, ?, ?)
            ''', (chapter_id, name, rule, usage, examples))
            added += 1
        except Exception as e:
            pass
    
    conn.commit()
    conn.close()
    print(f'新增语法点: {added}个')

if __name__ == '__main__':
    add_grammar_points()

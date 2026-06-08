#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为现有错题匹配知识点
"""

import sqlite3
import re

def get_db():
    return sqlite3.connect('knowledge.db')

def match_phrases(cursor, question, answer):
    """匹配短语"""
    matches = []
    
    cursor.execute('SELECT id, english, chinese FROM phrases')
    phrases = cursor.fetchall()
    
    question_lower = question.lower()
    answer_lower = (answer or '').lower()
    
    for phrase_id, english, chinese in phrases:
        # 检查英文短语是否出现在题目或答案中
        if english.lower() in question_lower or english.lower() in answer_lower:
            matches.append(('phrase', phrase_id))
        # 检查中文翻译
        elif chinese and (chinese in question or chinese in (answer or '')):
            matches.append(('phrase', phrase_id))
    
    return matches

def match_patterns(cursor, question, answer):
    """匹配句型"""
    matches = []
    
    cursor.execute('SELECT id, pattern, explanation FROM sentence_patterns')
    patterns = cursor.fetchall()
    
    question_lower = question.lower()
    answer_lower = (answer or '').lower()
    
    for pattern_id, pattern, explanation in patterns:
        # 检查句型是否出现在题目中
        if pattern.lower() in question_lower or pattern.lower() in answer_lower:
            matches.append(('pattern', pattern_id))
        # 检查解释关键词
        if explanation:
            # 提取关键词
            keywords = explanation.replace('，', ' ').replace('。', ' ').split()
            for kw in keywords:
                if len(kw) > 2 and kw in question:
                    matches.append(('pattern', pattern_id))
                    break
    
    return matches

def match_grammar(cursor, question, answer):
    """匹配语法点"""
    matches = []
    
    question_lower = question.lower()
    answer_lower = (answer or '').lower()
    combined = question_lower + ' ' + answer_lower
    
    cursor.execute('SELECT id, grammar_name FROM grammar_points')
    grammar_points = cursor.fetchall()
    
    # 语法关键词映射
    grammar_keywords = {
        '一般现在时': ['every day', 'usually', 'often', 'always', 'sometimes', 'on sundays'],
        '一般过去时': ['yesterday', 'last week', 'ago', 'last night', 'in the past'],
        '现在进行时': ['now', 'look', 'listen', 'at the moment', 'ing'],
        '过去进行时': ['was doing', 'were doing', 'at that time'],
        '现在完成时': ['have', 'has', 'yet', 'already', 'ever', 'never', 'just', 'for', 'since'],
        '过去完成时': ['had done', 'by the time', 'before'],
        '一般将来时': ['will', 'going to', 'shall', 'tomorrow', 'next week'],
        '情态动词': ['can', 'could', 'should', 'must', 'may', 'might', 'need', 'would'],
        '被动语态': ['be done', 'is done', 'was done', 'are done', 'were done', 'been'],
        '比较级': ['than', 'er', 'more'],
        '最高级': ['est', 'most', 'one of the'],
        '不定式': ['to do', 'to '],
        '动名词': ['doing', 'enjoy', 'finish', 'practice', 'mind'],
        '定语从句': ['who', 'which', 'that', 'whose', 'whom'],
        '宾语从句': ['that', 'if', 'whether', 'what', 'how'],
        '状语从句': ['when', 'because', 'if', 'although', 'though', 'so', 'until', 'while'],
        'so...that': ['so', 'that'],
        'too...to': ['too', 'to'],
        'enough': ['enough'],
        'used to': ['used to'],
        'there be': ['there is', 'there are', 'there was', 'there were']
    }
    
    for grammar_id, name in grammar_points:
        # 检查语法点名称
        if name in question or name in (answer or ''):
            matches.append(('grammar', grammar_id))
            continue
        
        # 检查关键词
        for kw_name, indicators in grammar_keywords.items():
            if kw_name in name or name in kw_name:
                for indicator in indicators:
                    if indicator in combined:
                        matches.append(('grammar', grammar_id))
                        break
    
    return matches

def link_mistakes_to_knowledge():
    """为所有错题匹配知识点"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取所有错题
    cursor.execute('''
        SELECT m.id, m.question_text, m.correct_answer, m.mistake_type
        FROM mistakes m
        WHERE NOT EXISTS (
            SELECT 1 FROM mistake_knowledge_links mkl 
            WHERE mkl.mistake_id = m.id
        )
    ''')
    mistakes = cursor.fetchall()
    
    print(f'需要匹配的错题数: {len(mistakes)}')
    
    linked_count = 0
    
    for mistake_id, question, answer, mistake_type in mistakes:
        all_matches = []
        
        # 匹配短语
        all_matches.extend(match_phrases(cursor, question, answer))
        
        # 匹配句型
        all_matches.extend(match_patterns(cursor, question, answer))
        
        # 匹配语法点
        all_matches.extend(match_grammar(cursor, question, answer))
        
        # 去重
        unique_matches = list(set(all_matches))
        
        # 如果没有匹配到任何知识点，根据题型随机关联
        if not unique_matches:
            if 'choice' in (mistake_type or '') or '单项选择' in question:
                cursor.execute("SELECT id FROM grammar_points ORDER BY RANDOM() LIMIT 2")
                for row in cursor.fetchall():
                    unique_matches.append(('grammar', row[0]))
            elif 'translation' in (mistake_type or '') or '翻译' in question:
                cursor.execute("SELECT id FROM sentence_patterns ORDER BY RANDOM() LIMIT 2")
                for row in cursor.fetchall():
                    unique_matches.append(('pattern', row[0]))
            elif 'vocabulary' in (mistake_type or '') or '词汇' in question:
                cursor.execute("SELECT id FROM phrases ORDER BY RANDOM() LIMIT 2")
                for row in cursor.fetchall():
                    unique_matches.append(('phrase', row[0]))
            else:
                # 随机关联一些知识点
                cursor.execute("SELECT id FROM phrases ORDER BY RANDOM() LIMIT 1")
                unique_matches.append(('phrase', cursor.fetchone()[0]))
                cursor.execute("SELECT id FROM grammar_points ORDER BY RANDOM() LIMIT 1")
                unique_matches.append(('grammar', cursor.fetchone()[0]))
        
        # 插入关联
        for knowledge_type, knowledge_id in unique_matches[:5]:  # 最多5个知识点
            try:
                cursor.execute('''
                    INSERT INTO mistake_knowledge_links (mistake_id, knowledge_type, knowledge_id)
                    VALUES (?, ?, ?)
                ''', (mistake_id, knowledge_type, knowledge_id))
                linked_count += 1
            except:
                pass
    
    conn.commit()
    conn.close()
    
    print(f'成功创建关联: {linked_count}条')
    
    # 验证
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM mistake_knowledge_links')
    print(f'数据库中关联总数: {cursor.fetchone()[0]}条')
    conn.close()

if __name__ == '__main__':
    link_mistakes_to_knowledge()

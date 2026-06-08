#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 错题集API路由
"""

from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
import json
import re

mistake_bp = Blueprint('mistakes', __name__)

DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@mistake_bp.route('/api/mistakes', methods=['GET'])
def get_mistakes():
    """获取错题列表"""
    user_id = request.args.get('user_id', 'default')
    subject_id = request.args.get('subject_id')
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT m.*, s.name as subject_name, g.name as grade_name, c.chapter_name
        FROM mistakes m
        LEFT JOIN subjects s ON m.subject_id = s.id
        LEFT JOIN grades g ON m.grade_id = g.id
        LEFT JOIN chapters c ON m.chapter_id = c.id
        WHERE m.user_id = ?
    '''
    params = [user_id]
    
    if subject_id:
        query += ' AND m.subject_id = ?'
        params.append(subject_id)
    
    if status:
        query += ' AND m.status = ?'
        params.append(status)
    
    # 获取总数
    count_query = query.replace('SELECT m.*, s.name as subject_name, g.name as grade_name, c.chapter_name', 'SELECT COUNT(*)')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # 分页
    query += ' ORDER BY m.created_at DESC LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    mistakes = []
    for row in rows:
        mistakes.append({
            'id': row['id'],
            'subject_name': row['subject_name'],
            'grade_name': row['grade_name'],
            'chapter_name': row['chapter_name'],
            'question_text': row['question_text'],
            'correct_answer': row['correct_answer'],
            'user_answer': row['user_answer'],
            'mistake_type': row['mistake_type'],
            'difficulty': row['difficulty'],
            'status': row['status'],
            'created_at': row['created_at']
        })
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': mistakes,
        'total': total,
        'page': page,
        'per_page': per_page
    })


@mistake_bp.route('/api/mistakes/<int:mistake_id>', methods=['GET'])
def get_mistake_detail(mistake_id):
    """获取错题详情"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取错题基本信息
    cursor.execute('''
        SELECT m.*, s.name as subject_name, g.name as grade_name, c.chapter_name
        FROM mistakes m
        LEFT JOIN subjects s ON m.subject_id = s.id
        LEFT JOIN grades g ON m.grade_id = g.id
        LEFT JOIN chapters c ON m.chapter_id = c.id
        WHERE m.id = ?
    ''', (mistake_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'error': '错题不存在'}), 404
    
    mistake = dict(row)
    
    # 获取关联知识点
    cursor.execute('''
        SELECT mkl.knowledge_type, mkl.knowledge_id,
               CASE 
                   WHEN mkl.knowledge_type = 'phrase' THEN p.english || ' - ' || p.chinese
                   WHEN mkl.knowledge_type = 'pattern' THEN sp.pattern
                   WHEN mkl.knowledge_type = 'grammar' THEN gp.grammar_name
               END as knowledge_content
        FROM mistake_knowledge_links mkl
        LEFT JOIN phrases p ON mkl.knowledge_type = 'phrase' AND mkl.knowledge_id = p.id
        LEFT JOIN sentence_patterns sp ON mkl.knowledge_type = 'pattern' AND mkl.knowledge_id = sp.id
        LEFT JOIN grammar_points gp ON mkl.knowledge_type = 'grammar' AND mkl.knowledge_id = gp.id
        WHERE mkl.mistake_id = ?
    ''', (mistake_id,))
    
    mistake['knowledge_points'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取生僻词
    cursor.execute('''
        SELECT id, word, meaning, phonetic, example_usage
        FROM vocabulary_notes
        WHERE mistake_id = ?
    ''', (mistake_id,))
    
    mistake['vocabulary'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取备注
    cursor.execute('''
        SELECT id, note_type, content, voice_duration, created_at
        FROM mistake_notes
        WHERE mistake_id = ?
        ORDER BY created_at DESC
    ''', (mistake_id,))
    
    mistake['notes'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取复习记录
    cursor.execute('''
        SELECT id, review_date, result, review_notes
        FROM review_records
        WHERE mistake_id = ?
        ORDER BY review_date DESC
    ''', (mistake_id,))
    
    mistake['review_history'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': mistake
    })


@mistake_bp.route('/api/mistakes', methods=['POST'])
def create_mistake():
    """创建新错题"""
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO mistakes (user_id, subject_id, grade_id, chapter_id, 
                              question_text, correct_answer, user_answer,
                              mistake_type, difficulty, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('user_id', 'default'),
        data.get('subject_id'),
        data.get('grade_id'),
        data.get('chapter_id'),
        data.get('question_text'),
        data.get('correct_answer'),
        data.get('user_answer'),
        data.get('mistake_type', 'unknown'),
        data.get('difficulty', 'medium'),
        data.get('status', 'pending'),
        now, now
    ))
    
    mistake_id = cursor.lastrowid
    
    # 插入关联知识点
    knowledge_points = data.get('knowledge_points', [])
    for kp in knowledge_points:
        cursor.execute('''
            INSERT INTO mistake_knowledge_links (mistake_id, knowledge_type, knowledge_id)
            VALUES (?, ?, ?)
        ''', (mistake_id, kp['type'], kp['id']))
    
    # 插入生僻词
    vocabulary = data.get('vocabulary', [])
    for vocab in vocabulary:
        cursor.execute('''
            INSERT INTO vocabulary_notes (mistake_id, word, meaning, phonetic, example_usage)
            VALUES (?, ?, ?, ?, ?)
        ''', (mistake_id, vocab.get('word'), vocab.get('meaning'), 
              vocab.get('phonetic'), vocab.get('example_usage')))
    
    # 插入备注
    notes = data.get('notes', [])
    for note in notes:
        cursor.execute('''
            INSERT INTO mistake_notes (mistake_id, note_type, content, voice_duration)
            VALUES (?, ?, ?, ?)
        ''', (mistake_id, note.get('type', 'text'), note.get('content'), 
              note.get('voice_duration')))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'data': {'id': mistake_id}
    })


@mistake_bp.route('/api/mistakes/<int:mistake_id>', methods=['PUT'])
def update_mistake(mistake_id):
    """更新错题"""
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    update_fields = []
    params = []
    
    for field in ['correct_answer', 'user_answer', 'mistake_type', 'difficulty', 'status', 'chapter_id']:
        if field in data:
            update_fields.append(f'{field} = ?')
            params.append(data[field])
    
    if update_fields:
        update_fields.append('updated_at = ?')
        params.append(now)
        params.append(mistake_id)
        
        cursor.execute(f'''
            UPDATE mistakes SET {', '.join(update_fields)}
            WHERE id = ?
        ''', params)
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})


@mistake_bp.route('/api/mistakes/<int:mistake_id>', methods=['DELETE'])
def delete_mistake(mistake_id):
    """删除错题"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM mistakes WHERE id = ?', (mistake_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})


@mistake_bp.route('/api/mistakes/<int:mistake_id>/notes', methods=['POST'])
def add_note(mistake_id):
    """添加备注"""
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO mistake_notes (mistake_id, note_type, content, voice_duration)
        VALUES (?, ?, ?, ?)
    ''', (
        mistake_id,
        data.get('type', 'text'),
        data.get('content'),
        data.get('voice_duration')
    ))
    
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'data': {'id': note_id}
    })


@mistake_bp.route('/api/mistakes/<int:mistake_id>/review', methods=['POST'])
def add_review(mistake_id):
    """添加复习记录"""
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO review_records (mistake_id, review_date, result, review_notes)
        VALUES (?, ?, ?, ?)
    ''', (mistake_id, now, data.get('result'), data.get('review_notes')))
    
    # 如果答对了3次，更新状态为已掌握
    if data.get('result') == 'correct':
        cursor.execute('''
            SELECT COUNT(*) FROM review_records 
            WHERE mistake_id = ? AND result = 'correct'
        ''', (mistake_id,))
        correct_count = cursor.fetchone()[0]
        
        if correct_count >= 3:
            cursor.execute('''
                UPDATE mistakes SET status = 'mastered', updated_at = ?
                WHERE id = ?
            ''', (now, mistake_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})


@mistake_bp.route('/api/mistakes/analyze', methods=['POST'])
def analyze_question():
    """分析题目，提取知识点和生僻词"""
    data = request.get_json()
    question_text = data.get('question_text', '')
    subject_id = data.get('subject_id')
    
    conn = get_db()
    cursor = conn.cursor()
    
    result = {
        'knowledge_points': [],
        'vocabulary': []
    }
    
    # 如果是英语学科，匹配知识点
    if subject_id:
        cursor.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,))
        subject = cursor.fetchone()
        
        if subject and subject['name'] == '英语':
            # 匹配短语
            cursor.execute('''
                SELECT p.id, p.english, p.chinese, c.chapter_name
                FROM phrases p
                JOIN chapters c ON p.chapter_id = c.id
            ''')
            
            for row in cursor.fetchall():
                if row['english'].lower() in question_text.lower():
                    result['knowledge_points'].append({
                        'type': 'phrase',
                        'id': row['id'],
                        'content': f"{row['english']} - {row['chinese']}",
                        'chapter': row['chapter_name']
                    })
            
            # 匹配句型关键词
            cursor.execute('''
                SELECT sp.id, sp.pattern, sp.explanation, c.chapter_name
                FROM sentence_patterns sp
                JOIN chapters c ON sp.chapter_id = c.id
            ''')
            
            for row in cursor.fetchall():
                # 简单匹配：如果句型关键词出现在题目中
                keywords = re.findall(r'[A-Za-z]+', row['pattern'])
                if any(kw.lower() in question_text.lower() for kw in keywords if len(kw) > 3):
                    result['knowledge_points'].append({
                        'type': 'pattern',
                        'id': row['id'],
                        'content': row['pattern'],
                        'chapter': row['chapter_name']
                    })
            
            # 提取生僻词（简单实现：提取较长英文单词）
            english_words = re.findall(r'\b[a-zA-Z]{6,}\b', question_text)
            common_words = {'because', 'should', 'would', 'could', 'during', 'before', 
                          'after', 'between', 'through', 'although', 'however'}
            
            for word in set(english_words):
                if word.lower() not in common_words:
                    result['vocabulary'].append({
                        'word': word,
                        'meaning': '',  # 需要后续填充
                        'phonetic': ''
                    })
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': result
    })


@mistake_bp.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取错题统计"""
    user_id = request.args.get('user_id', 'default')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 按学科统计
    cursor.execute('''
        SELECT s.name, COUNT(*) as count
        FROM mistakes m
        JOIN subjects s ON m.subject_id = s.id
        WHERE m.user_id = ?
        GROUP BY m.subject_id
    ''', (user_id,))
    
    by_subject = [{'name': row['name'], 'count': row['count']} for row in cursor.fetchall()]
    
    # 按状态统计
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM mistakes
        WHERE user_id = ?
        GROUP BY status
    ''', (user_id,))
    
    by_status = [{'status': row['status'], 'count': row['count']} for row in cursor.fetchall()]
    
    # 按难度统计
    cursor.execute('''
        SELECT difficulty, COUNT(*) as count
        FROM mistakes
        WHERE user_id = ?
        GROUP BY difficulty
    ''', (user_id,))
    
    by_difficulty = [{'difficulty': row['difficulty'], 'count': row['count']} for row in cursor.fetchall()]
    
    # 最近复习情况
    cursor.execute('''
        SELECT COUNT(*) as count
        FROM review_records rr
        JOIN mistakes m ON rr.mistake_id = m.id
        WHERE m.user_id = ? AND rr.review_date >= date('now', '-7 days')
    ''', (user_id,))
    
    weekly_reviews = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': {
            'by_subject': by_subject,
            'by_status': by_status,
            'by_difficulty': by_difficulty,
            'weekly_reviews': weekly_reviews
        }
    })


@mistake_bp.route('/api/ai/generate-question', methods=['POST'])
def generate_similar_question():
    """AI生成类似题目"""
    data = request.get_json()
    
    model = data.get('model', 'glm')
    original_question = data.get('original_question', '')
    correct_answer = data.get('correct_answer', '')
    knowledge_points = data.get('knowledge_points', '')
    question_type = data.get('mistake_type', 'choice')
    difficulty = data.get('difficulty', 2)
    
    # 根据不同模型生成题目
    # 这里先返回模拟数据，实际需要调用对应AI API
    
    # 模拟不同模型的响应
    mock_responses = {
        'gpt': {
            'question': f"[GPT生成] 根据知识点【{knowledge_points}】，请选择正确的答案：\nShe _____ to the cinema yesterday.\nA. go  B. goes  C. went  D. going",
            'answer': 'C. went（一般过去时，用动词过去式）'
        },
        'claude': {
            'question': f"[Claude生成] 基于【{knowledge_points}】的练习题：\n用括号内动词的正确形式填空：\nThey _____(watch) a movie last night.",
            'answer': 'watched（last night表示过去，用一般过去时）'
        },
        'glm': {
            'question': f"[GLM生成] 请根据【{knowledge_points}】完成下列题目：\n单项选择：\nI _____ breakfast at 7:00 this morning.\nA. have  B. has  C. had  D. having",
            'answer': 'C. had（this morning表示今天早上，是过去的时间，用一般过去时）'
        },
        'qwen': {
            'question': f"[通义千问生成] 针对知识点【{knowledge_points}】的练习：\n翻译句子：\n他昨天去了公园。",
            'answer': 'He went to the park yesterday.（yesterday是过去时间，go变成went）'
        }
    }
    
    response = mock_responses.get(model, mock_responses['glm'])
    
    return jsonify({
        'success': True,
        'data': response
    })
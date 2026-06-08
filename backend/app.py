#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 后端API服务
Flask + 智能问答接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

# 导入错题集路由
from mistake_routes import mistake_bp

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(mistake_bp)

# 配置
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# ==================== 用户相关 ====================

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """获取用户信息"""
    # TODO: 从数据库获取用户信息
    return jsonify({
        'code': 0,
        'data': {
            'userId': 'test_user',
            'nickname': '同学',
            'grade': '初中一年级',
            'avatar': '',
            'totalQuestions': 128,
            'studyDays': 15,
            'masteredPoints': 42
        }
    })

@app.route('/api/user/update', methods=['POST'])
def update_user_profile():
    """更新用户信息"""
    data = request.get_json()
    # TODO: 更新用户信息到数据库
    return jsonify({'code': 0, 'message': '更新成功'})

# ==================== AI问答 ====================

@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """AI问答接口"""
    data = request.get_json()
    question = data.get('question', '')
    subject = data.get('subject', '全部')
    context = data.get('context', [])
    
    # TODO: 调用AI模型生成回答
    # 这里先返回模拟数据
    response = generate_ai_response(question, subject)
    
    return jsonify({
        'code': 0,
        'data': {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
    })

def generate_ai_response(question, subject):
    """生成AI回复（模拟）"""
    # 实际项目中需要调用大模型API
    responses = {
        '数学': '这道数学题很有意思。让我来分析一下思路：\n\n1. 首先，我们需要理解题目要求\n2. 然后，找出已知条件和未知量\n3. 建立方程或关系式\n4. 求解并验证\n\n你能告诉我具体的题目内容吗？',
        '语文': '这是一个很好的语文问题。让我来帮你分析：\n\n从文章的结构、修辞手法和中心思想几个角度来看...',
        '英语': '英语学习中，这个问题很常见。\n\n这个语法的核心用法是...\n\n例句：...',
        '物理': '物理问题需要我们分析力和运动的关系。\n\n根据牛顿定律...',
        'default': '这是一个很好的问题！让我来帮你分析一下。请详细描述你遇到的具体问题，我会尽力帮助你理解。'
    }
    return responses.get(subject, responses['default'])

# ==================== 作业辅导 ====================

@app.route('/api/homework/analyze', methods=['POST'])
def analyze_homework():
    """分析作业图片"""
    if 'image' not in request.files:
        return jsonify({'code': 1, 'message': '请上传图片'}), 400
    
    image = request.files['image']
    subject = request.form.get('subject', '数学')
    
    # TODO: 调用OCR识别 + AI分析
    # 返回模拟数据
    return jsonify({
        'code': 0,
        'data': {
            'questionType': '计算题',
            'difficulty': '中等',
            'knowledgePoints': '一元二次方程、因式分解',
            'solution': '1. 观察方程结构\n2. 尝试因式分解\n3. 求解方程',
            'answer': 'x₁=2, x₂=3',
            'similarQuestions': []
        }
    })

# ==================== 学习进度 ====================

@app.route('/api/progress/stats', methods=['GET'])
def get_progress_stats():
    """获取学习进度统计"""
    # TODO: 从数据库获取统计数据
    return jsonify({
        'code': 0,
        'data': {
            'totalQuestions': 128,
            'studyDays': 15,
            'masteredPoints': 42,
            'weeklyData': [12, 15, 8, 20, 18, 25, 30],
            'subjectProgress': [
                {'subject': '数学', 'percent': 75},
                {'subject': '英语', 'percent': 60},
                {'subject': '物理', 'percent': 45},
                {'subject': '语文', 'percent': 80}
            ]
        }
    })

@app.route('/api/progress/record', methods=['POST'])
def record_progress():
    """记录学习进度"""
    data = request.get_json()
    # TODO: 保存学习记录到数据库
    return jsonify({'code': 0, 'message': '记录成功'})

# ==================== 学科相关 ====================

@app.route('/api/subjects/list', methods=['GET'])
def get_subjects():
    """获取学科列表"""
    return jsonify({
        'code': 0,
        'data': {
            'subjects': ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治']
        }
    })

@app.route('/api/subjects/<subject>/knowledge', methods=['GET'])
def get_knowledge_points(subject):
    """获取学科知识点"""
    # TODO: 从数据库获取知识点列表
    knowledge_data = {
        '数学': [
            {'id': 1, 'name': '一元二次方程', 'desc': '解方程、应用题', 'questionCount': 25},
            {'id': 2, 'name': '几何证明', 'desc': '三角形、四边形', 'questionCount': 30}
        ]
    }
    return jsonify({
        'code': 0,
        'data': knowledge_data.get(subject, [])
    })

# ==================== 健康检查 ====================

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
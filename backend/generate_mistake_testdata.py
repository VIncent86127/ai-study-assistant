#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 错题集测试数据生成
生成50条初中英语错题数据
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'

# 错题模板数据
MISTAKE_TEMPLATES = [
    # 单项选择
    {
        'type': 'choice',
        'questions': [
            {
                'text': 'She _____ to school by bike every day.\nA. go  B. goes  C. going  D. went',
                'answer': 'B. goes',
                'user_answer': 'A. go',
                'knowledge': 'phrase:go to school',
                'vocab': '',
                'grade': '初二',
                'difficulty': 1.5
            },
            {
                'text': 'The book is _____ than that one.\nA. interesting  B. more interesting  C. most interesting  D. the most interesting',
                'answer': 'B. more interesting',
                'user_answer': 'C. most interesting',
                'knowledge': 'grammar:比较级',
                'vocab': 'interesting',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': 'I have been waiting for him _____ two hours.\nA. since  B. for  C. in  D. at',
                'answer': 'B. for',
                'user_answer': 'A. since',
                'knowledge': 'grammar:现在完成时',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': 'He asked me _____ I could help him.\nA. that  B. what  C. if  D. which',
                'answer': 'C. if',
                'user_answer': 'A. that',
                'knowledge': 'grammar:宾语从句',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3
            },
            {
                'text': 'The teacher told us _____ late for class.\nA. not be  B. not to be  C. don\'t be  D. to not be',
                'answer': 'B. not to be',
                'user_answer': 'A. not be',
                'knowledge': 'grammar:动词不定式',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': 'There are many _____ in the zoo.\nA. monkey  B. monkeys  C. monkeies  D. monkeyes',
                'answer': 'B. monkeys',
                'user_answer': 'C. monkeies',
                'knowledge': 'grammar:名词复数',
                'vocab': 'monkey',
                'grade': '初一',
                'difficulty': 1
            },
            {
                'text': 'She enjoys _____ music in her free time.\nA. listen to  B. listening to  C. to listen to  D. listened to',
                'answer': 'B. listening to',
                'user_answer': 'A. listen to',
                'knowledge': 'phrase:enjoy doing, phrase:listen to',
                'vocab': 'enjoy',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': 'I don\'t know _____ to do next.\nA. how  B. what  C. which  D. where',
                'answer': 'B. what',
                'user_answer': 'A. how',
                'knowledge': 'grammar:宾语从句',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3
            },
            {
                'text': 'The movie was _____ interesting _____ I wanted to see it again.\nA. so; that  B. such; that  C. too; to  D. very; that',
                'answer': 'A. so; that',
                'user_answer': 'B. such; that',
                'knowledge': 'grammar:结果状语从句',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3.5
            },
            {
                'text': '_____ it rains tomorrow, we will stay at home.\nA. If  B. Unless  C. Until  D. Although',
                'answer': 'A. If',
                'user_answer': 'B. Unless',
                'knowledge': 'grammar:条件状语从句',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2
            }
        ]
    },
    # 完形填空
    {
        'type': 'cloze',
        'questions': [
            {
                'text': 'Last Sunday, I went to the park with my friends. We _____(1) a good time there. First, we _____(2) kites. Then we sat under a big tree and _____(3) some water. At noon, we _____(4) lunch together. We were all very happy.\n\n1. A. have  B. has  C. had  D. having',
                'answer': 'C. had',
                'user_answer': 'A. have',
                'knowledge': 'grammar:一般过去时',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': 'Tom is a good student. He always _____(finish) his homework on time. Yesterday, he _____(study) until 10 o\'clock.',
                'answer': 'finishes; studied',
                'user_answer': 'finish; study',
                'knowledge': 'grammar:一般现在时, grammar:一般过去时',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': 'The book _____(write) by Lu Xun is very popular. It _____(sell) well in our school.',
                'answer': 'written; sells',
                'user_answer': 'writing; is sold',
                'knowledge': 'grammar:过去分词作定语, grammar:主动表被动',
                'vocab': '',
                'grade': '初三',
                'difficulty': 4
            }
        ]
    },
    # 阅读理解
    {
        'type': 'reading',
        'questions': [
            {
                'text': '阅读短文，回答问题：\n\nMany people think that the sun is the biggest star. In fact, there are many stars much bigger than the sun. The sun looks bigger because it is much nearer to us than other stars.\n\n问题：Why does the sun look bigger than other stars?',
                'answer': 'Because it is much nearer to us than other stars.',
                'user_answer': 'Because it is the biggest star.',
                'knowledge': '',
                'vocab': 'fact, actually',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': '阅读理解：\n\nIn England, people often talk about the weather because the weather can change quickly. They can have four seasons in one day.\n\n问题：Why do English people often talk about the weather?',
                'answer': 'Because the weather can change quickly.',
                'user_answer': 'Because they like talking.',
                'knowledge': '',
                'vocab': 'weather, season',
                'grade': '初一',
                'difficulty': 1.5
            },
            {
                'text': '阅读理解：\n\nComputer games are very popular among teenagers. Some parents worry that their children spend too much time playing games. They think it is bad for their studies.\n\n问题：What do some parents worry about?',
                'answer': 'They worry that their children spend too much time playing games.',
                'user_answer': 'They worry about computers.',
                'knowledge': 'phrase:spend time doing',
                'vocab': 'popular, worry',
                'grade': '初三',
                'difficulty': 2.5
            }
        ]
    },
    # 词汇运用
    {
        'type': 'vocabulary',
        'questions': [
            {
                'text': '用所给词的适当形式填空：\n\nShe is _____ (happy) because she failed the exam.',
                'answer': 'unhappy',
                'user_answer': 'happy',
                'knowledge': '',
                'vocab': 'happy, unhappy, prefix',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': '根据首字母提示完成单词：\n\nWe should protect the e_____ because it is our home.',
                'answer': 'environment',
                'user_answer': 'earth',
                'knowledge': '',
                'vocab': 'environment',
                'grade': '初三',
                'difficulty': 3
            },
            {
                'text': '用所给词的适当形式填空：\n\nThe _____ (difficult) of the problem made us worried.',
                'answer': 'difficulty',
                'user_answer': 'difficult',
                'knowledge': 'grammar:词性转换',
                'vocab': 'difficult, difficulty',
                'grade': '初三',
                'difficulty': 2.5
            },
            {
                'text': '根据中文提示完成句子：\n\nHe _____ _____ (照顾) his little sister when his mother was away.',
                'answer': 'looked after / took care of',
                'user_answer': 'looked for',
                'knowledge': 'phrase:look after, phrase:take care of',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2
            },
            {
                'text': '用所给词的适当形式填空：\n\nIt is _____ (help) to learn English by reading English books.',
                'answer': 'helpful',
                'user_answer': 'help',
                'knowledge': 'grammar:词性转换',
                'vocab': 'help, helpful',
                'grade': '初二',
                'difficulty': 2
            }
        ]
    },
    # 语法填空
    {
        'type': 'grammar_blank',
        'questions': [
            {
                'text': '语法填空：\n\nI have a good friend. _____(she) name is Lucy. She is from America.',
                'answer': 'Her',
                'user_answer': 'She',
                'knowledge': 'grammar:形容词性物主代词',
                'vocab': '',
                'grade': '初一',
                'difficulty': 1.5
            },
            {
                'text': '语法填空：\n\nThe book _____(write) by Mo Yan is very interesting.',
                'answer': 'written',
                'user_answer': 'writing',
                'knowledge': 'grammar:过去分词作定语',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3.5
            },
            {
                'text': '语法填空：\n\nIt took me two hours _____(finish) my homework yesterday.',
                'answer': 'to finish',
                'user_answer': 'finishing',
                'knowledge': 'phrase:It takes sb. time to do sth.',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': '语法填空：\n\nThe teacher made us _____(clean) the classroom after school.',
                'answer': 'clean',
                'user_answer': 'to clean',
                'knowledge': 'grammar:使役动词make',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3
            },
            {
                'text': '语法填空：\n\nHe is one of the _____(tall) students in our class.',
                'answer': 'tallest',
                'user_answer': 'taller',
                'knowledge': 'grammar:最高级',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            }
        ]
    },
    # 书面表达
    {
        'type': 'writing',
        'questions': [
            {
                'text': '书面表达：\n\n请根据以下提示，以"My Summer Vacation"为题写一篇短文：\n1. 去年夏天你和家人去了北京\n2. 参观了长城和故宫\n3. 品尝了北京烤鸭\n4. 你的感受',
                'answer': 'My Summer Vacation\n\nLast summer, I went to Beijing with my family. We visited the Great Wall and the Forbidden City. The Great Wall was very long and magnificent. We also tasted Beijing roast duck, which was delicious. I felt very happy and learned a lot about Chinese history.',
                'user_answer': 'Last summer I go to Beijing with family. We visit Great Wall. It good.',
                'knowledge': 'grammar:一般过去时, pattern:go to sp.',
                'vocab': 'vacation, visit, delicious',
                'grade': '初二',
                'difficulty': 3
            },
            {
                'text': '书面表达：\n\n假如你是李明，你的美国笔友Tom想了解中国的传统节日。请给他写一封信，介绍春节（Spring Festival）。',
                'answer': 'Dear Tom,\n\nI\'m glad to tell you about the Spring Festival. It is the most important traditional festival in China. Before the festival, people clean their houses and buy new clothes. On the eve of the Spring Festival, families get together and have a big dinner. Children can get lucky money from their parents. During the festival, people visit relatives and friends.\n\nBest wishes!\nLi Ming',
                'user_answer': 'Dear Tom, Spring Festival is important. People eat dinner. Children get money.',
                'knowledge': '',
                'vocab': 'festival, traditional, relative',
                'grade': '初三',
                'difficulty': 3.5
            }
        ]
    },
    # 翻译
    {
        'type': 'translation',
        'questions': [
            {
                'text': '翻译句子：\n\n我每天花半小时做作业。',
                'answer': 'I spend half an hour doing my homework every day. / It takes me half an hour to do my homework every day.',
                'user_answer': 'I take half hour do homework every day.',
                'knowledge': 'phrase:spend time doing, phrase:It takes sb. time to do',
                'vocab': '',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': '翻译句子：\n\n他太累了，以至于无法继续工作。',
                'answer': 'He was too tired to go on working. / He was so tired that he couldn\'t go on working.',
                'user_answer': 'He too tired can\'t work.',
                'knowledge': 'grammar:too...to..., grammar:so...that...',
                'vocab': 'tired, continue',
                'grade': '初三',
                'difficulty': 3
            },
            {
                'text': '翻译句子：\n\n这本书比那本书有趣得多。',
                'answer': 'This book is much more interesting than that one.',
                'user_answer': 'This book interesting than that book.',
                'knowledge': 'grammar:比较级',
                'vocab': 'interesting',
                'grade': '初二',
                'difficulty': 2.5
            },
            {
                'text': '翻译句子：\n\n他说他已经完成了作业。',
                'answer': 'He said that he had finished his homework.',
                'user_answer': 'He said he finished homework.',
                'knowledge': 'grammar:宾语从句, grammar:过去完成时',
                'vocab': '',
                'grade': '初三',
                'difficulty': 3.5
            }
        ]
    }
]


def generate_test_data():
    """生成测试数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取学科和年级ID
    cursor.execute("SELECT id FROM subjects WHERE name = '英语'")
    subject_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id, name FROM grades")
    grade_map = {row[1]: row[0] for row in cursor.fetchall()}
    
    # 生成错题
    count = 0
    for template in MISTAKE_TEMPLATES:
        for q in template['questions']:
            # 随机生成创建时间（最近30天内）
            days_ago = random.randint(0, 30)
            created_at = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            
            # 确定年级ID
            grade_id = grade_map.get(q['grade'], 2)  # 默认初二
            
            # 插入错题
            cursor.execute('''
                INSERT INTO mistakes (user_id, subject_id, grade_id, question_text, 
                                      correct_answer, user_answer, mistake_type, 
                                      difficulty, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'test_user',
                subject_id,
                grade_id,
                q['text'],
                q['answer'],
                q['user_answer'],
                template['type'],
                q['difficulty'],
                random.choice(['pending', 'pending', 'pending', 'mastered']),  # 75%待复习
                created_at,
                created_at
            ))
            
            mistake_id = cursor.lastrowid
            count += 1
            
            # 插入生僻词
            if q.get('vocab'):
                words = [w.strip() for w in q['vocab'].split(',')]
                for word in words:
                    if word:
                        cursor.execute('''
                            INSERT INTO vocabulary_notes (mistake_id, word, meaning)
                            VALUES (?, ?, ?)
                        ''', (mistake_id, word, ''))
            
            # 插入备注（随机）
            if random.random() < 0.3:  # 30%的错题有备注
                notes = [
                    '这题考查的是时态，要注意动词的变化',
                    '下次遇到类似的题要仔细审题',
                    '这个知识点我总是记不住',
                    '需要多练习这类题目'
                ]
                cursor.execute('''
                    INSERT INTO mistake_notes (mistake_id, note_type, content)
                    VALUES (?, ?, ?)
                ''', (mistake_id, 'text', random.choice(notes)))
            
            # 插入复习记录（已掌握的错题）
            if random.random() < 0.25:  # 25%有复习记录
                cursor.execute('''
                    INSERT INTO review_records (mistake_id, result, review_date)
                    VALUES (?, ?, ?)
                ''', (mistake_id, 'correct', created_at))
    
    conn.commit()
    conn.close()
    
    print(f"✓ 已生成 {count} 条错题测试数据")


if __name__ == '__main__':
    generate_test_data()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充更多初二英语句型
"""

import sqlite3

def get_db():
    return sqlite3.connect('knowledge.db')

def add_patterns():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM chapters LIMIT 20")
    chapter_ids = [row[0] for row in cursor.fetchall()]
    
    new_patterns = [
        ('It takes sb. some time to do sth.', '做某事花费某人多长时间', 'It takes me an hour to do homework.'),
        ('sb. spend(s) time/money (in) doing sth.', '某人花费时间/金钱做某事', 'I spend two hours reading.'),
        ('sb. spend(s) money on sth.', '某人花钱买某物', 'I spent 50 yuan on this book.'),
        ('It is + adj. + for sb. to do sth.', '做某事对某人来说怎么样', 'It is important for us to learn English.'),
        ('It is + adj. + of sb. to do sth.', '某人做某事怎么样（形容人的品质）', 'It is kind of you to help me.'),
        ('Why don\'t you + 动词原形?', '为什么不...呢？（表建议）', 'Why don\'t you go with us?'),
        ('Why not + 动词原形?', '为什么不...呢？（表建议）', 'Why not go swimming?'),
        ('Would you like to do sth.?', '你愿意做某事吗？', 'Would you like to have a cup of tea?'),
        ('Would you mind doing sth.?', '你介意做某事吗？', 'Would you mind opening the window?'),
        ('I\'d like to do sth.', '我想要做某事', 'I would like to visit Beijing.'),
        ('prefer to do sth. rather than do sth.', '宁愿做...而不愿做...', 'I prefer to walk rather than take a bus.'),
        ('prefer doing sth. to doing sth.', '比起做...更喜欢做...', 'I prefer reading to watching TV.'),
        ('find it + adj. + to do sth.', '发现做某事怎么样', 'I find it hard to learn math.'),
        ('make sb. + adj.', '使某人怎么样', 'The news made me happy.'),
        ('make sb. do sth.', '使某人做某事', 'The teacher made us clean the room.'),
        ('let sb. do sth.', '让某人做某事', 'Let me help you.'),
        ('ask/tell/want sb. to do sth.', '请求/告诉/想要某人做某事', 'He asked me to help him.'),
        ('be afraid of doing sth.', '害怕做某事', 'I am afraid of speaking in public.'),
        ('be afraid to do sth.', '不敢做某事', 'He is afraid to swim in the river.'),
        ('look forward to doing sth.', '期待做某事', 'I look forward to seeing you.'),
        ('used to do sth.', '过去常常做某事', 'I used to play basketball.'),
        ('be used to doing sth.', '习惯于做某事', 'I am used to getting up early.'),
        ('be interested in doing sth.', '对做某事感兴趣', 'I am interested in learning English.'),
        ('be good at doing sth.', '擅长做某事', 'She is good at dancing.'),
        ('have fun doing sth.', '做某事很开心', 'We had fun playing games.'),
        ('practice doing sth.', '练习做某事', 'I practice playing the piano every day.'),
        ('enjoy doing sth.', '喜欢做某事', 'I enjoy listening to music.'),
        ('finish doing sth.', '完成做某事', 'I finished writing the letter.'),
        ('mind doing sth.', '介意做某事', 'Would you mind closing the door?'),
        ('give up doing sth.', '放弃做某事', 'Never give up trying.'),
        ('can\'t help doing sth.', '忍不住做某事', 'I couldn\'t help laughing.'),
        ('be busy doing sth.', '忙于做某事', 'I am busy preparing for the exam.'),
        ('see/hear/watch sb. doing sth.', '看见/听见/观看某人正在做某事', 'I saw him running in the park.'),
        ('see/hear/watch sb. do sth.', '看见/听见/观看某人做了某事', 'I saw him enter the room.'),
        ('stop to do sth.', '停下来去做另一件事', 'He stopped to have a rest.'),
        ('stop doing sth.', '停止正在做的事', 'He stopped talking.'),
        ('forget/remember to do sth.', '忘记/记得要去做某事', 'Remember to lock the door.'),
        ('forget/remember doing sth.', '忘记/记得做过某事', 'I remember meeting him before.'),
        ('try to do sth.', '尽力做某事', 'I will try to finish it today.'),
        ('try doing sth.', '尝试做某事', 'Why not try using this method?'),
        ('mean to do sth.', '打算做某事', 'I mean to go there tomorrow.'),
        ('mean doing sth.', '意味着做某事', 'Missing the train means waiting for another hour.'),
        ('go on to do sth.', '继续做另一件事', 'After reading, he went on to write.'),
        ('go on doing sth.', '继续做同一件事', 'He went on working after lunch.'),
    ]
    
    added = 0
    for i, (pattern, explanation, example) in enumerate(new_patterns):
        chapter_id = chapter_ids[i % len(chapter_ids)] if chapter_ids else None
        try:
            cursor.execute('''
                INSERT INTO sentence_patterns (chapter_id, pattern, explanation, example)
                VALUES (?, ?, ?, ?)
            ''', (chapter_id, pattern, explanation, example))
            added += 1
        except:
            pass
    
    conn.commit()
    conn.close()
    print(f'新增句型: {added}个')

if __name__ == '__main__':
    add_patterns()

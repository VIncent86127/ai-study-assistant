#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 知识点数据库初始化脚本
创建SQLite数据库并填充初中二年级英语知识点
"""

import sqlite3
import os

# 数据库路径
DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'

def create_database():
    """创建数据库和表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建学科表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建年级表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        stage TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建章节表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        grade_id INTEGER NOT NULL,
        chapter_number INTEGER NOT NULL,
        chapter_name TEXT NOT NULL,
        semester TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (subject_id) REFERENCES subjects(id),
        FOREIGN KEY (grade_id) REFERENCES grades(id),
        UNIQUE(subject_id, grade_id, chapter_number, semester)
    )
    ''')
    
    # 创建知识点表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS knowledge_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        point_number TEXT NOT NULL,
        point_name TEXT NOT NULL,
        point_type TEXT,
        definition TEXT,
        key_points TEXT,
        examples TEXT,
        difficulty INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
    )
    ''')
    
    # 创建短语表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phrases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        english TEXT NOT NULL,
        chinese TEXT NOT NULL,
        example_sentence TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
    )
    ''')
    
    # 创建句型表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sentence_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        pattern TEXT NOT NULL,
        explanation TEXT,
        example TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
    )
    ''')
    
    # 创建语法点表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grammar_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        grammar_name TEXT NOT NULL,
        grammar_rule TEXT,
        usage_notes TEXT,
        examples TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id)
    )
    ''')
    
    conn.commit()
    print("数据库表结构创建成功！")
    return conn

def init_basic_data(conn):
    """初始化基础数据（学科、年级）"""
    cursor = conn.cursor()
    
    # 插入学科
    subjects = [
        ('英语', '文科', '初中英语课程'),
        ('数学', '理科', '初中数学课程'),
        ('语文', '文科', '初中语文课程'),
        ('物理', '理科', '初中物理课程（初二开始）'),
        ('化学', '理科', '初中化学课程（初三开始）'),
        ('生物', '理科', '初中生物课程'),
        ('历史', '文科', '初中历史课程'),
        ('地理', '文科', '初中地理课程'),
        ('政治', '文科', '初中政治课程')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO subjects (name, category, description) VALUES (?, ?, ?)', subjects)
    
    # 插入年级
    grades = [
        ('初一', '初中'),
        ('初二', '初中'),
        ('初三', '初中')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO grades (name, stage) VALUES (?, ?)', grades)
    
    conn.commit()
    print("基础数据初始化成功！")

def get_ids(conn):
    """获取学科和年级ID"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM subjects WHERE name = '英语'")
    subject_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM grades WHERE name = '初二'")
    grade_id = cursor.fetchone()[0]
    
    return subject_id, grade_id

def insert_grade8_english_data(conn):
    """插入八年级英语知识点数据"""
    cursor = conn.cursor()
    subject_id, grade_id = get_ids(conn)
    
    # 八年级上册单元数据
    units_up = [
        {
            'unit': 1,
            'name': 'Where did you go on vacation?',
            'phrases': [
                ('go on vacation', '去度假'),
                ('stay at home', '待在家里'),
                ('go to the mountains', '上山/进山'),
                ('go to the beach', '到海边去'),
                ('visit museums', '参观博物馆'),
                ('go to summer camp', '去夏令营'),
                ('quite a few', '相当多'),
                ('most of the time', '大部分时间'),
                ('taste good', '尝起来味道好'),
                ('have a good time', '玩得开心'),
                ('of course', '当然可以'),
                ('feel like', '感觉像……/想要'),
                ('go shopping', '去购物'),
                ('in the past', '在过去'),
                ('walk around', '绕……走'),
                ('too many', '太多(可数名词前面)'),
                ('because of', '因为'),
                ('one bowl of', '一碗……'),
                ('find out', '查出来/发现'),
                ('go on', '继续'),
                ('take photos', '照相'),
                ('something important', '重要的事情'),
                ('up and down', '上上下下'),
                ('come up', '出来')
            ],
            'patterns': [
                ('—Where did you go on vacation?\n—I went to New York City.', '你到哪里去度假了? 我去了纽约城。'),
                ('—Did you go out with anyone?\n—No, No one was here. Everyone was on vacation.', '你出去带人了吗? 不，没有人在这儿。大家都去度假了。'),
                ('—Did you buy anything special?\n—Yes, I bought something for my father.', '你买了什么特别的东西吗? 对，我给父亲买了一些东西。'),
                ('—How was the food?\n—Everything tasted really good.', '食物怎么样? 每一样东西真的都好吃。'),
                ('There was nothing much to do in the evening but read.', '晚上除了读书以外无事可做。')
            ],
            'grammar': [
                ('一般过去时', '表示过去某个时间发生的动作或存在的状态', '主语 + 动词过去式 + 其他', 'I went to the beach yesterday.\nShe visited her grandmother last week.')
            ]
        },
        {
            'unit': 2,
            'name': 'How often do you exercise?',
            'phrases': [
                ('help with housework', '帮助做家务'),
                ('hardly ever', '几乎不'),
                ('once a week', '一周一次'),
                ('twice a month', '一个月两次'),
                ('use the Internet', '使用互联网'),
                ('be free', '有空'),
                ('have dance and piano lessons', '上舞蹈和钢琴课'),
                ('swing dance', '摇摆舞'),
                ('play tennis', '打网球'),
                ('stay up late', '熬夜'),
                ('at least', '至少'),
                ('go to the dentist', '看牙医'),
                ('junk food', '垃圾食品'),
                ('be good for', '对……有益'),
                ('be bad for', '对……有害'),
                ('want sb. to do sth.', '想要某人做某事'),
                ('spend time with sb.', '和某人一起度过时光'),
                ('the answer to the question', '问题的答案'),
                ('the best way to do sth.', '做某事的最好方式')
            ],
            'patterns': [
                ('—How often do you exercise?\n—I exercise every day.', '你多久锻炼一次？我每天都锻炼。'),
                ('—What do you usually do on weekends?\n—I often go to the movies.', '你周末通常做什么？我经常去看电影。')
            ],
            'grammar': [
                ('频度副词', '表示动作发生的频率', 'always, usually, often, sometimes, hardly ever, never', 'I always get up early.\nShe sometimes watches TV.')
            ]
        }
    ]
    
    # 八年级下册单元数据
    units_down = [
        {
            'unit': 1,
            'name': "What's the matter?",
            'phrases': [
                ('have a fever', '发烧'),
                ('have a cough', '咳嗽'),
                ('have a toothache', '牙疼'),
                ('talk too much', '说得太多'),
                ('drink enough water', '喝足够的水'),
                ('have a cold', '受凉;感冒'),
                ('have a stomachache', '胃疼'),
                ('have a sore back', '背疼'),
                ('have a sore throat', '喉咙痛'),
                ('lie down and rest', '躺下来休息'),
                ('hot tea with honey', '加蜂蜜的热茶'),
                ('see a dentist', '看牙医'),
                ('get an X-ray', '拍X光片'),
                ('take one\'s temperature', '量体温'),
                ('put some medicine on sth.', '在…上面敷药'),
                ('sound like', '听起来像'),
                ('all weekend', '整个周末'),
                ('in the same way', '以同样的方式'),
                ('go to a doctor', '看医生'),
                ('thanks to', '多亏了;由于'),
                ('in time', '及时'),
                ('save a life', '挽救生命'),
                ('get into trouble', '造成麻烦'),
                ('right away', '立刻;马上'),
                ('hurt oneself', '受伤'),
                ('fall down', '摔倒'),
                ('have a nosebleed', '流鼻血'),
                ('have problems breathing', '呼吸困难')
            ],
            'patterns': [
                ("—What's the matter?\n—I have a stomachache.", '你怎么了? 我胃疼。'),
                ('You should lie down and rest.', '你应该躺下休息一会儿。'),
                ('You shouldn\'t go out at night.', '你晚上不应该出去。')
            ],
            'grammar': [
                ('情态动词should/shouldn\'t', '表示建议', '主语 + should/shouldn\'t + 动词原形', 'You should drink more water.\nYou shouldn\'t eat too much junk food.')
            ]
        },
        {
            'unit': 2,
            'name': "I'll help to clean up the city parks.",
            'phrases': [
                ('clean up', '打扫干净'),
                ('cheer up', '使变得更高兴;振作'),
                ('give out', '分发;散发'),
                ('come up with', '想出;提出'),
                ('put off', '推迟;延迟'),
                ('put up', '张贴;举起'),
                ('hand out', '分发'),
                ('call up', '打电话;召集'),
                ('used to', '曾经…;过去…'),
                ('care for', '关心;照顾'),
                ('try out', '试用;试行'),
                ('work for', '为…工作'),
                ('at the age of', '在……岁时'),
                ('take after', '与……相像'),
                ('fix up', '修理;修补'),
                ('give away', '赠送;捐赠'),
                ('be similar to', '与……相似'),
                ('set up', '建立;设立'),
                ('make a difference', '影响;有作用'),
                ('be able to', '能够')
            ],
            'patterns': [
                ('The boy could give out food at the food bank.', '这个男孩可以在食品救济站分发食物。'),
                ('He volunteers at an animal hospital every Saturday morning.', '每周六上午，他都在一家动物医院当志愿者。')
            ],
            'grammar': [
                ('动词不定式作宾语补足语', '动词 + 宾语 + to do', 'ask sb. to do sth.\ntell sb. to do sth.\nwant sb. to do sth.', 'My mother asked me to clean my room.\nThe teacher told us to study hard.')
            ]
        },
        {
            'unit': 3,
            'name': 'Could you please clean your room?',
            'phrases': [
                ('go out for dinner', '出去吃饭'),
                ('stay out late', '在外面待到很晚'),
                ('go to the movies', '去看电影'),
                ('get a ride', '搭车'),
                ('work on', '从事'),
                ('finish doing sth.', '完成做某事'),
                ('do the dishes', '洗餐具'),
                ('take out the rubbish', '倒垃圾'),
                ('fold the clothes', '叠衣服'),
                ('sweep the floor', '扫地'),
                ('make the bed', '整理床铺'),
                ('clean the living room', '打扫客厅'),
                ('no problem', '没问题'),
                ('come over', '过来'),
                ('all the time', '一直;总是'),
                ('do housework', '做家务'),
                ('share the housework', '分担家务'),
                ('in surprise', '惊讶地'),
                ('hang out', '闲逛'),
                ('pass sb. sth.', '把某物传给某人'),
                ('lend sb. sth.', '把某物借给某人'),
                ('hate to do sth.', '讨厌做某事'),
                ('do chores', '做杂务'),
                ('a waste of time', '浪费时间'),
                ('in order to', '为了'),
                ('depend on', '依赖;依靠'),
                ('take care of', '照顾;照看')
            ],
            'patterns': [
                ('—Could you please clean your room?\n—Yes, sure.', '你能整理一下你的房间吗? 当然可以。'),
                ('—Could I use your computer?\n—Sorry, I\'m going to work on it now.', '我可以用一下你的电脑吗? 抱歉,我现在要用它工作。')
            ],
            'grammar': [
                ('Could you please...?', '表示委婉请求', 'Could you please + 动词原形?', 'Could you please help me?\nCould you please open the window?'),
                ('Could I...?', '表示请求许可', 'Could I + 动词原形?', 'Could I use your phone?\nCould I borrow your book?')
            ]
        },
        {
            'unit': 4,
            'name': "Why don't you talk to your parents?",
            'phrases': [
                ('have free time', '有空闲时间'),
                ('allow sb. to do sth.', '允许某人做某事'),
                ('hang out with sb.', '与某人闲逛'),
                ('after-school classes', '课外活动课'),
                ('get into a fight with sb.', '与某人吵架/打架'),
                ('until midnight', '直到半夜'),
                ('talk to sb.', '与某人交谈'),
                ('too many', '太多'),
                ('get enough sleep', '有足够的睡眠'),
                ('write sb. a letter', '给某人写信'),
                ('call sb. up', '打电话给某人'),
                ('be angry with sb.', '生某人的气'),
                ('a big deal', '重要的事'),
                ('work out', '成功地发展;解决'),
                ('get on with', '与…和睦相处'),
                ('refuse to do sth.', '拒绝做某事'),
                ('offer to do sth.', '主动提出做某事'),
                ('mind sb. doing sth.', '介意某人做某事'),
                ('worry about sth.', '担心某事'),
                ('compete with sb.', '与某人竞争'),
                ('give sb. pressure', '给某人施压')
            ],
            'patterns': [
                ("—Why don't you forget about it?\n—That's a good idea.", '你为什么不忘掉它呢? 好主意。'),
                ('Although she\'s wrong, it\'s not a big deal.', '虽然她错了,但这并不是什么大事儿。')
            ],
            'grammar': [
                ('Why don\'t you...?', '表示建议', 'Why don\'t you + 动词原形? = Why not + 动词原形?', "Why don't you talk to your parents?\nWhy not go to the movies?"),
                ('so that', '以便;为了', 'so that + 从句', 'I study hard so that I can get good grades.')
            ]
        }
    ]
    
    # 插入上册数据
    for unit_data in units_up:
        cursor.execute('''
            INSERT INTO chapters (subject_id, grade_id, chapter_number, chapter_name, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject_id, grade_id, unit_data['unit'], unit_data['name'], '上册'))
        chapter_id = cursor.lastrowid
        
        # 插入短语
        for eng, chn in unit_data['phrases']:
            cursor.execute('''
                INSERT INTO phrases (chapter_id, english, chinese)
                VALUES (?, ?, ?)
            ''', (chapter_id, eng, chn))
        
        # 插入句型
        for pattern, explanation in unit_data['patterns']:
            cursor.execute('''
                INSERT INTO sentence_patterns (chapter_id, pattern, explanation)
                VALUES (?, ?, ?)
            ''', (chapter_id, pattern, explanation))
        
        # 插入语法
        for name, rule, usage, examples in unit_data['grammar']:
            cursor.execute('''
                INSERT INTO grammar_points (chapter_id, grammar_name, grammar_rule, usage_notes, examples)
                VALUES (?, ?, ?, ?, ?)
            ''', (chapter_id, name, rule, usage, examples))
    
    # 插入下册数据
    for unit_data in units_down:
        cursor.execute('''
            INSERT INTO chapters (subject_id, grade_id, chapter_number, chapter_name, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject_id, grade_id, unit_data['unit'], unit_data['name'], '下册'))
        chapter_id = cursor.lastrowid
        
        # 插入短语
        for eng, chn in unit_data['phrases']:
            cursor.execute('''
                INSERT INTO phrases (chapter_id, english, chinese)
                VALUES (?, ?, ?)
            ''', (chapter_id, eng, chn))
        
        # 插入句型
        for pattern, explanation in unit_data['patterns']:
            cursor.execute('''
                INSERT INTO sentence_patterns (chapter_id, pattern, explanation)
                VALUES (?, ?, ?)
            ''', (chapter_id, pattern, explanation))
        
        # 插入语法
        for name, rule, usage, examples in unit_data['grammar']:
            cursor.execute('''
                INSERT INTO grammar_points (chapter_id, grammar_name, grammar_rule, usage_notes, examples)
                VALUES (?, ?, ?, ?, ?)
            ''', (chapter_id, name, rule, usage, examples))
    
    conn.commit()
    print("八年级英语知识点数据插入成功！")

def main():
    """主函数"""
    # 确保目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 创建数据库
    conn = create_database()
    
    # 初始化基础数据
    init_basic_data(conn)
    
    # 插入八年级英语数据
    insert_grade8_english_data(conn)
    
    # 查询统计
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM chapters")
    chapter_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phrases")
    phrase_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM sentence_patterns")
    pattern_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM grammar_points")
    grammar_count = cursor.fetchone()[0]
    
    print(f"\n数据库统计:")
    print(f"- 章节/单元: {chapter_count} 个")
    print(f"- 短语: {phrase_count} 条")
    print(f"- 句型: {pattern_count} 条")
    print(f"- 语法点: {grammar_count} 个")
    
    conn.close()
    print(f"\n数据库已创建: {DB_PATH}")

if __name__ == '__main__':
    main()

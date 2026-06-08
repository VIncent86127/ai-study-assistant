#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充初中数学易错点和常见题型
"""

import sqlite3

def get_db():
    return sqlite3.connect('knowledge.db')

def get_chapter_id(grade, semester, chapter_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM math_chapters 
        WHERE grade = ? AND semester = ? AND chapter_name = ?
    ''', (grade, semester, chapter_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_mistake(chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_common_mistakes (chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples))
        conn.commit()
    except:
        pass
    finally:
        conn.close()

def add_question_type(chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_question_types 
            (chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples))
        conn.commit()
    except:
        pass
    finally:
        conn.close()

def add_method(chapter_id, name, description, steps, applicable_types, examples, tips=None):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_methods (chapter_id, method_name, description, steps, applicable_types, examples, tips)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, name, description, steps, applicable_types, examples, tips))
        conn.commit()
    except:
        pass
    finally:
        conn.close()

def input_all_mistakes_and_types():
    """录入易错点和常见题型"""
    
    # ===== 有理数 =====
    chapter_id = get_chapter_id('七年级', '上册', '有理数')
    mistakes = [
        ('绝对值计算', '概念错误', '认为|a|=a', '正数绝对值是其本身，负数绝对值是其相反数', '|-3|=3，不是|-3|=-3', '例：求|-5|的值'),
        ('有理数大小比较', '方法错误', '认为绝对值大的数就大', '两个负数比较，绝对值大的反而小', '-3 > -5，因为|-3| < |-5|', '例：比较-3和-5的大小'),
        ('有理数乘方', '符号错误', '混淆(-a)²和-a²', '(-a)²是a的平方的相反数的平方，-a²是a的平方的相反数', '(-2)²=4，-2²=-4', '例：计算(-3)²和-3²'),
        ('有理数混合运算', '运算顺序', '运算顺序错误', '先乘方，再乘除，后加减，有括号先算括号', '-3²+4×(-2)= -9+(-8)=-17', '例：计算-3²+4×(-2)'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    question_types = [
        ('有理数分类', '判断一个数属于哪类有理数', '先看是否为整数，再看是否为分数', 1, '常考', '判断√2是否为有理数'),
        ('有理数运算', '加减乘除乘方运算', '按照运算顺序，注意符号', 2, '必考', '计算(-2)³+3×(-4)'),
        ('科学记数法', '将大数表示为科学记数法', '确定a和n的值', 2, '常考', '将3.6亿用科学记数法表示'),
    ]
    for q in question_types:
        add_question_type(chapter_id, *q)
    
    # ===== 整式的加减 =====
    chapter_id = get_chapter_id('七年级', '上册', '整式的加减')
    mistakes = [
        ('同类项判断', '概念错误', '只看字母相同', '必须字母相同且相同字母指数相同', '3x²和3x不是同类项', '例：判断3x²y和3xy²是否为同类项'),
        ('去括号', '符号错误', '括号前是负号时漏变号', '括号前是负号，括号内各项都要变号', '-(2x-3)=-2x+3', '例：化简-(2x-3y+1)'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 一元一次方程 =====
    chapter_id = get_chapter_id('七年级', '上册', '一元一次方程')
    mistakes = [
        ('去分母', '运算错误', '漏乘常数项', '去分母时，每一项都要乘', '(x+1)/2-1=3 → x+1-2=6（正确）', '例：解方程(x+1)/2-1=3'),
        ('移项', '符号错误', '移项不变号', '移项必须变号', '2x+3=7 → 2x=7-3（正确）', '例：解方程3x+5=2x-3'),
        ('方程的解检验', '遗漏步骤', '忘记检验', '代入检验是解题的必要步骤', '将x=2代入原方程检验', '例：解方程并检验'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    methods = [
        ('列一元一次方程解应用题', '用方程解决实际问题',
         '①审题，找等量关系\n②设未知数\n③列方程\n④解方程\n⑤检验作答',
         '应用题', '小明买5本书花了25元，每本书多少元？设每本书x元，则5x=25', '审题是关键'),
    ]
    for m in methods:
        add_method(chapter_id, *m)
    
    # ===== 二元一次方程组 =====
    chapter_id = get_chapter_id('七年级', '下册', '二元一次方程组')
    mistakes = [
        ('代入消元', '变形错误', '代入时表达式写错', '从一个方程变形后代入另一个方程', '由x+y=5得x=5-y，代入x-y=1', '例：解方程组'),
        ('加减消元', '系数错误', '系数化相同或相反时出错', '确保消去的未知数系数相同或相反', '2x+3y=7与4x-3y=5相加得6x=12', '例：解方程组'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 不等式 =====
    chapter_id = get_chapter_id('七年级', '下册', '不等式与不等式组')
    mistakes = [
        ('不等式性质', '方向错误', '乘除负数不等号不变向', '乘除负数时不等号方向必须改变', '-2x<6 → x>-3（正确）', '例：解不等式-2x<6'),
        ('解集表示', '表示错误', '数轴表示时端点画错', '有等号用实心点，无等号用空心点', 'x≥2用实心点，x>2用空心点', '例：在数轴上表示解集'),
        ('不等式组解集', '取值错误', '公共部分找错', '取各不等式解集的公共部分', '{x>2, x<5的解集是2<x<5', '例：解不等式组'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 全等三角形 =====
    chapter_id = get_chapter_id('八年级', '上册', '全等三角形')
    mistakes = [
        ('全等判定', '条件不足', '只有AAA或SSA不能判定全等', 'SSS、SAS、ASA、AAS、HL（直角三角形）', '只有AAA不能判定全等', '例：判断能否判定全等'),
        ('对应关系', '对应错误', '对应边、对应角找错', '书写全等时对应点要写在对应对位置', '△ABC≌△DEF，A对应D，B对应E', '例：写出全等关系'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    methods = [
        ('全等三角形证明', '证明两个三角形全等',
         '①找已知条件\n②确定判定方法\n③写出证明过程',
         '全等证明', '已知AB=CD，∠A=∠D，用AAS证明', '找准对应关系'),
    ]
    for m in methods:
        add_method(chapter_id, *m)
    
    # ===== 整式乘除与因式分解 =====
    chapter_id = get_chapter_id('八年级', '上册', '整式的乘除与因式分解')
    mistakes = [
        ('幂的运算', '法则混淆', '指数运算法则混淆', '同底数幂相乘：指数相加\n幂的乘方：指数相乘\n积的乘方：分别乘方', 'x²·x³=x⁵，不是x⁶', '例：计算x²·x³'),
        ('完全平方公式', '漏项', '忘记中间的2ab项', '(a±b)²=a²±2ab+b²', '(x+3)²=x²+6x+9，不是x²+9', '例：计算(x+3)²'),
        ('因式分解', '不彻底', '分解不彻底', '分解到不能再分为止', 'x⁴-16=(x²+4)(x+2)(x-2)', '例：因式分解x⁴-16'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 分式 =====
    chapter_id = get_chapter_id('八年级', '上册', '分式')
    mistakes = [
        ('分式有意义', '条件遗漏', '忘记分母不为0', '分母不为0时分式有意义', 'x/(x-2)有意义：x≠2', '例：求x取值范围'),
        ('分式值为0', '条件错误', '只考虑分子为0', '分子为0且分母不为0', 'x/(x-2)=0：x=0且x≠2', '例：求分式值为0的条件'),
        ('分式运算', '符号错误', '约分或通分时符号错误', '注意分数线相当于括号', '(x-y)/(y-x) = -1', '例：化简分式'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 二次根式 =====
    chapter_id = get_chapter_id('八年级', '下册', '二次根式')
    mistakes = [
        ('二次根式化简', '化简不彻底', '被开方数还有能开出的因数', '化简到最简二次根式', '√8=2√2，不是√8', '例：化简√18'),
        ('二次根式运算', '合并错误', '不是同类二次根式不能合并', '被开方数相同才能合并', '√2+√3不能合并', '例：计算√2+√8'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 平行四边形 =====
    chapter_id = get_chapter_id('八年级', '下册', '平行四边形')
    mistakes = [
        ('判定条件', '条件混淆', '平行四边形、矩形、菱形判定混淆', '区分各种四边形的判定定理', '矩形对角线相等，菱形对角线垂直', '例：判断四边形类型'),
        ('性质应用', '遗漏条件', '忘记使用性质条件', '先判断四边形类型，再用性质', '矩形四个角都是直角', '例：求矩形角度'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 一次函数 =====
    chapter_id = get_chapter_id('八年级', '下册', '一次函数')
    mistakes = [
        ('k、b符号判断', '判断错误', 'k、b符号与图象位置关系', 'k>0向上，k<0向下；b>0交于正半轴，b<0交于负半轴', 'y=-2x+3：k<0，b>0', '例：根据图象判断k、b符号'),
        ('函数图象', '画图错误', '列表取点错误', '选合适的点连线', '一次函数是直线，取两点即可', '例：画出y=2x+1的图象'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    methods = [
        ('一次函数应用题', '用一次函数解决实际问题',
         '①设函数表达式\n②根据条件求k、b\n③用函数解决问题',
         '函数应用', '路程s=vt+10中，v=60，t=2时s=130', '注意单位'),
    ]
    for m in methods:
        add_method(chapter_id, *m)
    
    # ===== 一元二次方程 =====
    chapter_id = get_chapter_id('九年级', '上册', '一元二次方程')
    mistakes = [
        ('判别式计算', '计算错误', 'Δ计算错误', 'Δ=b²-4ac', 'x²+2x+3=0，Δ=4-12=-8<0', '例：计算判别式'),
        ('公式法', '代入错误', '系数代入公式错误', 'x=(-b±√Δ)/(2a)', '注意符号', '例：用公式法解方程'),
        ('韦达定理', '条件遗漏', '忘记Δ≥0的前提', '只有方程有实根时才可用韦达定理', '根不存在时不能用韦达定理', '例：已知根求参数'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 二次函数 =====
    chapter_id = get_chapter_id('九年级', '上册', '二次函数')
    mistakes = [
        ('开口方向', '判断错误', 'a的符号决定开口方向', 'a>0向上，a<0向下', 'y=-x²向下开口', '例：判断开口方向'),
        ('顶点坐标', '公式记忆', '顶点坐标公式记错', '顶点(-b/(2a), (4ac-b²)/(4a))', '配方求顶点更可靠', '例：求顶点坐标'),
        ('最值问题', '条件遗漏', '不考虑定义域', '注意自变量取值范围', '实际问题中要考虑实际意义', '例：求最大利润'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    methods = [
        ('二次函数求最值', '求二次函数的最大值或最小值',
         '①确定a的符号\n②求顶点坐标\n③考虑定义域',
         '最值问题', 'y=-x²+4x+1，a=-1<0，最大值在顶点', '注意定义域'),
    ]
    for m in methods:
        add_method(chapter_id, *m)
    
    # ===== 圆 =====
    chapter_id = get_chapter_id('九年级', '上册', '圆')
    mistakes = [
        ('圆周角定理', '应用错误', '忽略圆心角和圆周角的关系', '同弧所对圆周角是圆心角的一半', '圆心角80°，圆周角40°', '例：求圆周角'),
        ('切线判定', '条件不足', '缺少垂直条件', '必须经过半径外端且垂直于半径', '连接圆心与切点，得垂直关系', '例：证明切线'),
        ('弧长和面积', '公式错误', '公式混淆', '弧长l=nπR/180，面积S=nπR²/360', '注意单位统一', '例：求弧长'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 概率 =====
    chapter_id = get_chapter_id('九年级', '上册', '概率初步')
    mistakes = [
        ('列举法', '遗漏情况', '列举不完整', '列表法或树状图法确保完整', '列表时注意所有可能性', '例：求概率'),
        ('概率计算', '计算错误', '事件数量计算错误', '正确计数是关键', '概率=所求事件数/总事件数', '例：求中奖概率'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 相似 =====
    chapter_id = get_chapter_id('九年级', '下册', '相似')
    mistakes = [
        ('相似比', '顺序错误', '对应顺序弄反', '相似比有顺序', '△ABC∽△DEF，相似比是AB/DE', '例：求相似比'),
        ('面积比', '关系错误', '面积比等于相似比的平方', '面积比=相似比²', '相似比2:3，面积比4:9', '例：求面积比'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    # ===== 锐角三角函数 =====
    chapter_id = get_chapter_id('九年级', '下册', '锐角三角函数')
    mistakes = [
        ('三角函数值', '记忆错误', '特殊角的三角函数值记错', '熟记30°、45°、60°的三角函数值', 'sin30°=1/2, cos60°=1/2, tan45°=1', '例：求三角函数值'),
        ('解直角三角形', '条件不足', '已知条件不够', '至少知道一边一角或两边', '利用三角函数关系求解', '例：解直角三角形'),
    ]
    for m in mistakes:
        add_mistake(chapter_id, *m)
    
    methods = [
        ('解直角三角形应用', '利用三角函数解决实际问题',
         '①画示意图\n②标出已知量和未知量\n③选择合适的三角函数\n④计算求解',
         '应用题', '测量山高：tan30°=高/距离', '注意角度和边对应'),
    ]
    for m in methods:
        add_method(chapter_id, *m)
    
    # 统计
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM math_common_mistakes')
    mistakes_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM math_question_types')
    types_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM math_methods')
    methods_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n补充完成！")
    print(f"  易错点：{mistakes_count}条")
    print(f"  常见题型：{types_count}条")
    print(f"  解题方法：{methods_count}条")

if __name__ == '__main__':
    input_all_mistakes_and_types()

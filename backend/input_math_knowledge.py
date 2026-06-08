#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入初中数学全部知识点数据
"""

import sqlite3

def get_db():
    return sqlite3.connect('knowledge.db')

def get_chapter_id(grade, semester, chapter_name):
    """获取章节ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM math_chapters 
        WHERE grade = ? AND semester = ? AND chapter_name = ?
    ''', (grade, semester, chapter_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_concept(chapter_id, name, concept_type, definition, formula=None, properties=None, examples=None, difficulty=1, keywords=None):
    """添加概念"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_concepts 
            (chapter_id, concept_name, concept_type, definition, formula, properties, examples, difficulty, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, name, concept_type, definition, formula, properties, examples, difficulty, keywords))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"添加概念失败: {name}, {e}")
        return None
    finally:
        conn.close()

def add_theorem(chapter_id, name, content, proof=None, application=None, examples=None, difficulty=1):
    """添加定理"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_theorems 
            (chapter_id, theorem_name, content, proof, application, examples, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, name, content, proof, application, examples, difficulty))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"添加定理失败: {name}, {e}")
        return None
    finally:
        conn.close()

def add_method(chapter_id, name, description, steps, applicable_types, examples, tips=None):
    """添加方法"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_methods 
            (chapter_id, method_name, description, steps, applicable_types, examples, tips)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, name, description, steps, applicable_types, examples, tips))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"添加方法失败: {name}, {e}")
        return None
    finally:
        conn.close()

def add_mistake(chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples):
    """添加易错点"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_common_mistakes 
            (chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, topic, mistake_type, wrong_approach, correct_approach, reason, examples))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def add_question_type(chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples):
    """添加题型"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO math_question_types 
            (chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chapter_id, type_name, description, solution_strategy, difficulty_level, exam_frequency, examples))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

# ==================== 七年级上册 ====================

def input_grade7_up_chapter1():
    """七年级上册 第一章：有理数"""
    chapter_id = get_chapter_id('七年级', '上册', '有理数')
    
    # 概念
    concepts = [
        ('正数和负数', '概念', 
         '大于0的数叫做正数；在正数前面加上负号"-"的数叫做负数；0既不是正数也不是负数。',
         None, '正数：+1, +2.5, +3/4\n负数：-1, -2.5, -3/4\n注意：+号可省略，-号不可省略',
         '如果向北走10米记作+10米，那么向南走10米记作-10米。',
         1, '正数 负数 相反意义'),
        
        ('有理数', '概念',
         '整数和分数统称为有理数。',
         '有理数 = 整数 + 分数',
         '分类：\n①按定义分：正整数、0、负整数、正分数、负分数\n②按正负分：正有理数、0、负有理数',
         '下列数中，哪些是有理数：-3, 0, 1/2, √2, -0.5',
         1, '有理数 整数 分数'),
        
        ('数轴', '概念',
         '用一条直线上的点表示数，这条直线叫做数轴。',
         None,
         '数轴三要素：原点、正方向、单位长度',
         '画出数轴，并在数轴上表示-3, -1.5, 0, 2, 3.5',
         2, '数轴 原点 正方向 单位长度'),
        
        ('相反数', '概念',
         '只有符号不同的两个数叫做互为相反数。',
         'a的相反数是-a',
         '①互为相反数的两个数位于原点两侧，到原点距离相等\n②0的相反数是0\n③相反数的和为0',
         '-3的相反数是3；3的相反数是-3；0的相反数是0',
         1, '相反数 符号'),
        
        ('绝对值', '概念',
         '一个数在数轴上对应的点到原点的距离叫做这个数的绝对值。',
         '|a| = {a (a≥0); -a (a<0)}',
         '①正数的绝对值是它本身\n②负数的绝对值是它的相反数\n③0的绝对值是0\n④|a|≥0',
         '|-3| = 3; |3| = 3; |0| = 0',
         2, '绝对值 距离 非负'),
        
        ('有理数的大小比较', '概念',
         '在数轴上，右边的数总比左边的数大。',
         None,
         '①正数大于0，负数小于0，正数大于负数\n②两个负数比较，绝对值大的反而小',
         '比较-3和-5的大小：|-3|=3, |-5|=5, 因为3<5，所以-3>-5',
         2, '大小比较 数轴'),
        
        ('有理数的加法', '运算法则',
         '同号两数相加，取相同的符号，并把绝对值相加；异号两数相加，取绝对值较大的符号，并用较大的绝对值减去较小的绝对值。',
         '加法法则：\n同号：符号不变，绝对值相加\n异号：取大符号，大减小\n互为相反数相加得0',
         '①加法交换律：a+b=b+a\n②加法结合律：(a+b)+c=a+(b+c)',
         '(-3)+(-5) = -8\n(-3)+(+5) = +2',
         2, '加法 符号'),
        
        ('有理数的减法', '运算法则',
         '减去一个数，等于加上这个数的相反数。',
         'a - b = a + (-b)',
         None,
         '(-3) - 5 = (-3) + (-5) = -8\n(-3) - (-5) = (-3) + (+5) = 2',
         2, '减法 相反数'),
        
        ('有理数的乘法', '运算法则',
         '两数相乘，同号得正，异号得负，并把绝对值相乘。',
         '符号法则：同号得正，异号得负',
         '①任何数与0相乘，都得0\n②乘法交换律：ab=ba\n③乘法结合律：(ab)c=a(bc)\n④乘法分配律：a(b+c)=ab+ac',
         '(-3)×(-5) = 15\n(-3)×5 = -15',
         2, '乘法 符号'),
        
        ('有理数的除法', '运算法则',
         '除以一个不为0的数，等于乘以这个数的倒数。',
         'a÷b = a×(1/b) (b≠0)',
         '①两数相除，同号得正，异号得负，并把绝对值相除\n②0除以任何不为0的数都得0\n③0不能做除数',
         '(-15)÷(-3) = 5\n(-15)÷3 = -5',
         2, '除法 倒数'),
        
        ('有理数的乘方', '概念',
         '求n个相同因数的积的运算叫做乘方，乘方的结果叫做幂。',
         'a^n = a×a×...×a (n个a相乘)',
         '①正数的任何次幂都是正数\n②负数的奇数次幂是负数，偶数次幂是正数\n③0的任何正整数次幂都是0',
         '(-2)^3 = -8; (-2)^4 = 16; 2^3 = 8',
         2, '乘方 幂 指数 底数'),
        
        ('科学记数法', '概念',
         '把一个大于10的数表示成a×10^n的形式，其中1≤a<10，n是正整数。',
         'N = a×10^n (1≤a<10)',
         'n等于原数的整数位数减1',
         '光速约为3×10^8米/秒\n地球半径约为6.4×10^6米',
         2, '科学记数法'),
        
        ('近似数', '概念',
         '接近准确数而不等于准确数的数叫做近似数。',
         None,
         '精确度：精确到哪一位就说近似数精确到哪一位',
         'π≈3.14（精确到百分位）\nπ≈3.1416（精确到万分位）',
         2, '近似数 精确度'),
    ]
    
    for c in concepts:
        add_concept(chapter_id, *c)
    
    # 定理/法则
    theorems = [
        ('有理数加法法则', 
         '同号两数相加，取相同的符号，并把绝对值相加；异号两数相加，取绝对值较大的符号，并用较大的绝对值减去较小的绝对数；互为相反数的两数相加得0。',
         None, '适用于有理数加法运算',
         '①(+3)+(+5)=+8  ②(-3)+(-5)=-8  ③(+3)+(-5)=-2',
         2),
        
        ('有理数乘法法则',
         '两数相乘，同号得正，异号得负，并把绝对值相乘。任何数与0相乘，都得0。',
         None, '适用于有理数乘法运算',
         '①(-2)×(-3)=+6  ②(-2)×(+3)=-6  ③(-2)×0=0',
         2),
    ]
    
    for t in theorems:
        add_theorem(chapter_id, *t)
    
    # 方法
    methods = [
        ('有理数混合运算', 
         '有理数的加减乘除乘方混合运算',
         '①先算乘方\n②再算乘除\n③最后算加减\n④如果有括号，先算括号里面的',
         '有理数混合运算',
         '(-2)^3 + (-3)×(-4) - (-5) = -8 + 12 - (-5) = 4 + 5 = 9',
         '注意运算顺序，符号不要搞错'),
        
        ('判断有理数类型',
         '判断一个数属于哪种类型的有理数',
         '①看是否为整数（正整数、0、负整数）\n②看是否为分数（正分数、负分数）\n③整数和分数统称有理数',
         '有理数分类',
         '判断√2是否为有理数：不是，因为不能表示为分数形式',
         None),
    ]
    
    for m in methods:
        add_method(chapter_id, *m)
    
    # 易错点
    mistakes = [
        ('相反数的理解', '概念混淆',
         '认为相反数就是负数',
         '相反数是指符号相反的两个数，正数也有相反数',
         '3的相反数是-3，正数也有相反数',
         '例：判断"正数没有相反数"是否正确'),
        
        ('绝对值的理解', '计算错误',
         '直接去掉符号',
         '负数的绝对值等于它的相反数',
         '|-3| = 3，不是 |-3| = -3',
         '例：求|-5|的值'),
        
        ('有理数加减运算', '符号错误',
         '忽略负号或符号运算错误',
         '按照运算法则，注意同号异号的处理',
         '(-3)+(-5) = -8，不是2',
         '例：计算(-3)+(-5)'),
        
        ('有理数乘方', '符号错误',
         '(-2)^2 与 -2^2 混淆',
         '(-2)^2 = 4，-2^2 = -4',
         '(-2)^2 = (-2)×(-2) = 4\n-2^2 = -(2^2) = -4',
         '例：计算(-3)^2 和 -3^2'),
    ]
    
    for mk in mistakes:
        add_mistake(chapter_id, *mk)
    
    print("第一章：有理数 - 录入完成")

def input_grade7_up_chapter2():
    """七年级上册 第二章：整式的加减"""
    chapter_id = get_chapter_id('七年级', '上册', '整式的加减')
    
    concepts = [
        ('用字母表示数', '概念',
         '用字母表示数可以把数和数量关系一般化地、简明地表示出来。',
         None, None,
         '如果用n表示一个数，那么它的2倍可以表示为2n',
         1, '字母表示数 代数式'),
        
        ('代数式', '概念',
         '用运算符号把数和字母连接而成的式子叫做代数式。单独一个数或一个字母也是代数式。',
         None,
         '运算符号包括：加、减、乘、除、乘方、开方',
         '2a, 3x+1, a², πr², x/y',
         1, '代数式'),
        
        ('单项式', '概念',
         '由数或字母的积组成的代数式叫做单项式。单独一个数或一个字母也是单项式。',
         None,
         '单项式的系数：单项式中的数字因数\n单项式的次数：所有字母的指数的和',
         '3x²y的系数是3，次数是3',
         2, '单项式 系数 次数'),
        
        ('多项式', '概念',
         '几个单项式的和叫做多项式。',
         None,
         '多项式的项：组成多项式的每个单项式\n常数项：不含字母的项\n多项式的次数：最高次项的次数',
         '3x²+2x-1是二次三项式，常数项是-1',
         2, '多项式 项 常数项'),
        
        ('整式', '概念',
         '单项式与多项式统称为整式。',
         '整式 = 单项式 + 多项式',
         None,
         '2x, x²+1, 3x-y都是整式',
         1, '整式'),
        
        ('同类项', '概念',
         '所含字母相同，并且相同字母的指数也相同的项叫做同类项。常数项也是同类项。',
         None,
         '判断同类项的两个条件：①所含字母相同 ②相同字母的指数相同',
         '3x²y和-2x²y是同类项',
         2, '同类项'),
        
        ('合并同类项', '运算法则',
         '把多项式中的同类项合并成一项，叫做合并同类项。',
         '合并同类项：系数相加，字母和指数不变',
         '合并同类项后，所得项的系数是合并前各同类项的系数的和，字母部分不变',
         '3x²+2x²-5x² = (3+2-5)x² = 0x² = 0',
         2, '合并同类项'),
        
        ('去括号法则', '运算法则',
         '括号前面是"+"号，把括号和它前面的"+"号去掉，括号里各项都不改变符号；括号前面是"-"号，把括号和它前面的"-"号去掉，括号里各项都改变符号。',
         '去括号：+不变，-全变',
         None,
         '+(a+b) = a+b\n-(a+b) = -a-b',
         2, '去括号'),
        
        ('添括号法则', '运算法则',
         '添括号后，括号前面是"+"号，括到括号里的各项都不改变符号；添括号后，括号前面是"-"号，括到括号里的各项都改变符号。',
         '添括号：+不变，-全变',
         None,
         'a+b+c = a+(b+c)\na-b-c = a-(b+c)',
         2, '添括号'),
    ]
    
    for c in concepts:
        add_concept(chapter_id, *c)
    
    methods = [
        ('整式加减运算',
         '整式的加减运算',
         '①去括号\n②合并同类项',
         '整式加减',
         '(3x²-2x+1)+(2x²+3x-5)\n= 3x²-2x+1+2x²+3x-5\n= 5x²+x-4',
         '注意去括号时的符号变化'),
    ]
    
    for m in methods:
        add_method(chapter_id, *m)
    
    mistakes = [
        ('同类项判断', '概念错误',
         '只看字母相同，忽略指数',
         '必须同时满足：字母相同，指数相同',
         '3x²和3x不是同类项',
         '例：判断3x²和3x是否为同类项'),
        
        ('去括号符号', '计算错误',
         '括号前是负号时，只变第一项符号',
         '括号前是负号，括号内各项都要变号',
         '-(a-b+c) = -a+b-c',
         '例：化简-(2x-3y+1)'),
    ]
    
    for mk in mistakes:
        add_mistake(chapter_id, *mk)
    
    print("第二章：整式的加减 - 录入完成")

def input_grade7_up_chapter3():
    """七年级上册 第三章：一元一次方程"""
    chapter_id = get_chapter_id('七年级', '上册', '一元一次方程')
    
    concepts = [
        ('方程', '概念',
         '含有未知数的等式叫做方程。',
         None,
         '方程必须具备两个条件：①含有未知数 ②是等式',
         '2x+3=7是方程，但2x+3不是方程',
         1, '方程 未知数 等式'),
        
        ('一元一次方程', '概念',
         '只含有一个未知数，未知数的次数都是1，等号两边都是整式的方程叫做一元一次方程。',
         '标准形式：ax+b=0 (a≠0)',
         '一元一次方程的特点：①一个未知数 ②次数是1 ③整式方程',
         '2x+3=7, 3y-1=0都是一元一次方程',
         1, '一元一次方程'),
        
        ('方程的解', '概念',
         '使方程左右两边相等的未知数的值叫做方程的解。',
         None,
         '检验方程解的方法：代入未知数的值，看方程左右两边是否相等',
         'x=2是方程2x+3=7的解，因为当x=2时，左边=2×2+3=7=右边',
         2, '方程的解'),
        
        ('等式的性质', '性质',
         '等式两边加（或减）同一个数（或式子），结果仍相等；等式两边乘同一个数，或除以同一个不为0的数，结果仍相等。',
         '性质1：如果a=b，那么a+c=b+c\n性质2：如果a=b，那么ac=bc，a÷c=b÷c(c≠0)',
         None,
         '如果x+3=5，那么x+3-3=5-3，即x=2',
         2, '等式的性质'),
        
        ('移项', '运算法则',
         '把等式一边的某项变号后移到另一边，叫做移项。',
         '移项变号',
         '移项的依据是等式的性质1',
         '2x+3=7，移项得2x=7-3',
         2, '移项'),
        
        ('解一元一次方程', '方法',
         '求方程的解的过程叫做解方程。',
         None,
         '一般步骤：①去分母 ②去括号 ③移项 ④合并同类项 ⑤系数化为1',
         '解方程：2x+3=7\n移项：2x=7-3\n合并：2x=4\n系数化为1：x=2',
         2, '解方程'),
    ]
    
    for c in concepts:
        add_concept(chapter_id, *c)
    
    methods = [
        ('解一元一次方程',
         '求解一元一次方程',
         '①去分母（方程两边同乘各分母的最小公倍数）\n②去括号\n③移项（含未知数的移到一边，常数项移到另一边）\n④合并同类项\n⑤系数化为1',
         '一元一次方程',
         '解方程：(x-1)/2 - (2x+1)/3 = 1\n去分母：3(x-1)-2(2x+1)=6\n去括号：3x-3-4x-2=6\n移项：3x-4x=6+3+2\n合并：-x=11\n系数化为1：x=-11',
         '注意去分母时不要漏乘常数项'),
    ]
    
    for m in methods:
        add_method(chapter_id, *m)
    
    mistakes = [
        ('去分母', '计算错误',
         '去分母时忘记乘常数项',
         '去分母时，方程两边每一项都要乘',
         '(x+1)/2 = 3\n去分母：x+1=6（正确）\n不要写成：(x+1)=6',
         '例：解方程(x+1)/2 - 1 = 2'),
        
        ('移项', '符号错误',
         '移项时忘记变号',
         '移项必须变号',
         '2x+3=7，移项得2x=7-3（正确）\n不能写成2x=7+3（错误）',
         '例：解方程3x+5=2x-3'),
    ]
    
    for mk in mistakes:
        add_mistake(chapter_id, *mk)
    
    print("第三章：一元一次方程 - 录入完成")

# 继续添加其他章节...

def input_all_chapters():
    """录入所有章节"""
    input_grade7_up_chapter1()
    input_grade7_up_chapter2()
    input_grade7_up_chapter3()
    # 更多章节将在后续添加

if __name__ == '__main__':
    input_all_chapters()

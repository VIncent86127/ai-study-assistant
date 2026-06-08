#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习助手 - 八年级英语完整知识点数据录入
人教版八年级上册 Unit 1-10 + 下册 Unit 1-10
"""

import sqlite3

DB_PATH = '/home/ubuntu/.openclaw/workspace/ai-study-assistant/backend/knowledge.db'

# 八年级上册完整数据 (Unit 1-10)
GRADE8_UP_DATA = [
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
            ('study for', '为……学习'),
            ('go out', '出去'),
            ('most of the time', '大部分时间/绝大多数时间'),
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
            ('come up', '出来'),
        ],
        'patterns': [
            ('—Where did you go on vacation?\n—I went to New York City.', '你到哪里去度假了? 我去了纽约城。'),
            ('—Did you go out with anyone?\n—No, No one was here. Everyone was on vacation.', '你出去带人了吗? 不，没有人在这儿。大家都去度假了。'),
            ('—Did you buy anything special?\n—Yes, I bought something for my father.', '你买了什么特别的东西吗? 对，我给父亲买了一些东西。'),
            ('—How was the food?\n—Everything tasted really good.', '食物怎么样? 每一样东西真的都好吃。'),
            ('There was nothing much to do in the evening but read.', '晚上除了读书以外无事可做。'),
        ],
        'grammar': [
            ('一般过去时', '表示过去某个时间发生的动作或存在的状态', '主语 + 动词过去式 + 其他', 'I went to the beach yesterday.\nShe visited her grandmother last week.'),
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
            ('the best way to do sth.', '做某事的最好方式'),
        ],
        'patterns': [
            ('—How often do you exercise?\n—I exercise every day.', '你多久锻炼一次？我每天都锻炼。'),
            ('—What do you usually do on weekends?\n—I often go to the movies.', '你周末通常做什么？我经常去看电影。'),
        ],
        'grammar': [
            ('频度副词', '表示动作发生的频率', 'always, usually, often, sometimes, hardly ever, never', 'I always get up early.\nShe sometimes watches TV.'),
        ]
    },
    {
        'unit': 3,
        'name': "I'm more outgoing than my sister.",
        'phrases': [
            ('more outgoing', '更外向'),
            ('as...as...', '和……一样……'),
            ('the same as', '和……相同'),
            ('be different from', '与……不同'),
            ('care about', '关心；在意'),
            ('be like a mirror', '像一面镜子'),
            ('the most important', '最重要的'),
            ('be similar to', '与……相像的/类似的'),
            ('be good at', '擅长……'),
            ('be good with', '善于应付……的'),
            ('call sb. at', '拨打……（号码）找某人'),
            ('have fun', '玩得开心'),
            ('make friends', '交朋友'),
            ('be talented in', '在……有天赋'),
            ('be good for', '对……有好处'),
            ('primary school', '小学'),
            ('in fact', '事实上；实际上'),
        ],
        'patterns': [
            ('Tom is taller than Sam.', 'Tom比Sam更高。'),
            ('Tina is more outgoing than Tara.', 'Tina比Tara更外向。'),
            ('I am as friendly as my sister.', '我和我姐姐一样友好。'),
            ('A good friend truly cares about me.', '一个好朋友真正关心我。'),
        ],
        'grammar': [
            ('形容词比较级', '表示两者之间的比较', '主语 + be动词 + 形容词比较级 + than + 比较对象', 'Lucy is taller than Lily.\nThis book is more interesting than that one.'),
        ]
    },
    {
        'unit': 4,
        'name': "What's the best movie theater?",
        'phrases': [
            ('so far', '到目前为止，迄今为止'),
            ('no problem', '没什么，别客气'),
            ('have...in common', '有相同特征(想法、兴趣等方面)相同'),
            ('be up to', '由……决定/是……的职责'),
            ('all kinds of', '各种各样的……'),
            ('play a role in doing sth.', '发挥作用，有影响'),
            ('make up', '编造(故事、谎言等)'),
            ('for example', '例如'),
            ('take...seriously', '认真对待'),
            ('not everybody', '并不是每个人'),
            ('close to', '离……近'),
            ('more and more', '越来越……'),
        ],
        'patterns': [
            ("What's the best movie theater?", '最好的电影院是哪家？'),
            ('The DJs choose songs the most carefully.', '流行音乐节目主持人最认真地选择歌曲。'),
            ('How do you like it so far?', '到目前为止，你认为它怎么样?'),
            ('Thanks for telling me.', '多谢你告诉我。'),
            ('They play a role in deciding the winner.', '他们在决定胜利者方面起着重要作用。'),
        ],
        'grammar': [
            ('形容词最高级', '表示三者或三者以上中的最高程度', '主语 + be动词 + the + 形容词最高级 + in/of + 范围', 'This is the best movie theater in town.\nShe is the most careful student in our class.'),
        ]
    },
    {
        'unit': 5,
        'name': 'Do you want to watch a game show?',
        'phrases': [
            ('find out', '查出/发现'),
            ('be ready to do', '准备做……'),
            ('dress up', '打扮/化妆成'),
            ("take one's place", '代替某人'),
            ('do a good job', '干得好/表演出色'),
            ('think of', '想到/思考'),
            ('game show', '游戏节目'),
            ('learn from', '向……学习'),
            ('talk show', '访谈节目'),
            ('soap opera', '肥皂剧'),
            ('go on', '继续'),
            ('watch a movie', '看电影'),
            ('one of...', '……之一'),
            ("try one's best to", '竭尽全力'),
            ('a pair of', '一双'),
            ('as famous as', '一样闻名/出名'),
            ('look like', '看起来像'),
            ('around the world', '世界各地'),
            ('have a discussion about', '讨论……'),
            ('one day', '有一天/某一天'),
            ('such as', '例如'),
            ('a symbol of', '一个象征/标志'),
            ('something enjoyable', '快乐的事情'),
            ('interesting information', '有趣的信息'),
        ],
        'patterns': [
            ('—Do you want to watch the news?\n—Yes, I do./No, I don\'t.', '你想看新闻吗？是的/不。'),
            ('—What do you think of talk shows?\n—I don\'t mind them./I can\'t stand them./I love watching them.', '你觉得访谈节目怎么样？我不介意/我不能忍受/我喜欢看。'),
            ('I hope to find out what\'s going on around the world.', '我希望发现世界正在发生的事情。'),
        ],
        'grammar': [
            ('动词不定式作宾语', '动词后接to do作宾语', 'want/hope/plan/expect + to do sth.', 'I want to watch a game show.\nShe hopes to be a reporter.'),
        ]
    },
    {
        'unit': 6,
        'name': "I'm going to study computer science.",
        'phrases': [
            ('grow up', '长大'),
            ('every day', '每天'),
            ('be sure about', '对某事确信'),
            ('make sure', '确信/有把握'),
            ('send...to...', '把……发送到……/把……寄……'),
            ('be able to', '能/能够'),
            ('the meaning of', '……的意思/含义'),
            ('different kinds of', '不同种类的'),
            ('have...in common', '有……共同点'),
            ('at the beginning of', '在……开始的时候'),
            ('write down', '写下/记下'),
            ('have to do with', '与……有关系'),
            ('take up', '开始从事/着手处理/接受'),
            ('hardly ever', '几乎不'),
            ('too...to...', '太……而不能……'),
        ],
        'patterns': [
            ('—What do you want to be when you grow up?\n—I want to be an engineer.', '当你长大的时候想当什么？我想当工程师。'),
            ('—How are you going to do that?\n—I\'m going to study math really hard.', '你打算怎样做呢？我打算努力学习数学。'),
            ('My parents want me to be a doctor, but I\'m not sure about that.', '我的双亲想要我当医生，但我还不确定。'),
            ('I\'m going to practice basketball every day.', '我打算每天练习篮球。'),
            ('My New Year\'s resolution is to get good grades.', '我的新年决心是取得好成绩。'),
        ],
        'grammar': [
            ('be going to结构', '表示将来的打算、计划或安排', '主语 + be going to + 动词原形 + 其他', 'I\'m going to study computer science.\nShe is going to be a doctor.'),
        ]
    },
    {
        'unit': 7,
        'name': 'Will people have robots?',
        'phrases': [
            ('on computers', '在电脑上'),
            ('on paper', '在纸上'),
            ('live to be 200 years old', '活到200岁'),
            ('free time', '空闲时间'),
            ('in danger', '处于危险之中'),
            ('on the earth', '在地球上'),
            ('play a part in', '参与；发挥作用'),
            ('space station', '太空站'),
            ('look for', '寻找'),
            ('computer programmer', '电脑程序设计师'),
            ('in the future', '在将来'),
            ('hundreds of', '许多；大量'),
            ('the same as', '和……一样'),
            ('over and over again', '多次；反复地'),
            ('get bored', '变得厌烦'),
            ('be able to', '能够'),
            ('wake up', '醒来'),
            ('fall down', '突然倒下；跌倒'),
        ],
        'patterns': [
            ('—Will there be less pollution?\n—Yes, there will./No, there won\'t.', '会有更少的污染吗？是的/不。'),
            ('Kids will study at home on computers.', '孩子们将在家里通过电脑学习。'),
            ('People will have robots in their homes.', '人们家里会有机器人。'),
            ('What will the future be like?', '未来会是什么样子的？'),
        ],
        'grammar': [
            ('一般将来时will', '表示将来要发生的动作或存在的状态', '主语 + will + 动词原形 + 其他', 'People will have robots.\nShe will be a teacher.'),
        ]
    },
    {
        'unit': 8,
        'name': 'How do you make a banana milk shake?',
        'phrases': [
            ('milk shake', '奶昔'),
            ('turn on', '接通（电流、煤气、水等）；打开'),
            ('pour...into...', '把……倒入……'),
            ('cut up', '切碎'),
            ('put...into...', '把……放入……'),
            ('one cup of yogurt', '一杯酸奶'),
            ('a piece of bread', '一片面包'),
            ('another ten minutes', '另外十分钟'),
            ('mix up', '混合在一起'),
            ('add...to...', '把……加到……'),
            ('fill...with...', '用……装满……'),
            ('cover...with...', '用……覆盖……'),
            ('one by one', '一个接一个'),
            ('a long time', '很长时间'),
            ('cut...into pieces', '把……切成片'),
        ],
        'patterns': [
            ('—How do you make a banana milk shake?\n—First, peel the bananas...', '你怎么制作香蕉奶昔？首先，剥香蕉皮……'),
            ('—How many bananas do we need?\n—We need three bananas.', '我们需要多少香蕉？我们需要三根香蕉。'),
            ('—How much yogurt do we need?\n—We need one cup of yogurt.', '我们需要多少酸奶？我们需要一杯酸奶。'),
        ],
        'grammar': [
            ('祈使句', '表示请求、命令、建议等', '动词原形开头的句子', 'Peel the bananas.\nPour the milk into the blender.'),
            ('可数名词与不可数名词', '可数名词有单复数变化，不可数名词没有', '可数名词用how many提问，不可数名词用how much提问', 'How many apples?\nHow much water?'),
        ]
    },
    {
        'unit': 9,
        'name': 'Can you come to my party?',
        'phrases': [
            ('on Saturday afternoon', '在星期六下午'),
            ('have to', '必须'),
            ('prepare for', '准备'),
            ('go to the doctor', '去看病'),
            ('have the flu', '患流感'),
            ('help my parents', '给父母帮忙'),
            ('come to the party', '参加晚会'),
            ('meet my friend', '见朋友'),
            ('too much homework', '太多的家庭作业'),
            ('go to the movies', '去看电影'),
            ('another time', '下次，另外的时间，别的时间'),
            ('last fall', '去年秋天'),
            ('hang out', '闲逛'),
            ('after school', '放学后'),
            ('on the weekend', '在周末'),
            ('study for a test', '备考'),
            ('visit grandparents', '拜访爷爷奶奶'),
            ('the day before yesterday', '前天'),
            ('the day after tomorrow', '后天'),
            ('have a piano lesson', '上钢琴课'),
            ('look after', '照看'),
            ('make an invitation', '制定邀请'),
            ('accept an invitation', '接受邀请'),
            ('turn down an invitation', '拒绝邀请'),
            ('take a trip to', '去……旅游'),
            ('at the end of this month', '在本月底'),
            ('look forward to', '期望/渴望'),
            ('the opening of...', '……的开幕/开业'),
            ('reply in writing', '写回信'),
            ('go shopping', '购物'),
            ('do homework', '做作业'),
            ('go to the concert', '参加音乐会'),
            ('not...until...', '直到……才……'),
        ],
        'patterns': [
            ('—Can you come to my party on Saturday afternoon?\n—Sure, I\'d love to. / Sorry, I can\'t. I have to prepare for an exam.', '星期六下午你能参加我的晚会吗？当然，我愿意去。/抱歉，我去不了。我必须要为考试做准备。'),
            ("I'm not available. = I'm not free.", '我没空。'),
            ("I'm afraid I can't. = I'm afraid not.", '恐怕不能。'),
            ('Sam isn\'t leaving until next Wednesday.', 'Sam要直到下周四才离开。'),
            ('I look forward to hearing from you all.', '我盼望着收到你的信。'),
        ],
        'grammar': [
            ('情态动词can表示邀请', '用于发出邀请', 'Can + 主语 + 动词原形 + 其他?', 'Can you come to my party?\nCan you help me?'),
            ('have to 与 must', 'have to表示客观需要，must表示主观意愿', 'have to + 动词原形', 'I have to study for the test.\nYou must be careful.'),
        ]
    },
    {
        'unit': 10,
        'name': "If you go to the party, you'll have a great time!",
        'phrases': [
            ('have a great time', '玩得开心'),
            ('stay at home', '待在家里'),
            ('take the bus', '乘公共汽车'),
            ('tomorrow night', '明天晚上'),
            ('have a class party', '开班级聚会'),
            ('half the class', '一半的学生'),
            ('make some food', '做些食物'),
            ('order food', '订购食物'),
            ('at the party', '在聚会上'),
            ('potato chips', '炸土豆片；薯条'),
            ('be upset', '心烦意乱；沮丧'),
            ('give sb. some advice', '给某人提些建议'),
            ('travel around the world', '环游世界'),
            ('go to college', '上大学'),
            ('make a lot of money', '赚很多钱'),
            ('get an education', '接受教育'),
            ('keep...to oneself', '保守秘密'),
            ('in the end', '最后'),
            ('be angry with sb.', '生某人的气'),
            ('be afraid to do sth.', '害怕做某事'),
            ('talk to sb.', '与某人交谈'),
            ('in half', '分成两半'),
            ('solve a problem', '解决问题'),
            ('school clean-up', '学校大扫除'),
            ('children\'s hospital', '儿童医院'),
        ],
        'patterns': [
            ('—I think I\'ll take the bus to the party.\n—If you do, you\'ll be late.', '我想我会乘公共汽车去参加聚会。如果你这样做，你会迟到的。'),
            ('—I think I\'ll stay at home.\n—If you do, you\'ll be sorry.', '我想我会待在家里。如果你这样做，你会遗憾的。'),
            ('If you go to the party, you\'ll have a great time!', '如果你去参加聚会，你会玩得很开心！'),
            ('What will happen if they have the party today?', '如果他们今天开聚会会发生什么？'),
        ],
        'grammar': [
            ('if引导的条件状语从句', '表示在某种条件下会发生什么', 'If + 一般现在时，主句用一般将来时(will + 动词原形)', 'If it rains tomorrow, I will stay at home.\nIf you study hard, you will pass the exam.'),
        ]
    },
]

# 八年级下册完整数据 (Unit 1-10)
GRADE8_DOWN_DATA = [
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
            ("take one's temperature", '量体温'),
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
            ('have problems breathing', '呼吸困难'),
        ],
        'patterns': [
            ("—What's the matter?\n—I have a stomachache.", '你怎么了? 我胃疼。'),
            ('You should lie down and rest.', '你应该躺下休息一会儿。'),
            ("You shouldn't go out at night.", '你晚上不应该出去。'),
        ],
        'grammar': [
            ('情态动词should/shouldn\'t', '表示建议', '主语 + should/shouldn\'t + 动词原形', 'You should drink more water.\nYou shouldn\'t eat too much junk food.'),
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
            ('be able to', '能够'),
        ],
        'patterns': [
            ('The boy could give out food at the food bank.', '这个男孩可以在食品救济站分发食物。'),
            ('He volunteers at an animal hospital every Saturday morning.', '每周六上午，他都在一家动物医院当志愿者。'),
        ],
        'grammar': [
            ('动词不定式作宾语补足语', '动词 + 宾语 + to do', 'ask sb. to do sth.\ntell sb. to do sth.\nwant sb. to do sth.', 'My mother asked me to clean my room.\nThe teacher told us to study hard.'),
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
            ('take care of', '照顾;照看'),
        ],
        'patterns': [
            ('—Could you please clean your room?\n—Yes, sure.', '你能整理一下你的房间吗? 当然可以。'),
            ("—Could I use your computer?\n—Sorry, I'm going to work on it now.", '我可以用一下你的电脑吗? 抱歉,我现在要用它工作。'),
        ],
        'grammar': [
            ('Could you please...?', '表示委婉请求', 'Could you please + 动词原形?', 'Could you please help me?\nCould you please open the window?'),
            ('Could I...?', '表示请求许可', 'Could I + 动词原形?', 'Could I use your phone?\nCould I borrow your book?'),
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
            ('give sb. pressure', '给某人施压'),
        ],
        'patterns': [
            ("—Why don't you forget about it?\n—That's a good idea.", '你为什么不忘掉它呢? 好主意。'),
            ("Although she's wrong, it's not a big deal.", '虽然她错了,但这并不是什么大事儿。'),
        ],
        'grammar': [
            ('Why don\'t you...?', '表示建议', 'Why don\'t you + 动词原形? = Why not + 动词原形?', "Why don't you talk to your parents?\nWhy not go to the movies?"),
            ('so that', '以便;为了', 'so that + 从句', 'I study hard so that I can get good grades.'),
        ]
    },
    {
        'unit': 5,
        'name': 'What were you doing when the rainstorm came?',
        'phrases': [
            ('make sure', '确信;确认'),
            ('beat against...', '拍打……'),
            ('fall asleep', '进入梦乡;睡着'),
            ('die down', '逐渐变弱;逐渐消失'),
            ('wake up', '醒来'),
            ('in a mess', '一团糟'),
            ('break...apart', '使……分离'),
            ('in times of difficulty', '在困难的时候'),
            ('at the time of', '当……时候'),
            ('go off', '(闹钟)发出响声'),
            ('take a hot shower', '洗热水澡'),
            ('miss the bus', '错过公交车'),
            ('pick up', '接电话'),
            ('bring...together', '使……靠拢'),
            ('in the area', '在这个地区'),
            ('miss the event', '错过这个事件'),
            ('by the side of the road', '在路边'),
            ('the Animal Helpline', '动物保护热线'),
            ('walk by', '走路经过'),
            ("make one's way to", '在某人去……的路上'),
            ('hear the news', '听到这个消息'),
            ('important events in history', '历史上的重大事件'),
            ('in silence', '沉默;无声'),
            ('take down', '拆除;摧毁'),
            ('have meaning to', '对……有意义'),
            ('remember doing sth.', '记得做过某事'),
            ('at first', '首先;最初'),
        ],
        'patterns': [
            ('—What were you doing at eight last night?\n—I was taking a shower.', '昨晚8点你在干什么？我在洗淋浴。'),
            ('When it began to rain, Ben was helping his mom make dinner.', '当开始下雨的时候，本正在帮他妈妈做晚饭。'),
            ('—What was Jenny doing while Linda was sleeping?\n—While Linda was sleeping, Jenny was helping Mary with her homework.', '琳达在睡觉的时候，珍妮正在干什么？琳达在睡觉的时候，珍妮正在帮玛丽做作业。'),
        ],
        'grammar': [
            ('过去进行时', '表示过去某个时间正在进行的动作', '主语 + was/were + 动词-ing形式 + 其他', 'I was reading when the rainstorm came.\nShe was cooking at 8 o\'clock last night.'),
        ]
    },
    {
        'unit': 6,
        'name': 'An old man tried to move the mountains.',
        'phrases': [
            ('work on doing sth.', '致力于做某事'),
            ('as soon as...', '一……就……'),
            ('once upon a time', '从前'),
            ('continue to do sth.', '继续做某事'),
            ('make sth. happen', '使某事发生'),
            ('try to do sth.', '试图做某事'),
            ('the journey to sp.', '……之旅'),
            ('tell the/a story', '讲故事'),
            ('put on', '穿上'),
            ('a little bit', '有点儿'),
            ('keep doing sth.', '坚持做某事'),
            ('give up', '放弃'),
            ('instead of', '代替;反而'),
            ('turn...into', '变成'),
            ('get married', '结婚'),
            ('the main character', '主要人物;主人公'),
            ('at other times', '在另外一些时候'),
            ('be able to', '能;会'),
            ('come out', '(书、电影等)出版'),
            ('become interested in', '对……感兴趣'),
            ('walk to the other side', '走到另一边去'),
            ('a fairy tale', '一个神话故事'),
            ('the rest of the story', '故事的其余部分'),
            ('leave sb. to do sth.', '让某人做某事'),
            ('make a plan to do sth.', '筹划/计划做某事'),
            ('go to sleep', '去睡觉'),
            ('lead sb. to sp.', '把某人领到某地'),
            ('get lost', '迷路'),
            ('change one\'s plan', '改变计划'),
            ('tell sb. to do sth.', '叫某人做某事'),
            ('in the moonlight', '在月光下'),
            ("find one's way home", '找到某人回家的路'),
            ('the next day', '第二天'),
            ('send sb. to sp.', '派某人去某地'),
        ],
        'patterns': [
            ('What do you think about/of...?', '你觉得……怎么样？'),
            ("It doesn't seem adj. to do sth.", '做某事似乎不……'),
            ('This is because...', '这是因为……'),
            ('...so...that...', '如此……以至于……'),
            ('It takes sb. some time to do sth.', '某人花多少时间做某事'),
            ('...not...until...', '直到……才……'),
        ],
        'grammar': [
            ('连词unless, as soon as, so...that', '引导不同类型的从句', 'unless = if not\nas soon as表示时间\nso...that表示结果', 'I won\'t go unless you go.\nI\'ll call you as soon as I arrive.\nHe is so tired that he can\'t walk.'),
        ]
    },
    {
        'unit': 7,
        'name': "What's the highest mountain in the world?",
        'phrases': [
            ('as big as', '与……一样大'),
            ('one of the oldest countries', '最古老的国家之一'),
            ('feel free to do sth.', '随意地做某事'),
            ('as far as I know', '据我所知'),
            ('man-made objects', '人造物体'),
            ('part of...', '……的组成部分'),
            ('the highest mountain', '最高的山脉'),
            ('in the world', '在世界上'),
            ('any other mountain', '其他任何一座山'),
            ('of all the salt lakes', '在所有的咸水湖中'),
            ('run along', '跨越……'),
            ('freezing weather', '冰冻的天气'),
            ('take in air', '呼吸空气'),
            ('the first people to do sth.', '第一个做某事的人'),
            ('in the face of difficulties', '面临危险'),
            ('give up doing sth.', '放弃做某事'),
            ("achieve one's dream", '实现某人的梦想'),
            ('the forces of nature', '自然界的力量'),
            ('reach the top', '到达顶峰'),
            ('even though', '虽然;尽管'),
            ('at birth', '在出生的时候'),
            ('be awake', '醒着'),
            ('run over with excitement', '兴奋地跑过去'),
            ('walk into sb.', '撞到某人'),
            ('fall over', '摔倒'),
            ('take care of', '照顾;照料'),
            ('every two years', '每两年'),
            ('cut down the forests', '砍伐林木'),
            ('endangered animals', '濒危动物'),
            ('fewer and fewer pandas', '大熊猫越来越少'),
            ('be in danger', '处于危险之中'),
        ],
        'patterns': [
            ('How high is Qomolangma?', '珠穆朗玛峰有多高？'),
            ('It is also very hard to take in air as you get near the top.', '当你接近山顶时，连呼吸都会困难。'),
            ('One of the main reasons is because people want to challenge themselves in the face of difficulties.', '其中的一个主要原因是人们想要在面临困难时挑战自己。'),
            ('The spirit of these climbers shows us that we should never give up trying to achieve our dreams.', '这些登山者的精神向我们证明：我们永远都不应该放弃实现自己的梦想。'),
            ('Although Japan is older than Canada, it is much smaller.', '虽然日本比加拿大有更悠久的历史，但是日本比加拿大小多了。'),
        ],
        'grammar': [
            ('形容词和副词的比较级和最高级', '表示程度的不同', '比较级：比较两者\n最高级：比较三者及以上', 'This mountain is higher than that one.\nQomolangma is the highest mountain in the world.'),
        ]
    },
    {
        'unit': 8,
        'name': 'Have you read Treasure Island yet?',
        'phrases': [
            ('on page 25', '在第25页'),
            ('the back of the book', '书的背面'),
            ('hurry up', '赶快;匆忙'),
            ('in two weeks', '在两周之内'),
            ('go out to sea', '出海'),
            ('an island full of treasures', '一个满是宝藏的岛屿'),
            ('write about', '写作关于……的内容'),
            ('finish doing sth.', '做完某事'),
            ('wait for another ship', '等待另一艘船到来'),
            ('learn to do sth.', '学会做某事'),
            ('grow fruits and vegetables', '种水果和蔬菜'),
            ('a few weeks ago', '几个星期前'),
            ("the marks of another man's feet", '另一个人的脚印'),
            ('not long after that', '不久之后'),
            ('run towards sp.', '跑向某地'),
            ('use...to do sth.', '用……来做某事'),
            ('signs left behind by someone', '某人留下的标记'),
            ('read the newspaper', '看报'),
            ('science fiction', '科幻小说'),
            ("can't wait to do sth.", '迫不及待地做某事'),
            ('a good way to wake up', '醒来的一个好办法'),
            ('number of people', '人数'),
            ('used to do sth.', '(过去)常常做某事'),
            ('study abroad', '在国外学习'),
            ('make sb. do sth.', '使某人做某事'),
            ('come to realize', '开始意识到'),
            ('ever since then', '自从那时起'),
            ('the southern states of America', '美国的南部地区'),
            ('belong to', '属于'),
            ('be kind to each other', '善待彼此'),
            ('trust one another', '互相信任'),
            ('the beauty of nature', '大自然的美'),
            ('have been to sp.', '去过某地'),
            ('do some research on sth.', '对……做研究'),
            ('hope to do sth.', '希望做某事'),
            ('see sb. do sth.', '看到某人做某事'),
        ],
        'patterns': [
            ('—Have you read Little Women yet?\n—Yes, I have./No, I haven\'t.', '你读过《小妇人》吗？是的，我读过。/不，我没有。'),
            ('—Has Tina read Treasure Island yet?\n—Yes, she has. She thinks it\'s fantastic.', '蒂娜读过《金银岛》这本书吗？是的，她读过。她觉得它很棒。'),
            ("I heard you lost your key.", '我听说你丢钥匙了。'),
            ('She came to realize how much she actually missed all of them.', '她开始意识到，事实上她是多么想念他们所有的人。'),
        ],
        'grammar': [
            ('现在完成时', '表示过去发生或已经完成的动作对现在造成的影响或结果', '主语 + have/has + 过去分词 + 其他', 'I have already read this book.\nShe hasn\'t finished her homework yet.'),
        ]
    },
    {
        'unit': 9,
        'name': 'Have you ever been to a museum?',
        'phrases': [
            ('at night', '在夜晚'),
            ('in a more natural environment', '在一个更加自然的环境中'),
            ('all year round', '一年到头;终年'),
            ('be far from', '离……远'),
            ('in the dark', '在黑暗中'),
            ('in the past', '在过去'),
            ('have been to sp.', '去过某地'),
            ('science museum', '科学博物馆'),
            ('history museum', '历史博物馆'),
            ('amusement park', '游乐园'),
            ('go somewhere different', '去不同的地方'),
            ('go skating', '去滑冰'),
            ('take the subway', '坐地铁'),
            ('a great way to spend a Saturday afternoon', '一个过周六下午的好方法'),
            ('all the old movie cameras', '所有的古老的电影摄影机'),
            ('learn about sth.', '了解有关……的情况'),
            ('on the weekend', '在周末'),
            ('camp in the mountains', '在大山里露营'),
            ('put up a tent', '搭帐篷'),
            ('in such a rapid way', '以如此迅猛的方式'),
            ('different kinds of', '各种各样的'),
            ('development of toilets', '厕所的发展'),
            ('social groups', '社会团体'),
            ('the tea art performances', '茶艺表演'),
            ('make a perfect cup of tea with beautiful tea sets', '用漂亮的茶具沏一杯完美的茶'),
            ('a nice place to enjoy tea', '一个品茶的好地方'),
            ('thousands of', '数以千计的'),
            ('International Museum of Toilets', '国际厕所博物馆'),
            ('the Terracotta Army', '兵马俑'),
            ('Southeast Asia', '东南亚'),
            ('Night Safari', '夜间动物园'),
            ('three quarters', '四分之三'),
            ('an English-speaking country', '一个讲英语的国家'),
            ('have problem doing sth.', '做某事很困难'),
            ('during the daytime', '在白天'),
            ('a couple of times', '好几次'),
            ('right now', '现在;目前'),
            ('an amusement park with a special theme', '一个有特别的主题的游乐园'),
            ('walk around the park', '在公园里到处走'),
            ('hear of', '听说'),
            ('take a ride', '兜风'),
            ('another province', '另一个省'),
            ("the Bird's Nest", '鸟巢'),
            ('encourage sb. to do sth.', '鼓励某人做某事'),
            ('on the one hand...on the other hand', '一方面，另一方面'),
        ],
        'patterns': [
            ('Have you ever been to a science museum?', '你曾经去过科学博物馆吗？'),
            ("Let's go somewhere different today.", '我们今天去个不同的地方吧。'),
            ('It\'s unbelievable that technology has progressed in such a rapid way!', '科技以如此迅猛的方式发展真是令人难以置信啊！'),
            ('One great thing about Singapore is that the temperature is almost the same all year round.', '新加坡一个很大的特征是它的气温几乎一年到头都是一样的。'),
            ('It is best to visit the zoo in the evening.', '最好在晚上参观这个动物园。'),
        ],
        'grammar': [
            ('现在完成时have been to', '表示曾经去过某地（现在已回来）', 'have/has been to + 地点', 'I have been to Beijing twice.\nShe has been to the museum.'),
        ]
    },
    {
        'unit': 10,
        'name': "I've had this bike for three years.",
        'phrases': [
            ('these days', '目前;现在'),
            ('regard with great interest', '以极大的兴趣关注着'),
            ('in order to', '为了'),
            ('so far', '迄今;到现在为止'),
            ('in need', '需要'),
            ('not...anymore', '不再……'),
            ('welcome to sp.', '欢迎来到……'),
            ('check out', '察看;观察'),
            ('board games', '棋类游戏'),
            ('one last thing', '最后一样东西'),
            ('junior high school', '初级中学'),
            ('clear out', '清理'),
            ('no longer', '不再;不复'),
            ('toy monkey', '玩具猴'),
            ('part with', '与……分开'),
            ('to be honest', '说实在的'),
            ('ride a bike', '骑自行车'),
            ('have a yard sale', '进行庭院拍卖会'),
            ("one's old things", '某人的旧东西'),
            ('bring back sweet memories', '勾起甜美的回忆'),
            ('give away', '捐赠'),
            ('play for a while', '玩一会儿'),
            ('do with...', '处置;处理'),
            ('search for work', '找工作'),
            ('for the last 13 years', '在过去的13年里'),
            ('the mid-20th century', '20世纪中期'),
            ('stay the same', '保持原状'),
            ('according to', '依据;按照'),
            ("in one's opinion", '依……看'),
            ('in my time', '在我那个年代'),
        ],
        'patterns': [
            ('—How long have you had that bike over there?\n—I\'ve had it for three years.', '那边的那辆自行车你买了多久了？我买了三年了。'),
            ('Amy has had her favorite book for three years.', '艾米拥有她最喜欢的书3年了。'),
            ("He's owned it since his fourth birthday.", '自他4岁生日起，他拥有这个东西了。'),
            ('Some people still live in their hometown. However, others may only see it once or twice a year.', '有些人仍然住在家乡。然而，另一些人可能一年只能回家乡一两次。'),
            ("As for me, I did not want to give up my football shirts. But, to be honest, I have not played for a while now.", '至于我，我不想放弃我的足球衣。但是，说实在的，我现在已经有一段时间没有踢(足球)了。'),
        ],
        'grammar': [
            ('现在完成时延续性用法', '表示从过去某一时间开始一直延续到现在的动作或状态', '主语 + have/has + 过去分词 + for + 时间段\n主语 + have/has + 过去分词 + since + 时间点', 'I have had this bike for three years.\nShe has lived here since 2010.'),
        ]
    },
]


def insert_data(conn, data_list, semester):
    """插入数据到数据库"""
    cursor = conn.cursor()
    
    # 获取学科和年级ID
    cursor.execute("SELECT id FROM subjects WHERE name = '英语'")
    subject_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM grades WHERE name = '初二'")
    grade_id = cursor.fetchone()[0]
    
    for unit_data in data_list:
        # 检查是否已存在
        cursor.execute('''
            SELECT id FROM chapters 
            WHERE subject_id = ? AND grade_id = ? AND chapter_number = ? AND semester = ?
        ''', (subject_id, grade_id, unit_data['unit'], semester))
        
        if cursor.fetchone():
            continue  # 已存在，跳过
        
        # 插入章节
        cursor.execute('''
            INSERT INTO chapters (subject_id, grade_id, chapter_number, chapter_name, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject_id, grade_id, unit_data['unit'], unit_data['name'], semester))
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


def main():
    """主函数"""
    conn = sqlite3.connect(DB_PATH)
    
    print("正在插入八年级上册数据...")
    insert_data(conn, GRADE8_UP_DATA, '上册')
    
    print("正在插入八年级下册数据...")
    insert_data(conn, GRADE8_DOWN_DATA, '下册')
    
    # 统计
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM chapters")
    chapter_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phrases")
    phrase_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM sentence_patterns")
    pattern_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM grammar_points")
    grammar_count = cursor.fetchone()[0]
    
    print(f"\n=== 数据库统计 ===")
    print(f"章节/单元: {chapter_count} 个")
    print(f"重点短语: {phrase_count} 条")
    print(f"重点句型: {pattern_count} 条")
    print(f"语法点: {grammar_count} 个")
    
    # 显示八年级英语详情
    print(f"\n=== 八年级英语单元列表 ===")
    cursor.execute('''
        SELECT c.chapter_number, c.chapter_name, c.semester,
               (SELECT COUNT(*) FROM phrases WHERE chapter_id = c.id) as phrase_count,
               (SELECT COUNT(*) FROM sentence_patterns WHERE chapter_id = c.id) as pattern_count
        FROM chapters c
        JOIN subjects s ON c.subject_id = s.id
        JOIN grades g ON c.grade_id = g.id
        WHERE s.name = '英语' AND g.name = '初二'
        ORDER BY c.semester, c.chapter_number
    ''')
    
    current_semester = None
    for row in cursor.fetchall():
        if row[2] != current_semester:
            current_semester = row[2]
            print(f"\n【{current_semester}】")
        print(f"  Unit {row[0]}: {row[1]}")
        print(f"         短语: {row[3]}条, 句型: {row[4]}条")
    
    conn.close()
    print("\n数据录入完成！")


if __name__ == '__main__':
    main()

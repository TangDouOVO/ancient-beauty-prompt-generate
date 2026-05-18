#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古风图片生成提示词生成器
根据用户输入的关键词，生成高质量的图片生成提示词
"""

import sys
import re
import json
import random
from typing import List, Dict, Set, Tuple

# 语义分类词典
SEMANTIC_CATEGORIES = {
    # 朝代识别（新增）
    "朝代": {
        "keywords": ["汉代", "汉朝", "唐代", "唐朝", "宋代", "宋朝", "明代", "明朝", "清代", "清朝", "魏晋", "南北朝", "秦朝", "秦代", "汉唐", "唐宋"],
        "mapping": {
            "汉代": "汉代", "汉朝": "汉代",
            "唐代": "唐代", "唐朝": "唐代",
            "宋代": "宋代", "宋朝": "宋代",
            "明代": "明代", "明朝": "明代",
            "清代": "清代", "清朝": "清代",
            "魏晋": "魏晋",
            "南北朝": "南北朝",
            "秦朝": "秦代", "秦代": "秦代"
        }
    },
    # 人物类型与气质（互斥分类，确保一致性）
    "气质类型": {
        "keywords": ["御姐", "甜妹", "少女", "萝莉", "女王", "女神", "仙女", "魔女", "妖女"],
        "mapping": {
            "御姐": {"identity": "御姐", "temperament": "御姐范", "traits": ["成熟妩媚", "高贵冷艳", "气场强大"]},
            "甜妹": {"identity": "甜妹", "temperament": "甜美少女感", "traits": ["元气", "俏皮", "可爱"]},
            "少女": {"identity": "少女", "temperament": "灵动少女感", "traits": ["清纯", "灵动", "天真"]},
            "萝莉": {"identity": "萝莉", "temperament": "软萌萝莉感", "traits": ["软萌", "治愈", "纯真"]},
            "女王": {"identity": "女王", "temperament": "女王气场", "traits": ["霸气", "威严", "高贵"]},
            "女神": {"identity": "女神", "temperament": "女神范", "traits": ["圣洁", "优雅", "完美"]},
            "仙女": {"identity": "仙女", "temperament": "仙气飘飘", "traits": ["空灵", "脱俗", "清冷"]},
            "魔女": {"identity": "魔女", "temperament": "邪魅神秘感", "traits": ["魅惑", "神秘", "危险"]},
            "妖女": {"identity": "妖女", "temperament": "妖艳妩媚感", "traits": ["妩媚", "妖娆", "风情"]},
        }
    },
    # 人物外貌
    "人物": {
        "keywords": ["少女", "美人", "女子", "女孩", "女生", "女", "姑娘", "佳人", "仙子"],
        "templates": ["一位{adj}少女", "{adj}美人", "{adj}女子"]
    },
    "肤色": {
        "keywords": ["白皙", "冷白皮", "雪白", "瓷肌", "肌肤", "皮肤"],
        "related": ["皮肤白皙光滑", "皮肤白皙嫩滑", "冷白皮", "瓷肌", "清透肌肤", "白里透红"]
    },
    "容貌": {
        "keywords": ["颜值", "美貌", "容貌", "五官", "脸蛋", "长相", "倾国倾城", "绝色", "美艳"],
        "related": ["倾国倾城容貌", "高颜值", "绝美双眼", "精致五官", "完美脸型", "卡姿兰大眼睛"]
    },
    "表情": {
        "keywords": ["灵动", "清纯", "娇媚", "楚楚动人", "天真", "妩媚", "俏皮", "可爱", "甜美", "清冷", "疏离", "纯欲"],
        "related": ["灵动可爱", "元气", "纯欲", "俏皮", "萌", "温柔", "高贵", "甜美", "清冷感"]
    },

    # 发型发饰
    "发型": {
        "keywords": ["发", "头发", "长发", "黑发", "髻", "发髻", "碎发", "发丝"],
        "related": ["墨色长发", "长发及腰", "黑色长发", "复杂发髻", "蓬松发髻", "碎发", "发丝灵动"]
    },
    "发饰": {
        "keywords": ["发饰", "头饰", "簪花", "簪钗", "朱钗", "玉簪", "宝石", "珍珠发饰", "珍珠", "步摇", "流苏", "珠翠", "羽毛", "绒花", "面纱", "丝带"],
        "related": ["华丽发饰", "繁复发饰", "步摇", "流苏发饰", "绒花", "缠花发簪", "珠翠", "绢花发钗"]
    },

    # 服装服饰
    "服装": {
        "keywords": ["衣", "服", "裙", "衫", "纱", "袍", "襦裙", "汉服", "古装", "纱衣", "战衣", "铠甲"],
        "related": ["汉服", "魏晋风", "仙侠飘逸古装", "轻纱汉服", "大袖衫", "罗裙", "襦裙"]
    },
    "颜色": {
        "keywords": ["红色", "粉色", "白色", "黑色", "蓝色", "绿色", "黄色", "金色", "紫色", "青色", "橙色", "红", "粉", "白", "黑", "蓝", "绿", "黄", "金", "紫", "青", "橙"],
        "mapping": {
            "红": "红色", "红色": "红色",
            "粉": "粉色", "粉色": "粉色",
            "白": "白色", "白色": "白色",
            "黑": "黑色", "黑色": "黑色",
            "蓝": "蓝色", "蓝色": "蓝色",
            "绿": "绿色", "绿色": "绿色",
            "金": "金色", "金色": "金色",
            "青": "青色", "青色": "青色",
            "紫": "紫色", "紫色": "紫色",
            "橙": "橙色", "橙色": "橙色",
            "黄": "黄色", "黄色": "黄色"
        }
    },
    "配饰": {
        "keywords": ["配饰", "首饰", "项链", "耳饰", "手镯", "戒指", "坠饰"],
        "related": ["精美繁复服饰配饰", "项链", "耳饰", "华丽精美的步摇与细流苏发饰"]
    },

    # 场景
    "场景": {
        "keywords": ["荷花池", "樱花", "桃花", "梅花", "荷花", "竹林", "园林", "城楼", "烟雾", "朦胧", "雪景", "月下", "花海", "落花", "屏风", "庭院", "宫殿", "山水"],
        "related": ["古风背景", "唯美清新古风剧场景", "烟雾朦胧美", "仙气飘飘"]
    },
    "氛围": {
        "keywords": ["仙气", "梦幻", "唯美", "神秘", "朦胧", "意境", "氛围"],
        "related": ["仙气飘飘", "宛若仙境", "梦幻", "唯美", "神秘", "朦胧意境", "梦核"]
    },

    # 动作
    "动作": {
        "keywords": ["抱", "抚", "抬", "倚", "立", "坐", "伸手", "弹", "持", "握"],
        "exclude_single": ["拿", "抱", "抚", "抬", "倚", "立", "坐", "弹", "持", "握"],
        "related": ["抬手", "倚坐", "静立", "手伸向镜头", "与镜头互动"]
    },
    "道具": {
        "keywords": ["团扇", "琵琶", "琴", "筝", "笛", "箫", "乐器", "灯笼", "伞", "剑", "书", "花", "酒杯", "毛笔"],
        "related": ["手执团扇", "抱琵琶", "抚琴", "手持灯笼", "撑伞", "佩剑"]
    },

    # 摄影风格
    "胶片": {
        "keywords": ["胶片", "摄影", "复古", "质感"],
        "related": ["胶片摄影", "胶片颗粒质感", "复古胶片", "lomo效果"]
    },
    "光影": {
        "keywords": ["光", "影", "明暗", "曝光", "朦胧"],
        "related": ["伦勃朗光", "强烈明暗对比", "光影斑驳", "透光感", "朦胧美学"]
    },
}

# 丰富的背景细节词库
BACKGROUND_DETAILS = {
    # 自然景观
    "荷花池": [
        "荷花池畔，荷叶田田，粉荷初绽，蜻蜓点水",
        "荷花池边，水波粼粼，荷香四溢，晨雾缭绕",
        "荷花池景，莲叶接天，荷花朵朵，鸳鸯戏水",
        "夏夜荷塘，月色如水，荷影婆娑，萤火点点",
        "荷塘月色，清风徐来，荷叶摇曳，暗香浮动"
    ],
    "樱花": [
        "樱花树下，落英缤纷，花瓣飘舞，春风拂面",
        "樱花盛开，粉色花海，浪漫唯美，蝴蝶翩翩",
        "樱花漫天，花瓣如雨，梦幻场景，少女撑伞",
        "樱花大道，花瓣铺地，粉色世界，浪漫邂逅",
        "樱花纷飞，春意盎然，花瓣飘落肩头，唯美意境"
    ],
    "竹林": [
        "竹林深处，翠竹摇曳，清幽雅致，竹叶沙沙",
        "竹林小径，竹影婆娑，静谧深远，阳光斑驳",
        "竹林幽境，竹叶沙沙，禅意悠然，薄雾弥漫",
        "翠竹林间，清风徐来，竹香沁人，幽静深远",
        "竹林深处，曲径通幽，竹影摇曳，光影交错"
    ],
    "梅花": [
        "梅花盛开，暗香浮动，雪中红梅，傲骨铮铮",
        "梅林深处，花瓣飘落，清香四溢，冬意盎然",
        "梅花枝头，白雪皑皑，红梅映雪，清冷高洁",
        "梅园小径，落英缤纷，梅香扑鼻，诗意盎然"
    ],
    "桃花": [
        "桃花盛开，粉红烂漫，春意盎然，蝴蝶飞舞",
        "桃花林中，花瓣纷飞，粉霞漫天，少女如花",
        "桃花源里，落英缤纷，世外桃源，梦幻仙境",
        "桃花枝头，春色满园，蜂蝶翩翩，生机勃勃"
    ],
    
    # 建筑场景
    "园林": [
        "古典园林，亭台楼阁，曲径通幽，假山流水",
        "江南园林，假山流水，诗情画意，小桥流水",
        "园林春色，花木扶疏，典雅精致，鸟语花香",
        "苏州园林，粉墙黛瓦，曲廊回转，诗意盎然",
        "皇家园林，雕梁画栋，金碧辉煌，气派非凡"
    ],
    "屏风": [
        "屏风之后，若隐若现，神秘典雅，烛光摇曳",
        "精美屏风，刺绣花鸟，古韵悠长，光影斑驳",
        "屏风掩映，光影交错，层次丰富，意境深远",
        "绢质屏风，山水画作，墨香四溢，文人雅趣"
    ],
    "宫殿": [
        "宫殿深处，金碧辉煌，气势恢宏，烛火通明",
        "宫廷内景，雕梁画栋，富丽堂皇，珠帘轻垂",
        "宫殿长廊，烛光摇曳，神秘庄严，宫灯高悬",
        "御花园中，百花盛开，亭台楼阁，皇家气派",
        "寝宫之内，锦帐轻垂，香炉袅袅，华贵典雅"
    ],
    "庭院": [
        "庭院深深，花木葱茏，静谧安详，鸟鸣啾啾",
        "庭院一角，石桌石凳，古朴雅致，茶香袅袅",
        "庭院花开，蝴蝶翩翩，生机盎然，阳光明媚",
        "深宅大院，青石板路，古树参天，幽静深远",
        "小院清幽，竹篱茅舍，野花点缀，田园诗意"
    ],
    "城楼": [
        "古城楼上，旌旗猎猎，夕阳西下，金光万丈",
        "城墙之上，远山如黛，云雾缭绕，壮阔苍茫",
        "城楼之巅，俯瞰山河，万家灯火，气象万千"
    ],
    
    # 氛围场景
    "月下": [
        "月下独酌，清辉如水，静谧唯美，桂花飘香",
        "月色朦胧，银辉洒落，如梦如幻，夜风轻拂",
        "月下花前，光影交织，浪漫诗意，萤火点点",
        "明月当空，银光如练，夜色如水，清冷孤寂",
        "月下抚琴，琴声悠扬，月光如水，意境深远"
    ],
    "雪景": [
        "雪景如画，银装素裹，纯净无瑕，雪花纷飞",
        "雪花纷飞，白茫茫一片，静谧空灵，寒梅傲雪",
        "雪后初晴，阳光映雪，晶莹剔透，银光闪闪",
        "雪夜静谧，月光映雪，银装素裹，清冷唯美",
        "漫天飞雪，雪花飘落，天地一色，纯净空灵"
    ],
    "烟雾": [
        "烟雾缭绕，若隐若现，神秘莫测，仙气飘飘",
        "晨雾弥漫，朦胧唯美，薄纱轻笼，意境深远",
        "云雾飘渺，宛若仙境，虚无缥缈，超凡脱俗",
        "山间云雾，层层叠叠，若隐若现，如入仙境"
    ],
    "山水": [
        "青山绿水，云雾缭绕，山峦叠翠，流水潺潺",
        "高山流水，瀑布飞泻，云蒸霞蔚，壮丽非凡",
        "山水之间，小舟轻荡，渔歌唱晚，诗意盎然",
        "远山如黛，近水含烟，山水相依，如诗如画",
        "悬崖峭壁，云海翻涌，苍松翠柏，气势磅礴"
    ],
    
    # 特殊场景
    "战场": [
        "战火纷飞，狼烟四起，残阳如血，旌旗猎猎",
        "沙场点兵，战鼓擂动，尘土飞扬，气势如虹",
        "古战场边，断壁残垣，夕阳西下，苍凉悲壮"
    ],
    "仙境": [
        "仙气缭绕，云雾飘渺，宛若仙境，灵气充沛",
        "蓬莱仙境，仙鹤飞舞，祥云瑞气，超凡脱俗",
        "瑶池仙境，仙花盛开，灵泉流淌，仙乐飘飘"
    ],
    "夜晚": [
        "夜色如墨，星光点点，萤火飞舞，静谧安详",
        "华灯初上，灯火阑珊，夜色迷人，流光溢彩",
        "深夜庭院，烛光摇曳，月影婆娑，幽静深远"
    ],
    "黄昏": [
        "夕阳西下，金光万丈，晚霞满天，壮丽辉煌",
        "黄昏时分，残阳如血，云霞绚烂，诗意盎然",
        "暮色苍茫，远山含黛，炊烟袅袅，宁静祥和"
    ],
    
    # 默认场景（大幅扩展）
    "default": [
        "唯美清新古风剧场景，典雅宫廷剧感浓郁，光影层次丰富",
        "古风意境深远，光影交错，诗情画意，韵味悠长",
        "仙气缭绕，云雾飘渺，宛若仙境，超凡脱俗",
        "古典韵味十足，雕梁画栋，古色古香，意境深远",
        "江南水乡，小桥流水，烟雨朦胧，诗意盎然",
        "深宅大院，青砖黛瓦，古木参天，幽静深远",
        "花木扶疏，鸟语花香，阳光斑驳，生机盎然",
        "烛光摇曳，珠帘轻垂，香炉袅袅，华贵典雅",
        "月色如水，清风徐来，花香四溢，静谧唯美",
        "远山如黛，近水含烟，山水相依，如诗如画",
        "晨曦初露，薄雾轻笼，露珠晶莹，清新脱俗",
        "古巷深处，青石板路，斑驳墙面，岁月静好"
    ]
}

# 丰富的人物细节词库
CHARACTER_DETAILS = {
    "御姐": {
        "face": ["精致脸蛋、完美脸型", "轮廓分明、气质冷艳", "眉眼如画、唇红齿白"],
        "eyes": ["杏眼、眼神犀利", "凤眼、眼波流转", "明眸善睐、眼神深邃"],
        "skin": ["冷白肤色", "瓷白肌肤", "雪肤花容"],
        "hair": ["黑色长发、复杂发髻", "墨色长发、发丝飘逸", "乌黑秀发、发髻高挽"],
        "makeup": ["精致妆容、红唇烈焰", "淡妆浓抹、气质冷艳", "高级感妆容、气场全开"],
        "expression": ["成熟妩媚、高贵冷艳", "气场强大、不怒自威", "清冷疏离、高不可攀"]
    },
    "甜妹": {
        "face": ["精致脸蛋、完美脸型", "娃娃脸、胶原蛋白满满", "鹅蛋脸、甜美可人"],
        "eyes": ["杏眼、眼神清澈", "桃花眼、眼波盈盈", "灵动大眼、眼眸闪亮"],
        "skin": ["冷白肤色", "白里透红", "粉嫩肌肤"],
        "hair": ["黑色长发、双马尾", "墨色长发、发丝柔顺", "乌黑秀发、空气刘海"],
        "makeup": ["清透妆容、元气满满", "粉嫩妆容、少女感十足", "裸妆感、自然清新"],
        "expression": ["元气、俏皮、可爱", "甜美、活泼、温柔", "纯欲、软萌、治愈"]
    },
    "少女": {
        "face": ["精致脸蛋、完美脸型", "青春洋溢、胶原蛋白", "清秀面容、楚楚动人"],
        "eyes": ["杏眼、眼神清澈", "灵动双眸、眼波流转", "明眸皓齿、眼神纯真"],
        "skin": ["冷白肤色", "白皙嫩滑", "肌肤如雪"],
        "hair": ["黑色长发、发丝飘逸", "墨色长发、简单发髻", "乌黑秀发、碎发轻盈"],
        "makeup": ["清透妆容、自然精致", "淡妆素雅、青春气息", "裸妆感、纯净无暇"],
        "expression": ["清纯、灵动、天真", "温柔、恬静、美好", "纯欲、娇羞、动人"]
    },
    "仙女": {
        "face": ["精致脸蛋、完美脸型", "仙气飘飘、超凡脱俗", "清冷面容、不染尘埃"],
        "eyes": ["杏眼、眼神空灵", "凤眼、眼波如水", "明眸善睐、不食人间烟火"],
        "skin": ["冷白肤色", "雪肤冰肌", "白璧无瑕"],
        "hair": ["黑色长发、发丝飘扬", "墨色长发、仙气缭绕", "乌黑秀发、发带飘逸"],
        "makeup": ["清透妆容、仙气十足", "淡妆素雅、超凡脱俗", "裸妆感、不染纤尘"],
        "expression": ["空灵、脱俗、清冷", "圣洁、高雅、出尘", "仙气飘飘、不食人间烟火"]
    },
    "妖女": {
        "face": ["精致脸蛋、完美脸型", "妖艳妩媚、风情万种", "魅惑面容、摄人心魄"],
        "eyes": ["杏眼、眼神魅惑", "凤眼、眼波流转", "媚眼如丝、摄人心魂"],
        "skin": ["冷白肤色", "雪肤花容", "白皙如玉"],
        "hair": ["黑色长发、发丝妖娆", "墨色长发、发髻华丽", "乌黑秀发、发饰璀璨"],
        "makeup": ["精致妆容、妖艳动人", "浓妆艳抹、风情万种", "魅惑妆容、摄人心魄"],
        "expression": ["妩媚、妖娆、风情", "魅惑、勾人、摄魂", "妖艳、动人、销魂"]
    },
    "default": {
        "face": ["精致脸蛋、完美脸型", "面容姣好、五官精致", "轮廓优美、气质出众"],
        "eyes": ["杏眼、眼神清澈", "明眸善睐、眼波流转", "灵动双眸、眼眸闪亮"],
        "skin": ["冷白肤色", "白皙嫩滑", "肌肤如雪"],
        "hair": ["黑色长发、发丝飘逸", "墨色长发、发髻精致", "乌黑秀发、发饰华丽"],
        "makeup": ["精致妆容、自然高级", "清透妆容、气质出众", "淡妆浓抹、恰到好处"],
        "expression": ["温柔、恬静、美好", "灵动、俏皮、可爱", "优雅、高贵、迷人"]
    }
}

# 服装细节词库（完全基于优质提示词文档）
CLOTHING_DETAILS = {
    "红色": [
        "红色纱衣、露肩、发丝和红色丝带飘扬",
        "一袭红衣随风飘动、奢华的配饰彰显独特品味",
        "红色烟霞色蹙金绣罗裙、裙裾上苏绣的湘妃竹纹层层叠叠",
        "赭石暗红正红织金柔软面料衣服、华丽精致",
        "朱红色汉服、刺绣精美、袖口宽大"
    ],
    "粉色": [
        "华丽浅绿色+粉色襦裙、柔美浪漫",
        "粉霞色罗裙、少女感十足",
        "浅粉色纱衣、仙气飘飘、轻纱外披",
        "粉色唯美古风少女服装、萌系古风贵族少女感"
    ],
    "白色": [
        "纯白纱衣、仙气飘飘、清冷出尘",
        "素白罗裙、不染纤尘、超凡脱俗",
        "浅米色汉服、带红色装饰和花纹",
        "白色汉服、清冷感、不染纤尘"
    ],
    "蓝色": [
        "蓝白色刺绣绫罗纱衣、内搭同色刺绣中衣",
        "天青色罗裙、如诗如画",
        "浅蓝色纱衣、温柔恬静",
        "蓝白色汉服、清新淡雅、刺绣精美"
    ],
    "绿色": [
        "浅绿色襦裙、清新自然",
        "翠绿色汉服、生机盎然",
        "青绿色纱衣、雅致脱俗",
        "绿色系汉服、神秘、梦核"
    ],
    "青色": [
        "青色衣衫、素雅清秀、飘逸灵动",
        "天青色罗裙、如诗如画、温婉典雅",
        "青色纱衣、清冷出尘、超凡脱俗",
        "青碧色汉服、淡雅如水、古韵悠长"
    ],
    "紫色": [
        "紫色纱衣、神秘高贵、仙气飘飘",
        "紫霞色罗裙、华丽富贵、流光溢彩",
        "淡紫色汉服、清雅脱俗、温婉动人"
    ],
    "金色": [
        "金色华服、璀璨夺目",
        "金色刺绣汉服、华丽高贵",
        "金色纱衣、流光溢彩",
        "橘红色与金色相间的唯美华丽轻纱汉服、袖口宽大"
    ],
    "default": [
        "烟霞色蹙金绣罗裙、华丽精致、裙裾上苏绣的湘妃竹纹层层叠叠",
        "轻纱汉服、飘逸灵动、柔软布料衣物",
        "精美刺绣罗裙、层次丰富、刺绣精美",
        "魏晋风华丽交领大袖衫、柔软材质服装",
        "仙侠飘逸古装、衣袂飘飘",
        "南北朝服饰、南北朝头饰、柔软材质服装",
        "唯美华丽轻纱汉服、轻纱外披、袖口宽大",
        "精美繁复服饰配饰、高级感重工极繁细节服装"
    ]
}

# 朝代服装细节词库
DYNASTY_CLOTHING = {
    "汉代": [
        "汉代曲裾深衣、交领右衽、宽袖博带",
        "汉代直裾袍服、素雅端庄、衣长曳地",
        "汉代襦裙、上襦下裙、腰间系带",
        "汉代深衣、交领曲裾、典雅大气"
    ],
    "唐代": [
        "唐代齐胸襦裙、高腰设计、飘逸灵动",
        "唐代大袖衫、披帛飘逸、华丽富贵",
        "唐代圆领袍、胡风融入、开放大气",
        "唐代襦裙、色彩艳丽、绣花精美"
    ],
    "宋代": [
        "宋代褙子、对襟长衫、素雅清秀",
        "宋代襦裙、窄袖设计、端庄秀丽",
        "宋代大袖衫、披帛轻垂、温婉典雅",
        "宋代罗裙、刺绣精美、层次分明"
    ],
    "明代": [
        "明代袄裙、上袄下裙、端庄大方",
        "明代马面裙、褶皱精致、华丽典雅",
        "明代立领对襟衫、精致刺绣、贵气十足",
        "明代披风、大袖设计、雍容华贵"
    ],
    "清代": [
        "清代旗装、满族服饰、端庄典雅",
        "清代旗袍、修身剪裁、绣花精美",
        "清代氅衣、宽袖设计、华丽富贵",
        "清代花盆底鞋、旗头、满族特色"
    ],
    "魏晋": [
        "魏晋风交领大袖衫、飘逸洒脱、仙风道骨",
        "魏晋襦裙、宽衣博带、风流倜傥",
        "魏晋深衣、素雅清逸、名士风流"
    ],
    "南北朝": [
        "南北朝服饰、交领大袖、飘逸灵动",
        "南北朝襦裙、柔软材质、层次丰富",
        "南北朝深衣、素雅端庄、古韵悠长"
    ],
    "秦代": [
        "秦代深衣、交领右衽、庄重威严",
        "秦代曲裾袍、黑色为主、大气磅礴",
        "秦代襦裙、简洁大方、古朴典雅"
    ]
}

# 朝代发型词库
DYNASTY_HAIRSTYLE = {
    "汉代": ["汉代堕马髻、发髻低垂、优雅端庄", "汉代高髻、发髻高耸、典雅大气", "汉代垂云髻、发丝飘逸、柔美动人"],
    "唐代": ["唐代高髻、发髻高耸、华丽富贵", "唐代双环髻、双环高耸、俏皮灵动", "唐代云髻、发髻如云、雍容华贵"],
    "宋代": ["宋代包髻、发髻包起、端庄秀丽", "宋代朝天髻、发髻朝天、清新雅致", "宋代低髻、发髻低垂、温婉典雅"],
    "明代": ["明代狄髻、发髻高耸、端庄大方", "明代桃心髻、发髻如桃、甜美可人", "明代牡丹头、发髻如花、雍容华贵"],
    "清代": ["清代旗头、两把头、满族特色", "清代大拉翅、头饰华丽、端庄典雅", "清代架子头、发髻高耸、贵气十足"],
    "魏晋": ["魏晋发髻、飘逸洒脱、仙风道骨", "魏晋高髻、发丝灵动、风流倜傥"],
    "南北朝": ["南北朝发髻、交领大袖、飘逸灵动", "南北朝高髻、发髻精致、古韵悠长"],
    "秦代": ["秦代高髻、发髻高耸、庄重威严", "秦代垂髻、发髻低垂、古朴典雅"]
}

# 朝代发饰词库
DYNASTY_HEADPIECES = {
    "汉代": ["汉代步摇、金钗、玉簪", "汉代花钗、发簪精美、典雅大方"],
    "唐代": ["唐代花钗、金步摇、华丽富贵", "唐代发簪、珠翠满头、雍容华贵"],
    "宋代": ["宋代花簪、珠翠点缀、端庄秀丽", "宋代发钗、精致典雅、温婉动人"],
    "明代": ["明代花钗、点翠发簪、华丽富贵", "明代珠翠、发饰精美、雍容华贵"],
    "清代": ["清代旗头、钿子、流苏垂坠", "清代花盆底、满族发饰、特色鲜明"],
    "魏晋": ["魏晋发簪、简约飘逸、仙风道骨", "魏晋步摇、轻盈灵动、风流倜傥"],
    "南北朝": ["南北朝发簪、珠翠点缀、古韵悠长"],
    "秦代": ["秦代玉簪、金钗、古朴典雅", "秦代发饰、简洁大方、庄重威严"]
}

# 摄影风格词库（随机组合增加变化）
PHOTOGRAPHY_STYLES = [
    "胶片摄影，镜头语言，淡彩，个性视角",
    "胶片摄影，对焦模糊，过曝、高曝光、淡彩",
    "胶片摄影，镜头语言，暗调，氛围低光",
    "古风胶片摄影，镜头语言，淡彩，个性视角",
    "胶片摄影，镜头语言，朦胧美学，个性视角",
    "胶片摄影，对焦模糊，高曝，过曝，暗调，伦勃朗光，强烈明暗对比，高反差",
    "暗朦调，柔和七彩霞光，泛朦，胶片摄影，对焦模糊，强侧光，伦勃朗光",
    "胶片摄影，镜头语言，淡彩亮色，个性视角",
    "颓废治愈氛围，自然静谧气息，斑驳梦幻光影，呼吸感，梦核，流光溢彩，极致光影美学"
]

# 后期效果词库（随机组合）
POST_EFFECTS = [
    "层次丰富，写意，朦胧美学，光的美学，lomo效果，超现实，高级感，杰作",
    "胶片颗粒质感，层次丰富，写意，朦胧美学，光的美学，lomo效果，高级感，杰作",
    "叠加高斯模糊与动态模糊效果，层次丰富，写意，朦胧美学，lomo效果，超现实，杰作",
    "粒子高噪点，胶片颗粒质感，层次丰富，写意，朦胧美学，光的美学，高级感，杰作",
    "虚焦，既视感，情绪氛围感拉满，暗朦，光朦，胶片颗粒质感，层次丰富，杰作",
    "情绪氛围感拉满，暗朦，光朦，粒子高噪点，胶片颗粒质感，层次丰富，写意，朦胧美学，光的美学，lomo效果，超现实，高级感，杰作",
    "高颜值，高对比度，虚焦，既视感，情绪氛围感拉满，暗朦，光朦，胶片颗粒质感，层次丰富，写意，朦胧美学，光的美学，lomo效果，超现实，高级感，杰作"
]

# 镜头效果词库
LENS_EFFECTS = [
    "对焦模糊，高曝，过曝，暗调，伦勃朗光，强烈明暗对比，高反差",
    "动态模糊，虚焦，高亮高饱和色彩叙事，褪色记忆",
    "慢快门，朦胧美学，层次感，大师视角，高清渲染",
    "运动模糊，构图随意却尽显生活中的绚丽日常",
    "奇特视角，胶片颗粒感，慢快门，朦胧美学，层次感",
    "朦胧感+模糊感，超强模糊质感的摄影抓拍，周边的物体全部虚化",
    "半身构图，镜头近距离，近距离写真，逼真",
    "微距镜头，面部阴影，面部聚焦，丰富的细节",
    "正面照，超清晰画质，细节完美，绝美角度拍摄",
    "侧光，发丝轻飘，凌乱，随机角度拍摄",
    "电影级面光，光线追踪，网感脸，网感妆"
]

# 华丽风格词库
LUXURY_STYLES = [
    "高级感重工极繁细节服装，服装上带有精美绣花",
    "精美繁复服饰配饰，神秘，梦核，高级",
    "满头流苏装饰，层层叠叠，复杂精致，华丽璀璨",
    "奢华的配饰彰显独特品味，俏皮灵动的姿态",
    "发饰巧夺天工，各种精致步摇流苏，各种精致宝石点缀簪子，细小宝石链",
    "中式刺绣服饰，妆造精致，饰品精巧，细节精致",
    "华丽璀璨，奢华闪耀，瑰丽多彩，璀璨夺目，晶莹剔透，流光粒子，绚丽画风"
]

# 光影效果词库
LIGHT_EFFECTS = [
    "光影弥散，抽象表达，艺术氛围，情绪表达和叙事，超现实主义美学，高级的氛围感",
    "电影光线，朦胧，半透明纹理，哑光高级质感，动态柔光投影，朦胧发光层",
    "光影斑驳，浮光，出片姿势，超高清，魅力，最高画质，细腻渲染",
    "明暗对比，光影强烈，光影斑驳，浮光",
    "光线柔和自然，非均匀打光，表情自然松弛，照片毫无修饰感，带有生活真实感",
    "阳光透过发丝照在脸上，突出冷白皮通透自然的肌肤状态",
    "柔和光线笼罩整体，增添梦幻朦胧感"
]

# 皮肤质感词库
SKIN_TEXTURES = [
    "冷白皮，皮肤肌理清晰可见，十分美艳动人",
    "清透肌肤，瓷肌，高清32k，面部阴影，面部聚焦，空灵感",
    "皮肤白皙，底妆通透，肤色均匀自然，纯欲风",
    "冷白皮质感的哑光皮肤，皮肤质感，人物有最好的骨相",
    "白里透红的肌肤，妩媚诱人的表情",
    "肌肤如雪，卡姿兰大眼睛",
    "皮肤白皙嫩滑，倾国倾城容貌",
    "冷白皮，时尚穿搭，瓜子脸尖下巴，皮肤白皙，底妆通透",
    "细腻陶瓷水嫩肌肤，偏冷白皮，皮肤美白透亮",
    "冷白皮漫感质感的光滑皮肤，fairskin",
    "冷白皮气质美女，皮肤白皙，气质出众"
]

def analyze_input(user_input: str) -> Dict[str, List[str]]:
    """分析用户输入，提取语义类别"""
    detected = {
        "朝代": [],
        "气质类型": [],
        "人物": [],
        "肤色": [],
        "容貌": [],
        "表情": [],
        "发型": [],
        "发饰": [],
        "服装": [],
        "颜色": [],
        "配饰": [],
        "场景": [],
        "氛围": [],
        "动作": [],
        "道具": [],
        "胶片": [],
        "光影": [],
        "其他": []
    }

    # 收集所有词库中的关键词
    all_keywords_by_category = {}
    all_keywords = set()
    for category, data in SEMANTIC_CATEGORIES.items():
        if "keywords" in data:
            all_keywords_by_category[category] = data["keywords"]
            all_keywords.update(data["keywords"])

    # 用常见分隔符拆分用户输入
    import re as _re
    user_tokens = _re.split(r'[，,、。.！!？?\s；;：:""\'\'（）()]+', user_input)

    matched_keywords = set()

    for token in user_tokens:
        token = token.strip()
        if not token:
            continue

        # 对每个词组，找出所有能匹配的关键词（按长度降序，贪心匹配不重叠部分）
        token_remaining = token
        for category, keywords in all_keywords_by_category.items():
            for keyword in sorted(keywords, key=len, reverse=True):
                if keyword in token_remaining and len(keyword) >= 2 and keyword not in matched_keywords:
                    detected[category].append(keyword)
                    matched_keywords.add(keyword)
                    token_remaining = token_remaining.replace(keyword, "", 1)
        
        # 额外检查：如果token包含颜色词（如"红衣"包含"红"），单独识别颜色
        for color in ["红色", "粉色", "白色", "黑色", "蓝色", "绿色", "金色", "红", "粉", "白", "黑", "蓝", "绿", "金"]:
            if color in token and color not in matched_keywords:
                detected["颜色"].append(color)
                matched_keywords.add(color)

    # 收集用户输入中未被词库匹配到的词
    # 过滤掉常见的位置描述词（如"头上"、"身后"、"背景是"等）
    position_words = {"头上", "头上是", "身后", "身后是", "背景", "背景是", "手里", "手里是", "手中", "穿着", "戴着"}
    
    # 与古风主题不相关的词（黑名单）
    irrelevant_words = {
        # 现代科技
        "高压", "电压", "电力", "汽车", "手机", "电脑", "飞机", "火车", "地铁", "电梯",
        "空调", "冰箱", "电视", "网络", "互联网", "软件", "硬件", "程序", "代码",
        # 现代生活
        "上班", "下班", "打卡", "加班", "工资", "薪水", "公司", "企业", "银行",
        "股票", "基金", "投资", "理财", "保险", "贷款", "信用卡",
        # 现代物品
        "快递", "外卖", "超市", "商场", "便利店", "加油站", "停车场",
        # 现代概念
        "科技", "科学", "研究", "实验", "数据", "分析", "统计", "报告",
        # 其他不相关
        "电压", "电流", "电阻", "功率", "频率", "电压", "电池", "充电"
    }
    
    # 允许通过的未匹配词（白名单）- 这些词虽然不在词库中，但与古风主题相关
    allowed_words = {
        # 气质描述
        "明艳", "高冷", "高贵", "典雅", "优雅", "端庄", "秀丽", "清秀", "娇媚",
        "妩媚", "妖娆", "风情", "魅惑", "冷艳", "艳丽", "华贵", "雍容",
        # 表情神态
        "微笑", "忧郁", "忧伤", "哀愁", "淡然", "恬静", "温柔", "娇羞",
        "含笑", "浅笑", "嫣然", "莞尔", "恬淡", "从容", "慵懒", "俏皮",
        # 人物特征
        "美女", "佳人", "丽人", "绝色", "倾城", "国色", "天香", "绝世",
        # 服装风格
        "华丽", "精致", "繁重", "精美", "华丽", "纯欲", "洛丽塔",
        # 身材描述
        "婀娜", "娇小", "苗条",
        # 其他古风相关
        "飘逸", "洒脱", "灵动", "仙气", "出尘", "脱俗", "超凡", "江南"
    }
    
    unmatched = []
    for token in user_tokens:
        token = token.strip()
        if not token or len(token) < 2:
            continue
        if token in position_words:
            continue
        # 过滤掉与古风主题不相关的词
        if token in irrelevant_words:
            continue
        # 检查是否包含不相关的词，如果有则拆分处理
        filtered_token = token
        for irr in irrelevant_words:
            if irr in filtered_token:
                filtered_token = filtered_token.replace(irr, "")
        # 过滤后如果还有内容，继续处理
        if not filtered_token or len(filtered_token) < 2:
            continue
        # 如果过滤后的词在白名单中，直接添加
        if filtered_token in allowed_words:
            unmatched.append(filtered_token)
            continue
        is_covered = False
        for kw in matched_keywords:
            if kw in filtered_token and len(kw) >= 2:
                is_covered = True
                break
        if not is_covered:
            unmatched.append(filtered_token)

    detected["未匹配"] = unmatched

    return detected


def get_temperament_config(detected: Dict[str, List[str]], user_input: str) -> Dict[str, str]:
    """获取气质类型配置"""
    default_config = {
        "identity": "美人",
        "temperament": "高贵优雅感",
        "traits": ["妩媚", "迷人"]
    }

    if detected["气质类型"]:
        temperament_key = detected["气质类型"][0]
        if temperament_key in SEMANTIC_CATEGORIES["气质类型"]["mapping"]:
            return SEMANTIC_CATEGORIES["气质类型"]["mapping"][temperament_key]

    if "御姐" in user_input or "成熟" in user_input or "妩媚" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["御姐"]
    elif "甜妹" in user_input or "可爱" in user_input or "元气" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["甜妹"]
    elif "萝莉" in user_input or "软萌" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["萝莉"]
    elif "女王" in user_input or "霸气" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["女王"]
    elif "仙女" in user_input or "仙气" in user_input or "清冷" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["仙女"]
    elif "魔女" in user_input or "邪魅" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["魔女"]
    elif "妖女" in user_input or "妖艳" in user_input or "妖娆" in user_input:
        return SEMANTIC_CATEGORIES["气质类型"]["mapping"]["妖女"]

    return default_config


def generate_rich_prompt(detected: Dict[str, List[str]], user_input: str) -> str:
    """生成丰富、有变化的提示词"""
    
    # 获取气质类型
    temperament_config = get_temperament_config(detected, user_input)
    identity = temperament_config.get("identity", "美人")
    traits = temperament_config.get("traits", ["妩媚", "迷人"])
    
    # 获取对应的人物细节词库
    char_details = CHARACTER_DETAILS.get(identity, CHARACTER_DETAILS["default"])
    
    # 随机选择摄影风格
    photo_style = random.choice(PHOTOGRAPHY_STYLES)
    
    # 随机选择后期效果
    post_effect = random.choice(POST_EFFECTS)
    
    # 生成背景细节
    scene_key = detected["场景"][0] if detected["场景"] else "default"
    bg_options = BACKGROUND_DETAILS.get(scene_key, BACKGROUND_DETAILS["default"])
    background_detail = random.choice(bg_options)
    
    # 检测朝代
    dynasty = None
    if detected["朝代"]:
        dynasty_key = detected["朝代"][0]
        if dynasty_key in SEMANTIC_CATEGORIES["朝代"]["mapping"]:
            dynasty = SEMANTIC_CATEGORIES["朝代"]["mapping"][dynasty_key]
    
    # 生成人物细节
    face_detail = random.choice(char_details["face"])
    eyes_detail = random.choice(char_details["eyes"])
    skin_detail = random.choice(char_details["skin"])
    makeup_detail = random.choice(char_details["makeup"])
    
    # 表情描述：优先使用用户输入的情绪词
    # 检查用户输入中是否有情绪/表情相关词
    # 表情/情绪词（优先级高）
    expression_emotions = {
        "忧郁": "忧郁、哀愁、眼神深邃",
        "忧伤": "忧伤、哀愁、眼神忧郁",
        "哀愁": "哀愁、忧郁、眼神深邃",
        "垂泪": "垂泪、泪眼朦胧、楚楚动人",
        "落泪": "落泪、泪眼婆娑、楚楚可怜",
        "含泪": "含泪、泪光闪烁、楚楚动人",
        "哭泣": "哭泣、泪流满面、楚楚可怜",
        "微笑": "微笑、温柔、恬静",
        "娇媚": "娇媚、妩媚、风情万种",
        "妩媚": "妩媚、娇媚、风情万种",
        "清冷": "清冷、疏离、高冷",
        "高冷": "高冷、清冷、疏离",
        "冷艳": "冷艳、清冷、高贵",
        "灵动": "灵动、俏皮、活泼",
        "俏皮": "俏皮、灵动、可爱",
        "可爱": "可爱、俏皮、灵动",
        "甜美": "甜美、温柔、可爱",
        "慵懒": "慵懒俏皮、甜美氛围",
        "纯欲": "纯欲风、俏皮可爱、甜美氛围"
    }
    
    # 气质词（优先级较低）
    temperament_words = {
        "温柔": "温柔、恬静、微笑",
        "恬静": "恬静、温柔、淡然",
        "明艳": "明艳、娇艳、光彩照人",
        "高贵": "高贵、优雅、端庄",
        "优雅": "优雅、高贵、端庄",
        "端庄": "端庄、高贵、优雅",
        "绝世": "容颜绝美、独特韵味的美",
        "婀娜": "婀娜多姿、身材完美"
    }
    
    # 合并所有情绪词
    all_emotions = {**expression_emotions, **temperament_words}
    
    # 检查未匹配词中是否有表情/情绪词（优先匹配表情词）
    expression_detail = random.choice(char_details["expression"])
    user_emotion = None
    
    # 先检查表情/情绪词
    for word in detected.get("未匹配", []):
        if word in expression_emotions:
            user_emotion = word
            expression_detail = expression_emotions[word]
            break
    
    # 如果没有表情词，再检查气质词
    if not user_emotion:
        for word in detected.get("未匹配", []):
            if word in temperament_words:
                user_emotion = word
                expression_detail = temperament_words[word]
                break
    
    # 如果用户输入中直接包含情绪词
    if not user_emotion:
        for emotion in expression_emotions:
            if emotion in user_input:
                expression_detail = expression_emotions[emotion]
                break
        if not user_emotion:
            for emotion in temperament_words:
                if emotion in user_input:
                    expression_detail = temperament_words[emotion]
                    break
    
    # 发型：优先使用朝代特定发型
    if dynasty and dynasty in DYNASTY_HAIRSTYLE:
        hair_detail = random.choice(DYNASTY_HAIRSTYLE[dynasty])
    else:
        hair_detail = random.choice(char_details["hair"])
    
    # 服装细节：朝代服装与颜色结合
    if dynasty and dynasty in DYNASTY_CLOTHING:
        dynasty_clothing = random.choice(DYNASTY_CLOTHING[dynasty])
        # 如果有颜色，将颜色与朝代服装结合
        if detected["颜色"]:
            color_key = detected["颜色"][0]
            if color_key in SEMANTIC_CATEGORIES["颜色"]["mapping"]:
                color_key = SEMANTIC_CATEGORIES["颜色"]["mapping"][color_key]
            color_clothing = random.choice(CLOTHING_DETAILS.get(color_key, CLOTHING_DETAILS["default"]))
            clothing_detail = f"{color_clothing}，{dynasty_clothing}"
        else:
            clothing_detail = dynasty_clothing
    else:
        color_key = detected["颜色"][0] if detected["颜色"] else "default"
        if color_key in SEMANTIC_CATEGORIES["颜色"]["mapping"]:
            color_key = SEMANTIC_CATEGORIES["颜色"]["mapping"][color_key]
        clothing_options = CLOTHING_DETAILS.get(color_key, CLOTHING_DETAILS["default"])
        clothing_detail = random.choice(clothing_options)
    
    # 发饰描述：优先使用朝代特定发饰
    accessories_desc = ""
    if detected["发饰"]:
        head_items = []
        for acc in detected["发饰"]:
            if acc in ["簪花", "珍珠", "朱钗", "簪钗", "绒花", "步摇", "流苏", "玉簪", "宝石"]:
                head_items.append(acc)
        if head_items:
            accessories_desc = "头戴" + "、".join(head_items)
    elif dynasty and dynasty in DYNASTY_HEADPIECES:
        accessories_desc = random.choice(DYNASTY_HEADPIECES[dynasty])
    
    # 道具描述
    prop_desc = ""
    if detected["道具"]:
        if "团扇" in detected["道具"]:
            prop_desc = "手执团扇"
        elif "琵琶" in detected["道具"]:
            prop_desc = "手抱琵琶"
        elif "毛笔" in detected["道具"]:
            prop_desc = "手持毛笔"
        else:
            prop_desc = "手持" + detected["道具"][0]
    
    # 未匹配词
    unmatched_desc = ""
    if detected.get("未匹配"):
        unmatched_desc = "，".join(detected["未匹配"])
    
    # 随机选择镜头效果、华丽风格、光影效果
    lens_effect = random.choice(LENS_EFFECTS)
    luxury_style = random.choice(LUXURY_STYLES)
    light_effect = random.choice(LIGHT_EFFECTS)
    skin_texture = random.choice(SKIN_TEXTURES)
    
    # 组装完整提示词
    prompt_parts = []
    
    # 摄影风格
    prompt_parts.append(photo_style)
    
    # 人物细节（增加皮肤质感）
    person_detail = f"微距特写、{face_detail}、{identity}、{skin_texture}，黑色眼睛、{hair_detail}，{eyes_detail}、{expression_detail}，中式古风妆容、{makeup_detail}"
    if accessories_desc:
        person_detail += f"；{accessories_desc}"
    prompt_parts.append(f"\n- 人物细节：{person_detail}")
    
    # 服装细节（增加华丽风格）
    prompt_parts.append(f"\n- 服装细节：穿着{clothing_detail}，{luxury_style}")
    
    # 道具和动作
    if prop_desc:
        prompt_parts.append(f"\n- 动作：{prop_desc}")
    
    # 镜头效果
    prompt_parts.append(f"\n- 镜头效果：{lens_effect}")
    
    # 光影效果
    prompt_parts.append(f"\n- 光影效果：{light_effect}")
    
    # 未匹配词
    if unmatched_desc:
        prompt_parts.append(f"\n- 其他：{unmatched_desc}")
    
    # 整体呈现
    temperament = temperament_config.get("temperament", "高贵优雅感")
    prompt_parts.append(f"\n整体呈现{temperament}、一眼惊艳的构图")
    
    # 后期效果
    prompt_parts.append(f"\n{post_effect}")
    
    # 比例
    prompt_parts.append(" 比例9:16。")
    
    return "".join(prompt_parts)


def generate_prompt(user_input: str) -> str:
    """主函数：根据用户输入生成提示词"""
    # 分析输入
    detected = analyze_input(user_input)
    
    # 生成丰富提示词
    prompt = generate_rich_prompt(detected, user_input)
    
    return prompt.strip()


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        user_input = sys.stdin.read().strip()
    else:
        user_input = sys.argv[1]

    if not user_input:
        print("请输入描述关键词，例如：古风女妖艳红衣")
        sys.exit(1)

    prompt = generate_prompt(user_input)
    print(prompt)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 图片生成提示词生成器
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_prompt import generate_prompt, analyze_input


def test_basic():
    """测试基本功能"""
    print("=" * 50)
    print("测试1: 基本功能")
    print("=" * 50)
    
    test_cases = [
        "清代美女，甜美可爱",
        "魏晋红衣，忧郁",
        "绝世美女，垂泪，服饰华丽",
        "唐代，雍容华贵",
    ]
    
    for case in test_cases:
        print(f"\n输入: {case}")
        prompt = generate_prompt(case)
        print(f"输出:\n{prompt}\n")


def test_dynasty():
    """测试朝代识别"""
    print("=" * 50)
    print("测试2: 朝代识别")
    print("=" * 50)
    
    dynasties = ["汉代", "唐代", "宋代", "明代", "清代", "魏晋", "南北朝", "秦代"]
    
    for dynasty in dynasties:
        input_text = f"{dynasty}美女"
        detected = analyze_input(input_text)
        print(f"输入: {input_text} -> 识别朝代: {detected.get('朝代', [])}")


def test_emotion():
    """测试情绪识别"""
    print("\n" + "=" * 50)
    print("测试3: 情绪识别")
    print("=" * 50)
    
    emotions = ["忧郁", "甜美", "高冷", "妩媚", "垂泪", "微笑"]
    
    for emotion in emotions:
        input_text = f"美女，{emotion}"
        prompt = generate_prompt(input_text)
        # 检查是否包含情绪词
        has_emotion = emotion in prompt or any(e in prompt for e in ["忧郁", "哀愁", "甜美", "温柔", "高冷", "清冷", "妩媚", "垂泪", "微笑"])
        print(f"输入: {input_text} -> 情绪识别: {'✓' if has_emotion else '✗'}")


def test_color():
    """测试颜色识别"""
    print("\n" + "=" * 50)
    print("测试4: 颜色识别")
    print("=" * 50)
    
    colors = ["红衣", "粉色", "白色", "蓝色", "绿色", "金色", "青色"]
    
    for color in colors:
        input_text = f"美女，穿着{color}衣服"
        detected = analyze_input(input_text)
        print(f"输入: {input_text} -> 识别颜色: {detected.get('颜色', [])}")


def test_filter():
    """测试无关词过滤"""
    print("\n" + "=" * 50)
    print("测试5: 无关词过滤")
    print("=" * 50)
    
    # 包含现代词汇的输入
    input_text = "美女，高贵电压，忧郁"
    detected = analyze_input(input_text)
    print(f"输入: {input_text}")
    print(f"未匹配词: {detected.get('未匹配', [])}")
    print(f"预期: '高贵'保留，'电压'过滤")


if __name__ == "__main__":
    test_basic()
    test_dynasty()
    test_emotion()
    test_color()
    test_filter()
    print("\n" + "=" * 50)
    print("所有测试完成!")
    print("=" * 50)

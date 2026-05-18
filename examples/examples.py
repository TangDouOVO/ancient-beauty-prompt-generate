#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 图片生成提示词生成器
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_prompt import generate_prompt


def example_1():
    """示例1: 清代风格"""
    print("=" * 60)
    print("示例1: 清代风格 - 甜美可爱")
    print("=" * 60)
    
    prompt = generate_prompt("清代美女，头上有旗头，甜美可爱")
    print(prompt)


def example_2():
    """示例2: 魏晋风格"""
    print("\n" + "=" * 60)
    print("示例2: 魏晋风格 - 忧郁红衣")
    print("=" * 60)
    
    prompt = generate_prompt("魏晋美女，红衣，忧郁")
    print(prompt)


def example_3():
    """示例3: 垂泪美女"""
    print("\n" + "=" * 60)
    print("示例3: 垂泪美女 - 华丽服饰")
    print("=" * 60)
    
    prompt = generate_prompt("绝世美女，垂泪，服饰华丽，头上插满朱钗和簪花")
    print(prompt)


def example_4():
    """示例4: 宋代贵妇"""
    print("\n" + "=" * 60)
    print("示例4: 宋代贵妇")
    print("=" * 60)
    
    prompt = generate_prompt("宋朝，贵妇")
    print(prompt)


def example_5():
    """示例5: 青色衣衫"""
    print("\n" + "=" * 60)
    print("示例5: 青色衣衫 - 忧郁柔弱")
    print("=" * 60)
    
    prompt = generate_prompt("忧郁，柔弱、美女、青色衣衫的美女")
    print(prompt)


def example_6():
    """示例6: 团扇蝴蝶"""
    print("\n" + "=" * 60)
    print("示例6: 甜美可爱 - 团扇蝴蝶")
    print("=" * 60)
    
    prompt = generate_prompt("古风美女，甜美，绝美，甜美，可爱，拿着团扇，周围有蝴蝶")
    print(prompt)


if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
    example_6()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)

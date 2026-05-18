# Ancient Beauty Prompt Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

根据用户输入的古风关键词，生成高质量的AI图片生成提示词。支持朝代识别、情绪识别、颜色匹配等功能，输出比例固定为9:16。

## 功能特性

- 🎨 **智能语义匹配**：自动识别人物、服装、发饰、场景等关键词
- 🏛️ **朝代识别**：支持汉、唐、宋、明、清、魏晋、南北朝、秦等朝代
- 😊 **情绪识别**：支持忧郁、甜美、高冷、妩媚等多种表情
- 🎭 **气质类型**：御姐、甜妹、少女、萝莉、女王、仙女、魔女、妖女
- 🌈 **颜色匹配**：红、粉、白、黑、蓝、绿、金、青、紫、橙、黄
- 🎬 **丰富词库**：镜头效果、光影效果、皮肤质感、华丽风格
- 🚫 **智能过滤**：自动过滤与古风主题不相关的现代词汇

## 安装

### 方式一：直接克隆使用

```bash
git clone https://github.com/yourusername/ancient-beauty-prompt-generate.git
cd ancient-beauty-prompt-generate
python scripts/generate_prompt.py "你的关键词"
```

### 方式二：作为Python包安装

```bash
pip install -e .
```

## 使用方法

### 命令行

```bash
# 直接输入
python scripts/generate_prompt.py "清代美女，头上有旗头，甜美可爱"

# 通过管道
echo "魏晋美女，红衣，忧郁" | python scripts/generate_prompt.py
```

### Python API

```python
from image_prompt_generator import generate_prompt

# 生成提示词
prompt = generate_prompt("绝世美女，垂泪，服饰华丽，头上插满朱钗")
print(prompt)
```

## 示例输出

### 示例1：清代风格

**输入**：`清代美女，头上有旗头，甜美可爱`

**输出**：
```
胶片摄影，镜头语言，淡彩亮色，个性视角
- 人物细节：微距特写、娃娃脸、胶原蛋白满满、甜妹、冷白皮，时尚穿搭，瓜子脸尖下巴，皮肤白皙，底妆通透，黑色眼睛、清代旗头、两把头、满族特色，杏眼、眼神清澈、可爱、俏皮、灵动，中式古风妆容、清透妆容、元气满满；清代旗头、钿子、流苏垂坠
- 服装细节：穿着清代氅衣、宽袖设计、华丽富贵，华丽璀璨，奢华闪耀，瑰丽多彩，璀璨夺目，晶莹剔透，流光粒子，绚丽画风
- 镜头效果：微距镜头，面部阴影，面部聚焦，丰富的细节
- 光影效果：柔和光线笼罩整体，增添梦幻朦胧感
整体呈现甜美少女感、一眼惊艳的构图
情绪氛围感拉满，暗朦，光朦，粒子高噪点，胶片颗粒质感，层次丰富，写意，朦胧美学，光的美学，lomo效果，超现实，高级感，杰作 比例9:16。
```

### 示例2：魏晋风格

**输入**：`魏晋美女，红衣，忧郁`

**输出**：
```
古风胶片摄影，镜头语言，淡彩，个性视角
- 人物细节：微距特写、精致脸蛋、完美脸型、美人、肌肤如雪，卡姿兰大眼睛，黑色眼睛、魏晋发髻、飘逸洒脱、仙风道骨，明眸善睐、眼波流转、忧郁、哀愁、眼神深邃，中式古风妆容、清透妆容、气质出众
- 服装细节：穿着朱红色汉服、刺绣精美、袖口宽大，魏晋风交领大袖衫、飘逸洒脱、仙风道骨，高级感重工极繁细节服装，服装上带有精美绣花
- 镜头效果：朦胧感+模糊感，超强模糊质感的摄影抓拍，周边的物体全部虚化
- 光影效果：阳光透过发丝照在脸上，突出冷白皮通透自然的肌肤状态
- 其他：美女，明艳，高冷，高贵
整体呈现高贵优雅感、一眼惊艳的构图
叠加高斯模糊与动态模糊效果，层次丰富，写意，朦胧美学，lomo效果，超现实，杰作 比例9:16。
```

## 支持的朝代

| 朝代 | 服装示例 | 发型示例 | 发饰示例 |
|------|---------|---------|---------|
| 汉代 | 曲裾深衣、交领右衽 | 堕马髻、高髻 | 步摇、金钗、玉簪 |
| 唐代 | 齐胸襦裙、大袖衫 | 高髻、双环髻 | 花钗、金步摇 |
| 宋代 | 褙子、窄袖襦裙 | 包髻、低髻 | 花簪、珠翠 |
| 明代 | 袄裙、马面裙 | 狄髻、牡丹头 | 点翠发簪、珠翠 |
| 清代 | 旗装、旗袍 | 旗头、大拉翅 | 钿子、流苏 |
| 魏晋 | 交领大袖衫 | 飘逸发髻 | 简约发簪 |
| 南北朝 | 交领大袖 | 精致发髻 | 珠翠点缀 |
| 秦代 | 深衣、曲裾袍 | 高髻、垂髻 | 玉簪、金钗 |

## 项目结构

```
ancient-beauty-prompt-generate/
├── scripts/
│   └── generate_prompt.py    # 主脚本
├── references/
│   ├── keyword_library.md    # 关键词库文档
│   └── prompt_templates.md   # 模板文档
├── tests/
│   └── test_generator.py     # 测试文件
├── examples/
│   └── examples.py           # 使用示例
├── README.md                 # 项目说明
├── LICENSE                   # 许可证
├── setup.py                  # 安装配置
└── requirements.txt          # 依赖列表
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

[MIT License](LICENSE)
"# ancient-beauty-prompt-generate" 

#!/usr/bin/env python3
"""
Jack 叔叔 · 每日思想实验推送（带详细解说 + 打乱顺序）
每天自动从概念词典里选一个概念，推送到 钉钉/飞书/微信。
"""
import json, os, urllib.request, urllib.parse, datetime, random, sys

# ─── 加载概念 ───
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SCRIPT_DIR, "concepts_detailed.json"), encoding="utf-8") as f:
    concepts = json.load(f)

# ─── 选取今日概念（打乱顺序 + 按日期循环） ───
# 用日期做随机种子，保证同一天看到的永远是同一个概念
today = datetime.date.today()
random.seed(today.isoformat())
shuffled = concepts.copy()
random.shuffle(shuffled)

# 计算是第几天（从 2026-09-19 开始）
start_date = datetime.date(2026, 9, 19)
day_num = (today - start_date).days + 1
if day_num < 1:
    day_num = 1

# 用 day_num 取模来选概念（68个循环）
concept_index = (day_num - 1) % len(shuffled)
concept = shuffled[concept_index]

# ─── 构建消息（包含详细解说） ───
title = f"🧪 思想实验 · 第 {day_num} 天"

discipline = concept.get("discipline", "")
category_short = concept["category"].replace("心理学/行为经济学", "心理学").replace("数学/统计/概率", "数学").replace("物理/化学/生物", "科学").replace("经济学/社会", "经济").replace("人生方法论", "人生心法")

lines = [
    f"### 🧪 今天的思想实验 · 第 {day_num} 天",
    f"",
    f"**📖 概念：{concept['name']}**",
    f"",
]
if discipline and discipline != "—":
    lines.append(f"📚 分类：{discipline}")
    lines.append("")
lines.append(f"🏷️ 领域：{category_short}")
lines.append(f"")
lines.append(f"---")
lines.append(f"")
lines.append(f"💡 **{concept['insight']}**")
lines.append(f"")
lines.append(f"---")
lines.append(f"")
lines.append(f"**📖 这是什么？**")
lines.append(f"{concept['explanation']}")
lines.append(f"")
lines.append(f"**🌟 举个例子**")
lines.append(f"{concept.get('example', '生活中到处都能用这个概念...')}")
lines.append(f"")
lines.append(f"---")
lines.append(f"")
lines.append(f"🤔 **今日思考**：")
lines.append(f"今天你在哪件事上能用到「{concept['name']}」？")
lines.append(f"带着这个概念过今天，晚上打开 Obsidian 写下你的答案。")
lines.append(f"")
lines.append(f"---")
lines.append(f"📊 进度：第 {day_num} 天 / 68 个概念（每天随机打乱）")

text = "\n".join(lines)

# ─── 发送 ───
webhook = os.environ.get("WEBHOOK_URL", "").strip()
platform = os.environ.get("PUSH_PLATFORM", "dingtalk").strip().lower()

if not webhook:
    print("⚠️  未设置 WEBHOOK_URL，仅打印消息内容：")
    print("=" * 50)
    print(text)
    print("=" * 50)
    sys.exit(0)

print(f"推送平台：{platform}")
print(f"第 {day_num} 天概念：{concept['name']}")

try:
    if platform == "dingtalk":
        # 钉钉机器人
        data = json.dumps({
            "msgtype": "markdown",
            "markdown": {"title": title, "text": text},
            "at": {"isAtAll": False}
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=data,
            headers={"Content-Type": "application/json"})

    elif platform == "feishu":
        # 飞书机器人
        data = json.dumps({
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title}
                },
                "elements": [
                    {"tag": "markdown", "content": text}
                ]
            }
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=data,
            headers={"Content-Type": "application/json"})

    elif platform == "serverchan":
        # Server酱 → 微信
        data = urllib.parse.urlencode({
            "title": title,
            "desp": text
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=data)

    elif platform == "wecom":
        # 企业微信群机器人
        data = json.dumps({
            "msgtype": "markdown",
            "markdown": {"content": text}
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=data,
            headers={"Content-Type": "application/json"})

    else:
        print(f"❌ 不支持的平台：{platform}")
        sys.exit(1)

    resp = urllib.request.urlopen(req, timeout=30)
    result = resp.read().decode("utf-8")
    print(f"✅ 推送成功！")

except Exception as e:
    print(f"❌ 推送失败：{e}")
    sys.exit(1)
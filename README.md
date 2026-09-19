# 🧪 Jack 叔叔 · 每日思想实验推送

每天早上 8:00 自动把一个概念推送到你的手机（钉钉/飞书/微信），不需要开电脑。

## 工作原理

```
GitHub 云服务器（24小时运行）
  ↓ 每天北京时间 8:00
  读取 concepts.json（68个概念）
  ↓ 选今天的概念
  发送到你的 钉钉/飞书/微信
```

---

## 安装步骤（共 5 步）

### 第 1 步：选一个推送平台（三选一）

#### 🅰️ 钉钉（最简单）
1. 打开钉钉，随便建一个群（或用现有的群，只有你自己也行）
2. 群设置 → **智能群助手** → **添加机器人** → **自定义**
3. 机器人名字随便填（比如「思想实验」）
4. 安全设置选「自定义关键词」，填 `思想实验`（这样只有含这个词的消息能发）
5. **复制 webhook 地址**（形如 `https://oapi.dingtalk.com/robot/send?access_token=xxx`）
6. 记住你的平台名：`dingtalk`

#### 🅱️ 飞书
1. 打开飞书，建一个群（只有你自己也行）
2. 群设置 → **群机器人** → **添加机器人** → **自定义机器人**
3. 名字随便填
4. **复制 webhook 地址**（形如 `https://open.feishu.cn/open-apis/bot/v2/hook/xxx`）
5. 记住你的平台名：`feishu`

#### 🅲️ 微信（通过 Server酱）
1. 打开 [sct.ftqq.com](https://sct.ftqq.com)，用微信扫码登录
2. 关注「Server酱」公众号
3. 复制你的 **SendKey**（一串字母数字）
4. 你的 webhook 地址是：`https://sctapi.ftqq.com/send/你的SendKey.send`
5. 记住你的平台名：`serverchan`

---

### 第 2 步：注册 GitHub（如果已有账号跳过）

1. 打开 [github.com](https://github.com)
2. 点 **Sign up**，用邮箱注册（免费）
3. 验证邮箱

---

### 第 3 步：创建仓库并上传文件

1. 登录 GitHub，点右上角 **+** → **New repository**
2. 仓库名填：`jack-daily-push`
3. 选 **Public**（必须 Public，免费版才能定时运行）
4. 勾选 **Add a README file**
5. 点 **Create repository**

6. 进入仓库后，点 **Add file** → **Upload files**
7. 把这个文件夹里的 3 个文件拖进去：
   - `daily_push.py`
   - `concepts.json`
   - `.github/workflows/daily-push.yml`（这个需要先在仓库里建 `.github/workflows/` 文件夹）
8. 点 **Commit changes**

> 💡 最简单的方式：把 `daily_push.py` 和 `concepts.json` 直接拖上传。然后新建文件 `.github/workflows/daily-push.yml`，把内容粘贴进去。

---

### 第 4 步：添加密钥（最关键的一步）

1. 在仓库页面点 **Settings** → 左侧 **Secrets and variables** → **Actions**
2. 点 **New repository secret**，添加两个：

   **第一个：**
   - Name：`WEBHOOK_URL`
   - Value：你第 1 步复制的 webhook 地址
   
   **第二个：**
   - Name：`PUSH_PLATFORM`
   - Value：`dingtalk` 或 `feishu` 或 `serverchan`（根据你选的平台）

3. 两个都点 **Add secret** 保存

---

### 第 5 步：测试！

1. 在仓库页面点 **Actions** 标签
2. 左边选 **每日思想实验推送**
3. 点 **Run workflow** → **Run workflow**
4. 等几十秒，你的钉钉/飞书/微信应该收到一条消息！

收到消息就成功了 ✅ 之后每天早上 8:00 会自动推送。

---

## 常见问题

**Q: 没收到消息？**
- 检查 Actions 页面有没有报错（红色 ❌）
- 检查 Secrets 是否填对
- 钉钉检查关键词是否设为「思想实验」

**Q: 想改推送时间？**
- 编辑 `.github/workflows/daily-push.yml`
- `cron: "0 0 * * *"` 是北京时间 8:00
- 改成 `cron: "30 23 * * *"` = 北京时间 7:30（更早）
- 改成 `cron: "0 22 * * *"` = 北京时间 6:00

**Q: 概念用完了怎么办？**
- 68 个概念用完后会自动从头循环，但从不同角度再学一遍很有价值
- 想加新概念：编辑 `concepts.json`，加一条 `{"name": "新概念", "category": "...", "insight": "..."}`

**Q: GitHub 免费够用吗？**
- 完全够用。免费版每月 2000 分钟，每天跑 1 次只用 30 秒，绰绰有余。

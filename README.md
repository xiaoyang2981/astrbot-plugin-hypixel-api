# astrbot-plugin-hypixel-api

AstrBot 数据查询插件，支持 **Hypixel** 和 **BuGLand (布吉岛)** 双平台玩家数据查询。

## 安装

```bash
cd AstrBot/data/plugins
git clone https://github.com/xiaoyang2981/astrbot-plugin-hypixel-api.git
cd astrbot-plugin-hypixel-api
pip install -r requirements.txt
```

## 配置

在 AstrBot 管理面板 → 插件管理 →「Hypixel API」配置页中填写：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `api_key` | Hypixel API Key | [Hypixel Developer Dashboard](https://developer.hypixel.net/) |
| `bjd_token` | BuGLand Token | 游戏内大厅输入 `/openapi` 申领 |
| `ban_groups` | 黑名单群组 | 群号列表，一行一个 |
| `ban_users` | 黑名单用户 | 用户ID列表，一行一个 |

也可通过指令设置：
```
/hyp setkey <Hypixel API Key>
/hyp bjdkey <BuGLand Token>
/bjd setkey <BuGLand Token>
```

## 命令

### Hypixel 查询 (`/hyp` 或 `/hypixel`)

| 命令 | 说明 |
|------|------|
| `/hyp player <ID>` | 玩家基本信息（等级、UUID、Rank、Karma 等） |
| `/hyp bedwars <ID>` | 起床战争（胜场、FKDR、KDR、拆床、连胜等） |
| `/hyp skywars <ID>` | 空岛战争（胜场、K/D、Souls、Heads 等） |
| `/hyp arcade <ID>` | 街机游戏总览（总胜场、排行等） |
| `/hyp zombies <ID>` | 丧尸末日（击杀、爆头、各地图最佳回合等） |
| `/hyp party <ID>` | 小游戏派对（各小游戏胜场列表） |
| `/hyp blitz <ID>` | 布吉岛 Blitz 数据（走 BuGLand API） |

### BuGLand 布吉岛查询 (`/bjd`)

| 命令 | 说明 |
|------|------|
| `/bjd blitz <ID>` | Blitz 详细数据 |
| `/bjd bedwars <ID>` | 起床战争 |
| `/bjd skywars <ID>` | 空岛战争 |
| `/bjd player <ID>` | 玩家信息 |
| `/bjd <game> <ID>` | 通用游戏查询（支持 murder, thebridges, arcade 等） |

## 项目结构

```
astrbot-plugin-hypixel-api/
├── main.py                  # 命令路由
├── hypixel/
│   ├── __init__.py
│   ├── client.py            # Hypixel API 客户端
│   └── command.py           # Hypixel 命令处理器
├── bjd/
│   ├── __init__.py
│   ├── client.py            # BuGLand API 客户端
│   └── command.py           # BuGLand 命令处理器
├── _conf_schema.json
├── metadata.yaml
└── README.md
```

## 输出样式

纯文本格式输出，使用 Emoji 和 Unicode 排版。

## 依赖

- aiohttp

## 许可

MIT License

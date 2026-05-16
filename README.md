# astrbot-plugin-hypixel-api

AstrBot Hypixel 玩家数据查询插件，支持查询 Hypixel 玩家基本信息、BedWars、SkyWars 等游戏数据。

## 安装

### 通过 AstrBot 插件市场安装（推荐）

在 AstrBot 管理面板 -> 插件市场 中搜索 `hypixel-api` 安装。

### 手动安装

```bash
# 在 AstrBot 插件目录下
cd plugins
git clone https://github.com/<your-repo>/astrbot-plugin-hypixel-api.git
cd astrbot-plugin-hypixel-api
pip install -r requirements.txt
```

## 使用

### 1. 获取 Hypixel API Key

前往 [Hypixel Developer Dashboard](https://developer.hypixel.net/) 创建 API Key。

### 2. 设置 API Key

```
/hypixel setkey <你的API密钥>
```

### 3. 查询命令

| 命令 | 说明 |
|------|------|
| `/hypixel player <玩家ID>` | 查看玩家基本信息（等级、排名、登录时间等） |
| `/hypixel bedwars <玩家ID>` | 查看 BedWars 数据（胜场、FKDR、拆床等） |
| `/hypixel skywars <玩家ID>` | 查看 SkyWars 数据（胜场、K/D、Souls等） |
| `/hypixel` | 显示帮助信息 |

### 示例

```
/hypixel player Technoblade
/hypixel bedwars gamerboy80
/hypixel skywars SammyGreen
```

## 依赖

- Python >= 3.10
- aiohttp >= 3.9.0

## 许可

MIT License
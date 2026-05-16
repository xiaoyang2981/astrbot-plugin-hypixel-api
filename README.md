# astrbot-plugin-hypixel-api

AstrBot Hypixel 玩家数据查询插件，支持查询玩家基本信息、起床战争、空岛战争、街机游戏、丧尸末日、小游戏派对等数据，输出为自定义样式图片。

## 安装

### 通过 AstrBot 插件市场安装（推荐）

在 AstrBot 管理面板 -> 插件市场 中搜索 `hypixel-api` 安装。

### 手动安装

```bash
cd AstrBot/data/plugins
git clone https://github.com/xiaoyang2981/astrbot-plugin-hypixel-api.git
cd astrbot-plugin-hypixel-api
pip install -r requirements.txt
```

## 配置

### 方式一：WebUI 配置页

在 AstrBot 管理面板 -> 插件管理，找到「Hypixel API」，在配置页中填写 API Key。

### 方式二：指令设置

```
/hypixel setkey <你的API密钥>
```

API Key 前往 [Hypixel Developer Dashboard](https://developer.hypixel.net/) 获取。

## 命令

| 命令 | 说明 |
|------|------|
| `/hypixel player <ID>` | 玩家基本信息（等级、UUID、Karma、登录时间等） |
| `/hypixel bedwars <ID>` | 起床战争数据（胜场、FKDR、KDR、拆床、连胜等） |
| `/hypixel skywars <ID>` | 空岛战争数据（胜场、K/D、Souls、Heads等） |
| `/hypixel arcade <ID>` | 街机游戏总览（总胜场、回合数、热门小游戏排行） |
| `/hypixel zombies <ID>` | 丧尸末日数据（击杀、爆头、各地图最佳回合等） |
| `/hypixel party <ID>` | 小游戏派对数据（回合胜场、各小游戏胜场列表） |

## 示例

```
/hypixel player Technoblade
/hypixel bedwars gamerboy80
/hypixel skywars SammyGreen
/hypixel zombies Mortuus_Killer
```

## 输出样式

查询结果以自定义卡片图片形式输出（深色风格）。如果渲染引擎不可用，自动降级为纯文本输出。

## 依赖

- aiohttp

## 许可

MIT License

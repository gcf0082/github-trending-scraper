# GitHub Trending Scraper

采集 GitHub Trending 排行榜数据，存储到 SQLite 数据库，并提供 GitHub Pages 页面展示。

## 功能特性

- 采集 GitHub Trending 日榜、周榜、月榜
- 自动去重，合并三个榜单数据
- 记录项目创建时间和最近更新时间
- 每日自动执行（北京时间 19:00）
- GitHub Pages 页面展示最新 100 条数据

## 本地运行

```bash
pip install -r requirements.txt

# 采集数据并保存到数据库
python collect_all.py

# 导出当日数据到 datas/ 目录
python export_daily.py

# 导出最新100条数据（用于 GitHub Pages）
python export_latest.py

# 查看数据
python main.py
```

## 定时任务

项目已配置 GitHub Actions，每天北京时间 19:00 自动执行：

1. 采集数据并保存到 `github_trending.db`
2. 导出当日数据到 `datas/YYYY-MM-DD.json`
3. 导出最新100条到 `datas/latest.json`
4. 自动提交到仓库

## GitHub Pages

访问 [https://gcf0082.github.io/github-trending-scraper/](https://gcf0082.github.io/github-trending-scraper/) 查看最新 100 条记录。

启用方法：
1. 进入仓库 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "master"，目录选择 "/ (root)"

## 数据字段

每个项目包含以下字段：

| 字段 | 说明 |
|------|------|
| name | 项目名称 |
| description | 项目描述 |
| language | 编程语言 |
| stars | 总星数 |
| forks | 分支数 |
| today_stars | 今日新增星数 |
| url | 项目链接 |
| created_at | 创建时间 |
| updated_at | 最近更新时间 |
| fetched_at | 采集时间 |

## 项目结构

```
├── collect_all.py      # 采集所有榜单数据
├── export_daily.py     # 导出当日数据
├── export_latest.py   # 导出最新数据
├── main.py            # 命令行查看
├── scraper.py         # 爬虫核心
├── index.html        # GitHub Pages 页面
├── github_trending.db # SQLite 数据库
└── datas/             # 每日数据目录
    ├── latest.json
    └── YYYY-MM-DD.json
```

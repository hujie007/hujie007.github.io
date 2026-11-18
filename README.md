# Jie Hu — 可自行维护的学术主页

这是已经填入 Jie Hu 信息的个人主页，采用参考 **Huiyuan Wang 学术主页**的左侧个人信息、右侧内容布局。主页包含 News，Research 分为三个可点击的方向，每个方向都有独立论文页面。保留了较大的字号、手机显示、论文搜索、BibTeX 下载、CV 和照片替换功能。

你维护的是普通 Markdown 和 YAML 文件。日常修改不需要改 HTML，不需要安装 Ruby，也不依赖本次聊天。第一次放进你自己的 GitHub 仓库并启用 Pages 后，GitHub 会自动构建和发布后续修改。

## 你的正式主页

- 公开主页：https://hujie007.github.io/
- 修改入口：https://github.com/hujie007/hujie007.github.io
- 日常更新：打开下面对应的文件，点铅笔修改，再点 **Commit changes** 保存。GitHub Actions 会自动更新网站。

## 最常用的文件

| 想修改什么 | 修改哪个文件 |
| --- | --- |
| 姓名、职称、邮箱、学校、Scholar 链接、求职提示 | `site.yml` |
| 首页个人介绍 | `content/about.md` |
| Research 总介绍 | `content/research.md` |
| 三个研究方向的标题、简述和关键词 | `data/research.yml` |
| Transfer Learning 分类介绍 | `content/research-transfer.md` |
| Federated Learning 分类介绍 | `content/research-federated.md` |
| Statistical Learning 分类介绍 | `content/research-inference.md` |
| 期刊审稿服务 | `content/service.md` |
| 论文、作者、期刊、审稿状态、论文链接 | `data/publications.yml` |
| 首页 News | `data/news.yml` |
| 教学和教育经历 | `content/teaching.md` |
| 报告和会议 | `content/talks.md` |
| 软件和代码链接 | `data/software.yml` |
| CV 文件 | 替换 `assets/pdf/Jie_Hu_CV.pdf`，文件名保持不变 |
| 照片 | 替换 `assets/img/jie-hu.jpg`，文件名保持不变 |
| 主题色 | `site.yml` 中的 `accent_color` |
| 深入修改字体、间距、布局 | `assets/css/jie-hu.css`（使用 rem 字号，兼顾电脑和手机） |

**不要直接编辑 `dist/`。** 它是自动生成的网站，下一次构建会根据上面的源文件重新生成。

## 第一次放到你的 GitHub

### 方法 A：只使用 GitHub 网页

1. 登录你的 GitHub，新建一个仓库。仓库名填 **`你的GitHub用户名.github.io`**，把这里的中文替换成真实用户名。个人主页一般使用公开仓库；普通公开主页的访客不需要登录。
2. 解压源码包，进入 `Jie_Hu_Academic_Website` 文件夹。将**文件夹里面的内容**上传到仓库根目录，不能再套一层同名目录。根目录应该直接看到 `site.yml`、`content/`、`data/`、`scripts/`、`assets/`、`requirements.txt` 等。
3. 确认 `.github/workflows/deploy.yml` 也上传了。它是一个隐藏文件夹里的发布配置；Mac Finder 可按 **Command + Shift + .** 显示隐藏文件。
4. 如果网页上传时漏了这个隐藏文件，可以在仓库选择 **Add file → Create new file**，文件名填 `.github/workflows/deploy.yml`，把本源码包中 `GITHUB_PAGES_WORKFLOW.yml` 的全部内容复制进去，然后保存。
5. 在仓库进入 **Settings → Pages**，将 **Source** 设置为 **GitHub Actions**。
6. 打开仓库的 **Actions**，找到 **Build and deploy academic website**。如果之前没有成功发布，可点击 **Run workflow** 再运行一次。等它完成后，Pages 设置里会显示你的网站地址。

本仓库已经使用你的 GitHub 账号 `hujie007`，仓库名为 `hujie007.github.io`。首次配置步骤仅供迁移或另建网站时参考。

### 方法 B：使用 Git / GitHub Desktop

也可以把源码包内容放入你自己的本地仓库，提交并推送到 `main`，再按上面的第 5–6 步开启 Pages。源码包已经包含自动发布配置；无需手动上传 `dist/`。

## 以后怎么改文字

例如更新个人介绍：

1. 在你的 GitHub 仓库点开 `content/about.md`。
2. 点铅笔图标（Edit file）。
3. 修改英文文字；可点 **Preview** 预览 Markdown。
4. 点 **Commit changes** 保存。可直接提交到自己的发布分支；如果仓库设置要求走分支，就提交并合并到发布分支。
5. 等 Actions 构建完成，再刷新你的主页。发布通常需要几分钟。

**你只需要修改文件和保存，发布由工作流处理。** GitHub 上的 Markdown Preview 主要用于检查文字格式；完整的网站排版以发布后页面为准。

## 添加一篇论文

在 `data/publications.yml` 最后复制一个完整条目，修改内容。每篇论文的 `id` 必须不同；目前已用 1–28，可以从 29 开始。

```yaml
- id: 29
  title: 'Your new paper title'
  authors: 'Jie Hu, Coauthor Name, Yong Chen*'
  year: 2027
  venue: ''
  status: 'Working papers'
  topic: 'Transfer learning'
  areas: ['transfer']
  selected: false
  url: ''
  code: ''
  pdf: ''
  detail: 'Submitted'
```

- `status` 只使用三种之一：`Published & accepted`、`Under revision`、`Working papers`。
- `selected: true` 表示加入 Publications 页面中的 Selected 筛选。
- `areas` 决定论文自动出现在哪些 Research 分类页：`transfer`、`federated`、`inference`。例如 `areas: [transfer, federated]` 会同时显示在两个方向。
- 三个分类页从同一份论文数据生成，无需重复录入文章，也无需手动修改分类论文数。
- `venue` 是正式发表或接收的期刊名；未发表时可以留空。
- `url` 填文章页面、DOI 或 arXiv 的完整 `https://...` 链接。
- `code` 填代码仓库的完整链接，没有就留空。
- `pdf` 可填 PDF 完整网址；或者先把 PDF 上传到 `assets/pdf/`，再填 `assets/pdf/YourPaper.pdf`。
- `detail` 可填 `In press`、`Minor revision` 或卷期页码。
- `topic` 可沿用现有主题，也可以添加新主题。筛选选项和论文数会自动更新。
- 作者写成英文正常顺序，用逗号分开；`†` 表示共同第一作者，`*` 表示通讯作者。你的姓名会自动加粗。

YAML 用空格缩进，不能用 Tab。如果题目含冒号等符号，请像例子一样用引号包起来。字符串里如果有单引号，可以用双引号包住整段文字。

## 更新 News

在 `data/news.yml` 最上面添加条目。`category`、`title`、`text`、`url` 都保留；没有链接时把 `url` 设为 `''`。`text` 支持 Markdown，包括加粗、斜体和链接。

```yaml
- date: 'Jan. 2027'
  category: 'Accepted'
  title: 'Paper title accepted by Journal Name'
  text: 'A brief description of the work.'
  url: 'publications/#paper-29'
```

## 更新 CV、照片和求职提示

- 更新 CV：上传新 PDF，并替换相同路径 `assets/pdf/Jie_Hu_CV.pdf`。
- 更新照片：上传新 JPG，并替换相同路径 `assets/img/jie-hu.jpg`。如果换成 PNG，需同时改 `site.yml` 的 `portrait` 路径。
- 关闭求职提示：在 `site.yml` 将 `job_market: true` 改成 `job_market: false`。
- 改颜色：把 `accent_color` 改成另一个六位颜色，例如 `'#416b91'`。保留引号和 `#`。
- 更新日期：修改 `site.yml` 中的 `updated`，例如 `'January 2027'`。
- GitHub 链接：`site.yml` 的 `github` 已填写为 `https://github.com/hujie007`；可自行修改或清空。

## 如果 Actions 构建失败

先在仓库的 **Actions → 对应的运行记录 → Build website** 查看错误。常见原因是 YAML 缩进、重复论文 id、写错 `status`，或 PDF 路径与实际文件不一致。修正源文件后再提交即可。

`site.yml` 和 `data/` 都经过构建检查；构建或链接检查未通过时，该次工作流不会替换线上版本。

## 在电脑上预览（可选）

安装 Python 3.12 后，在源码文件夹运行：

```bash
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --directory dist
```

然后打开 `http://localhost:8000/`。修改源文件后再运行一次 `python scripts/build.py` 并刷新浏览器。

## 版本与来源

- 当前网站内容以用户提供的 November 2026 CV 和 Penn 个人介绍为依据。
- Google Scholar 使用用户提供的链接；未抓取引用量或 h-index。
- 初版模板来源和 MIT 许可见 `THIRD_PARTY_NOTICES.md` 与 `LICENSE`。复制或分发模板时保留它们。
- 当前页面为独立编写的 Python + Markdown + YAML 模板，视觉参考 Huiyuan Wang 的学术主页；它不是 Jekyll、AcademicPages 或 al-folio 的未经修改的发行版。
- 原有版本的 MIT 许可文件保留；来源和布局变更见 `THIRD_PARTY_NOTICES.md`。
- Service 页面按用户提供的信息列出 IJOC、JASA、JMVA 审稿服务；未添加年份、次数或荣誉。
- 不包含其他学者的照片、CV 或个人文稿。
- 源码包不包含 ChatGPT 的项目标识、访问配置、登录信息或密钥。
- 当前 ChatGPT 预览与未来的 GitHub Pages 是两个独立部署。建立自己的 GitHub 仓库后，以它作为日常维护入口；修改该仓库不会自动同步到旧的 ChatGPT 预览网址。

## 官方操作文档

- GitHub 网页编辑文件：https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
- GitHub Pages 入门：https://docs.github.com/en/pages/quickstart
- GitHub Actions 发布 Pages：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

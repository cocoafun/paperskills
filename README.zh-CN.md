# PaperSkills

面向 AI Agents 的学术技能集。  
PaperSkills 为 Claude Code、Cursor、Codex 等 agent/coding assistant 提供一组可复用的学术工作流技能，帮助研究者在论文选题、文献检索、研究缺口分析、摘要生成、引文核验、同行评审、期刊匹配、论文追踪等环节更高效地使用 AI。

项目主页：<https://www.paperskills.com/>

## 为什么做这个项目

很多研究者已经感受到 AI 的帮助，但真正进入论文工作流时，常常还是会卡住：一个选题怎么继续收敛，一组文献怎么快速理清脉络，一篇草稿怎么系统地查缺补漏，一批引用又该怎么逐条核验。

很多时候，真正缺少的不是工具本身，而是一套可以直接拿来用的研究流程。

PaperSkills 想做的，就是把这些高频、具体、反复出现的学术任务，整理成一组面向 agent 的 research skills。你不需要从零组织步骤，也不需要每次重新设计流程；可以直接把任务交给 Claude Code、Cursor、Codex 这类 agent，让它们按更清晰的结构完成检索、分析、评审、核验和追踪。

它的目标很简单：让 AI 不只是“聊得不错”，而是真的能在论文研究和写作过程中帮你省时间、补盲点、提高质量。

## 适合谁使用

PaperSkills 适合：

- 本科生、硕士生、博士生
- 青年教师与科研工作者
- 需要频繁阅读、整理、撰写论文的研究人员
- 希望把 Claude Code、Cursor、Codex 等 agent 能力真正接入学术工作流的人

## 这个项目的作用

PaperSkills 不是单纯提供几个 prompt，而是把常见的学术任务整理成一组可复用的 agent skills。

它可以帮助你：

- 从模糊想法收敛出更具体的研究问题与论文标题
- 快速检索和整理相关文献
- 识别研究缺口
- 生成更符合学术写作要求的摘要
- 核验引用是否真实、准确、可追溯
- 对草稿进行结构化同行评审
- 匹配更合适的投稿期刊
- 持续追踪相关方向的新论文

换句话说，PaperSkills 想做的是：

**把学术研究中那些重复、耗时、但又高度结构化的环节，沉淀为 agent 可以直接调用的 research skills。**

## 安装

### Claude Code

#### 全局安装（所有项目可用）

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.claude/skills/paperskills
cd ~/.claude/skills/paperskills && ./setup
```

#### 单项目安装

```bash
mkdir -p .claude/skills
ln -s /path/to/paperskills .claude/skills/paperskills
cd .claude/skills/paperskills && ./setup
```

`./setup` 会创建诸如 `.claude/skills/peer-review`、`.claude/skills/shared` 之类的同级链接，以便生成报告类技能读取共享模板。更新 PaperSkills 后，建议重新执行一次 `./setup`。

### Cursor

Cursor 当前不会原生自动发现 `SKILL.md`。较实用的接入方式，是把 PaperSkills 作为项目内 prompt library 使用，并通过 Cursor Rules 指向安装说明。

可直接告诉 Cursor：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.cursor/INSTALL.md
```

或者手动参考仓库中的 [`.cursor/INSTALL.md`](.cursor/INSTALL.md)。

### Codex

可直接告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

或者手动安装：

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.agents/skills/paperskills
cd ~/.agents/skills/paperskills && ./setup
```

`./setup` 同样会链接生成报告类技能所需的共享资源目录。

## 可用技能

| Skill               | 说明                                               | Token Budget |
| ------------------- | ------------------------------------------------ | ------------ |
| `/topic-framing`    | 将模糊想法收敛为更具体的研究问题与论文标题                            | 15–25K       |
| `/lit-search`       | 跨 Semantic Scholar、OpenAlex、PubMed、arXiv 等进行文献检索 | 15–25K       |
| `/abstract`         | 生成多种格式的摘要（IMRaD、thematic、extended、short）         | 10–20K       |
| `/cite-verify`      | 基于 CrossRef / Semantic Scholar / OpenAlex 核验引文   | 25–65K       |
| `/citation-network` | 构建引用网络，并生成交互式 HTML 报告                            | 35–55K       |
| `/research-gap`     | 从时间、方法、主题、应用等维度分析研究缺口                            | 55–85K       |
| `/peer-review`      | 对论文草稿进行结构化同行评审，并支持评分与图表展示                        | 35–60K       |
| `/paper-tracker`    | 在指定时间窗口内追踪作者、期刊、会议、关键词、机构的新论文                    | 15–30K       |
| `/journal-match`    | 为论文推荐更合适的目标投稿期刊                                  | 25–35K       |

## 使用方式

你可以直接调用具体技能：

```text
/cite-verify my-manuscript.md
/peer-review draft.md
/lit-search 大模型支持文献综述写作
/paper-tracker track new Nature papers in the last month
```

也可以通过路由入口统一分发：

```text
/paperskills 帮我检索关于大模型支持文献综述写作的文献
```

## 语言支持

报告生成类技能支持中英文输出，包括：

* `cite-verify`
* `citation-network`
* `journal-match`
* `research-gap`
* `peer-review`
* `paper-tracker`

系统会根据论文内容自动判断输出语言，也可以显式指定，例如：

```text
用中文生成报告
```

## 推荐工作流

这些技能可以串联使用，形成一条更完整的学术工作流：

1. `/topic-framing` → 从模糊想法收敛出研究问题
2. `/lit-search` → 检索相关文献
3. `/research-gap` → 识别研究缺口
4. `/peer-review` → 对草稿进行结构化评审
5. `/cite-verify` → 在投稿前核验全部引用
6. `/paper-tracker` → 持续追踪相关方向的新论文


## 灵感来源

PaperSkills 的部分灵感和素材来源于以下开源项目，特别感谢：

- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code)

它们在 AI 学术写作、研究技能整理与 agent 工作流方面提供了重要启发。

## License

MIT

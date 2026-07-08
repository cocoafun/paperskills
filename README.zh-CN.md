# PaperSkills

面向 AI Agents 的开源学术技能库。  
PaperSkills 为 Claude Code、Cursor、Codex 等 agent / coding assistant 提供一组可复用、可组合、可扩展的学术工作流技能，帮助研究者把 AI 真正接入论文研究与写作过程，而不只是把它当成一个聊天工具。

项目主页：<https://www.paperskills.com/>

## 项目定位

PaperSkills 想做的，不是再增加一批零散 prompt，而是建设一套面向学术场景的开源基础设施：

- 把高频、重复、结构化的研究任务沉淀成可调用的 skills
- 让不同 agent 能以一致方式接入论文工作流
- 让技能可以组合，而不是一次性使用
- 让社区可以持续补充新的研究任务、模板、报告格式和路由逻辑

如果把 AI 在科研中的使用拆开来看，真正有价值的往往不是“单次回答得像不像人”，而是它能不能稳定地完成一段工作流。  
PaperSkills 关注的正是这件事：把论文选题、文献检索、研究缺口分析、摘要生成、引文核验、同行评审、期刊匹配、论文追踪等环节，变成 agent 可以直接执行的能力模块。

## 为什么做这个项目

很多研究者已经感受到 AI 的帮助，但真正进入论文工作流时，常常还是会卡住：

- 一个模糊选题怎么继续收敛
- 一组文献怎么快速理清脉络
- 一篇草稿怎么系统地查缺补漏
- 一批引用怎么逐条核验真假与完整性
- 一个方向怎么持续追踪最新论文

很多时候，真正缺少的不是模型本身，而是一套可以直接落地的研究流程。

PaperSkills 的目标很明确：

**把学术研究中那些重复、耗时、但又高度结构化的环节，沉淀为 agent 可以直接调用的 research skills。**

这样你不需要每次从零设计步骤，也不需要反复组织 prompt；可以直接把任务交给 Claude Code、Cursor、Codex 这类 agent，让它们按更清晰的结构完成检索、分析、评审、核验和追踪。

具体来说，PaperSkills 希望解决的是这些常见问题：

- 从模糊想法收敛出更具体的研究问题与论文标题
- 快速检索和整理相关文献
- 识别研究缺口
- 生成更符合学术写作要求的摘要
- 核验引用是否真实、准确、可追溯
- 对草稿进行结构化同行评审
- 匹配更合适的投稿期刊
- 持续追踪相关方向的新论文

换句话说，PaperSkills 试图提供的是一层“学术工作流能力层”，让 agent 在科研任务上更稳定、更可复用、更接近真实可交付的工作方式。

## 适合谁使用

PaperSkills 适合：

- 本科生、硕士生、博士生
- 青年教师与科研工作者
- 需要频繁阅读、整理、撰写论文的研究人员
- 希望把 Claude Code、Cursor、Codex 等 agent 真正接入学术工作流的人
- 希望构建学术 AI 工作流、并愿意参与开源共建的开发者

## 设计原则

为了把这个项目做成一个长期可维护的开源项目，PaperSkills 当前遵循几条很明确的设计原则：

- `Skill-first`：每个 skill 只解决一个清晰问题，降低理解和维护成本
- `Agent-native`：优先适配 Claude Code、Cursor、Codex 这类原生 agent 使用方式
- `Composable`：技能既可以单独使用，也可以串成完整工作流
- `Open stack`：尽量基于公开可访问的数据源和透明流程构建
- `Practical over fancy`：优先解决真实研究流程中的高频问题，而不是堆叠概念
- `Readable by humans`：既方便 agent 调用，也方便研究者和贡献者直接阅读、修改、扩展

## 当前支持的生态

PaperSkills 目前面向以下 agent 生态提供接入方式：

- Claude Code：支持原生 skills 安装
- Codex：支持原生 skills 安装
- Cursor：通过项目规则与 prompt library 方式接入

这意味着 PaperSkills 的目标不是绑定单一平台，而是尽可能成为一套跨 agent 的学术技能标准化仓库。

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

`./setup` 会创建诸如 `.claude/skills/peer-review` 之类的同级链接，便于各个子技能被 agent 原生发现。更新 PaperSkills 后，建议重新执行一次 `./setup`。

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

`./setup` 同样会链接各个子技能目录，便于 Codex 原生发现与调用。

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

## 推荐工作流

这些技能可以串联使用，形成一条更完整的学术工作流：

1. `/topic-framing` → 从模糊想法收敛出研究问题
2. `/lit-search` → 检索相关文献
3. `/research-gap` → 识别研究缺口
4. `/peer-review` → 对草稿进行结构化评审
5. `/cite-verify` → 在投稿前核验全部引用
6. `/paper-tracker` → 持续追踪相关方向的新论文

## 语言支持

报告生成类技能支持中英文输出，包括：

- `cite-verify`
- `citation-network`
- `journal-match`
- `research-gap`
- `peer-review`
- `paper-tracker`

系统会根据论文内容自动判断输出语言，也可以显式指定，例如：

```text
用中文生成报告
```

## 项目结构

当前仓库大致由以下部分组成：

- `SKILL.md`：项目级路由入口
- `skills/`：各个独立学术技能
- `assets/`：项目资源文件
- `artifacts/`：产物与示例输出目录
- `.codex/`：Codex 集成说明
- `.cursor/`：Cursor 集成说明
- `setup`：安装后自动注册链接

这种结构的目标很直接：让仓库既能作为“使用中的技能库”，也能作为“可持续扩展的开源代码库”。

## 开源协作方向

如果你也希望把这个项目做成一个真正可扩展的大型开源项目，PaperSkills 欢迎以下方向的贡献：

- 新的学术技能：例如综述生成、方法比较、审稿回复、实验设计辅助等
- 新的数据源接入：例如更多公开论文数据库、期刊目录、机构库
- 更稳定的报告模板与评估标准
- 更好的路由逻辑、任务分解方式与跨 skill 协同
- 更多 agent 平台的适配与安装方式
- 中英文文档、案例、教程与 benchmark

如果你在实际研究中反复遇到某个任务，而它又适合被结构化、复用、自动化，这类问题就很适合被沉淀成新的 PaperSkills skill。

## 灵感来源

PaperSkills 的部分灵感和素材来源于以下开源项目，特别感谢：

- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code)

它们在 AI 学术写作、研究技能整理与 agent 工作流方面提供了重要启发。

## License

MIT

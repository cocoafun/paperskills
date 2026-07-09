# PaperSkills

<p align="center">
  <img src="./logo-readme.png" alt="PaperSkills logo" width="120" />
</p>

面向 AI Agent 的场景化学术工作流技能工具箱。

[English](./README.md) | [项目主页](https://www.paperskills.com/)

## PaperSkills 是什么

PaperSkills 帮助研究者在真实科研流程中判断：**现在该用哪些 AI-agent skills，如何安装，第一条 prompt 怎么写，应该得到什么结果，下一步如何推进。**

它不是单纯的 prompt 合集，也不再只是一个独立 skill 仓库。当前项目由两层组成：

- Skill 分发层：把学术 skills 安装到 Claude Code、Codex、Cursor、OpenCode 等 agent 环境中。
- 科研场景层：从用户当前科研处境出发，推荐 skill 组合、可复制 prompt、预期输出和后续动作。

一句话说：

**PaperSkills 想把 AI Agent 的科研工作流变得可安装、可理解、可真正用于论文工作。**

## 从科研场景开始

PaperSkills 的入口不应该是“这里有一堆 skill，请自己猜怎么组合”，而应该是“你现在处在哪一步”：

| 当前场景 | 推荐工作流 |
| --- | --- |
| 我刚进入一个新领域，需要快速建立判断力 | `/lit-search` + `/citation-network` + `/research-gap` + `/paper-tracker` |
| 我有兴趣方向，但还没有可投稿的问题 | `/topic-framing` + `/research-gap` + `/lit-search` |
| 我要把文献和 PDF 整理成证据 | 文献综述 + PDF 精读 + `/cite-verify` + 可视化技能 |
| 我已经有论文草稿，需要投稿前体检 | `/abstract` + `/peer-review` + `/cite-verify` + `/journal-match` |
| 我要选择投稿期刊 | `/journal-match` + `/peer-review` + `/abstract` + `/cite-verify` |
| 我要做期刊级图表或科研展示产物 | 科学可视化、图组叙事、web artifact 技能 |
| 我想把课题组流程沉淀成自定义 agent | skill 创建、自定义、学习路径、自我审计技能 |

结构化场景目录见 [`registry/scenarios.json`](./registry/scenarios.json)，skill packs 见 [`registry/packs.json`](./registry/packs.json)。

## 当前核心技能

PaperSkills core package 目前维护这些论文工作流技能：

| Skill | 作用 |
| --- | --- |
| `/topic-framing` | 把宽泛兴趣收束成可研究、可投稿、可执行的论文题目 |
| `/lit-search` | 跨公开学术 API 检索文献，并按主题、证据和相关性整理 |
| `/research-gap` | 从文献和现有讨论中提炼真实研究缺口与贡献空间 |
| `/citation-network` | 梳理关键论文、作者、主题和引用关系，建立领域地图 |
| `/abstract` | 把研究问题、方法、发现和贡献压缩成清晰摘要 |
| `/peer-review` | 模拟学术审稿，识别结构、证据、贡献和投稿风险 |
| `/cite-verify` | 核验引用是否支撑原文论断，减少错引和过度引用 |
| `/journal-match` | 根据论文主题、方法、贡献和风险匹配目标期刊 |
| `/paper-tracker` | 持续追踪主题、作者、期刊和关键词，维护可复用论文监测清单 |

同时，registry 可以引用外部精选 skills 或未来扩展 skills，用于更完整的场景包，例如文献综述、PDF 精读、科学可视化、图组叙事、计算基础设施和领域建模工作流。

## 使用示例

可以直接调用具体 skill：

```text
/topic-framing 我想研究大模型辅助文献综述写作，请帮我收敛成可投稿的研究问题。
/lit-search 检索 AI-assisted systematic literature review 方向近五年和高被引核心论文。
/peer-review draft.md 请按期刊审稿标准评估这篇论文，并按优先级列出修改风险。
/cite-verify draft.md 请核验文中引用是否真实支撑对应论点。
```

也可以使用统一路由入口：

```text
/paperskills 我刚进入 AI 搜索广告这个领域，请帮我选择合适的研究工作流。
```

## 安装

### Claude Code

全局安装：

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.claude/skills/paperskills
cd ~/.claude/skills/paperskills && ./setup
```

单项目安装：

```bash
mkdir -p .claude/skills
ln -s /path/to/paperskills .claude/skills/paperskills
cd .claude/skills/paperskills && ./setup
```

`./setup` 会创建诸如 `.claude/skills/peer-review` 和 `.claude/skills/shared` 的同级链接，便于 agent 原生发现各个子技能。更新 PaperSkills 后建议重新执行一次 `./setup`。

### Codex

可以直接告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

也可以手动安装：

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.agents/skills/paperskills
cd ~/.agents/skills/paperskills && ./setup
```

### Cursor

Cursor 当前不会原生自动发现 `SKILL.md`。更实用的方式是把 PaperSkills 作为项目内 prompt library，并通过 Cursor Rules 指向安装说明。

可以直接告诉 Cursor：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.cursor/INSTALL.md
```

或参考 [`.cursor/INSTALL.md`](./.cursor/INSTALL.md)。

### OpenCode 和其他 Agent

PaperSkills 使用 registry 保存 skill metadata，便于安装器和后续集成生成不同 agent 平台的安装命令。支持平台和 sparse-checkout 路径见 [`registry/skills.json`](./registry/skills.json)。

## 项目结构

- [`SKILL.md`](./SKILL.md)：PaperSkills 路由入口
- [`skills/`](./skills)：核心学术工作流 skills
- [`registry/`](./registry)：skill、scenario、pack 元数据
- [`docs/`](./docs)：中英文文档页面
- [`assets/`](./assets)：共享报告模板与资源
- [`setup`](./setup)：安装后的链接初始化脚本

## 设计原则

- `Scenario-first`：用户应从自己的科研处境开始，而不是先解码一堆 skill 名称。
- `Skill-native`：每个工作流都应能在真实 AI agent 环境里安装和调用。
- `Composable`：skill 可以单独使用，也可以组合成完整论文生命周期。
- `Traceable`：文献检索、引用核验和投稿匹配优先基于公开、可检查的数据源。
- `Practical`：优先解决真实科研流程里的高频问题，而不是只做演示。
- `Extensible`：registry 应能同时承载 core skills、外部 skills 和未来 skill packs。

## 语言支持

报告生成类 skills 支持中英文输出。系统会根据稿件内容自动判断，也可以显式指定：

```text
用中文生成报告
```

## 路线图

当前 MVP 重点是：

- 为常见科研阶段建立场景页
- 建立 skills、packs、推荐 workflow 的 registry
- 支持跨 agent 平台生成安装命令
- 为每个场景提供可复制 prompt 和预期输出
- 维护一组可在本地 agent 环境中运行的核心论文 skills

后续会继续扩展外部 skill packs、用户 preset、paper-tracker watchlist、面向 agent 的结构化索引，以及更多领域化科研工作流。

## 参考项目与感谢

PaperSkills 受到以下开源项目的启发，也对它们表示感谢：

- [HughYau/AcademicForge](https://github.com/HughYau/AcademicForge)：PaperSkills 在 skill registry、安装命令生成、跨 agent 分发和 skill 选配体验上重点参考了这个项目。
- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)：提供了 AI 学术研究与写作工具生态的重要整理。
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code)：在 agent 工作流组织和研究型 coding-agent 实践上提供了启发。

PaperSkills 会借鉴这些项目的基础能力，但产品方向有所不同：分发能力是基础设施，围绕论文生命周期组织的场景化科研工作流才是核心体验。

## License

MIT

<p align="center">
  <img src="./logo-readme.png" alt="PaperSkills" width="80" />
</p>

<h1 align="center">PaperSkills</h1>

<p align="center"><strong>PaperSkills，面向科研用户的 AI Agent 学术工作箱。</strong></p>

<p align="center">
  帮你找到、组合并安装当前科研任务所需的 Agent Skills
</p>

<p align="center">
  <a href="https://www.paperskills.com/zh"><strong>从科研场景开始</strong></a>
  · <a href="https://www.paperskills.com/zh/skills">浏览 349 个 Skills</a>
  · <a href="./registry/scenarios.json">场景目录</a>
  · <a href="./README.md">English</a>
</p>

## AI 工具那么多，真正难的是怎么把它们用进科研

AI 工具、Agent 和 Skills 越来越多。面对如此多的选择，很多研究者并不是没有工具可用，而是不知道该选什么、怎样开始，又该如何把这些工具真正用进自己的科研流程。

- 这个工具看起来很强，但到底适不适合我的课题？
- 找到一个可能有用的 Skill，要准备什么材料，第一句话又该怎么说？
- Skills 分散在不同仓库里，怎么安装，能不能用于自己的 Agent？
- 单次检索、分析或写作都能完成，怎样把它们接成一条完整的科研流程？
- AI 给出了结果，我该检查什么，又该接着做哪一步？

**PaperSkills 想做的，就是少让你走这段弯路，帮助你高效借助 AI 工具的能力，加快科研进度。** 我们从不同开源仓库中筛选高质量的科研 Skills，再把它们整理成看得懂的科研场景、可以直接使用的 Skill 组合，以及能够复制运行的安装命令。你不用先研究完所有 AI 工具，只要说清楚“我现在想完成什么科研任务”，就能找到一条可以马上动手的路径。

## PaperSkills 里现在有什么

| 你能用到的内容 | 当前规模 | 用来做什么 |
| --- | ---: | --- |
| 可安装 Skills | **349** | 覆盖科研流程、写作润色、科研工程、图表与可视化 |
| Repositories | **13** | 汇集 PaperSkills Core 和 12 个外部 Skill 来源 |
| 科研场景 | **12** | 告诉你要准备什么、调用哪些 Skills、怎样提问、会得到什么 |
| 场景分组 | **4** | 从问题与证据，一路覆盖计算科研、实验环境和发表传播 |
| Skill Packs | **7** | 把经常一起使用的 Skills 保存成可复用组合 |
| Agent 适配 | **广泛兼容** | 可用于各类支持 Skills 的 Agent，并对 4 个主流 Agent 提供深度适配 |

其中，PaperSkills Core 是我们维护的一组本地 Skills，目前有 9 个。**它只是 349 个可安装 Skills 中的一部分，并不是 PaperSkills 的全部。** 另外 340 个 Skills 来自 12 个外部 Skill 来源。

## 不知道怎么选，也没关系

### 1. 不确定用什么：从科研场景开始

如果你还不确定该用哪个 Skill，先别急着翻完整列表。打开 [PaperSkills 中文首页](https://www.paperskills.com/zh)，找到与你当前任务最接近的场景。页面会帮你把下面几件事理清楚：

- 需要准备哪些输入材料
- 推荐组合哪些 Skills
- 每一步可以复制什么 Prompt
- 应该得到哪些中间产物
- 完成后可以进入哪个后续场景

目前的 12 个场景，按真实科研工作分成四组：

| 场景组 | 包含的工作流 |
| --- | --- |
| 从问题到证据 | 文献与证据、设计与统计、数据分析管线 |
| 计算科研与学科工具 | AI 与模型实验、生命科学数据、蛋白分子材料、地理与物理科学 |
| 实验、算力与可复用工作流 | 实验与自动化、算力与环境、自定义科研 Agent |
| 发表与科研传播 | 论文与投稿、图表与展示 |

这里的场景不只是一张“推荐工具清单”。每个场景都会把 Skills 串成可以照着推进的流程，告诉你每一步怎样提问、应该拿到什么，以及接下来往哪里走。完整数据见 [`registry/scenarios.json`](./registry/scenarios.json)。

### 2. 已经知道需要什么：进入 Skills 安装台

如果你已经知道自己要做什么，就直接打开 [Skills 安装台](https://www.paperskills.com/zh/skills)：

1. 按“流程与方法、写作与润色、科研与工程、图表与可视化”筛选 Skills。
2. 选择一个完整集合，或只选择集合中的某个 Skill。
3. 选择 macOS / Linux 或 Windows。
4. 选择已深度适配的 Claude Code、Codex、Cursor 或 OpenCode。
5. 复制自动生成的安装命令，到终端里运行。

PaperSkills 收录的 Skills 并不局限于这四个 Agent。只要你的 Agent 支持 Skills 或兼容相应目录规范，通常都可以使用；Claude Code、Codex、Cursor 和 OpenCode 则拥有更完整的安装命令生成与路径适配。

你也可以从场景页带着推荐组合直接进入安装台，不用再把同一批 Skills 逐个找一遍。

## 这些 Skills 从哪里来

PaperSkills 不只收录自己维护的 Skills，也持续从优秀的开源项目中筛选高质量 Skills。我们关注它们是否真正解决科研问题、是否具备清晰的使用方式，以及能否融入实际工作流；同时保留明确的来源、许可和安装信息，再放进同一个可检索、可安装的目录中。

| 类型 | 当前收录 |
| --- | --- |
| PaperSkills 本地集合 | PaperSkills Core（9 Skills） |
| 通用 Agent 工作流 | Superpowers、Karpathy-Inspired Claude Code Guidelines、Qiushi Skill |
| 科研 Agent 与学科工具 | Scientific Agent Skills、AI Research Skills、Nature Skills、Claude Science |
| 写作与语言处理 | Humanizer、Humanizer ZH、Paper Polish Workflow |
| 科研图表与展示 | Scientific Visualization、PosterSkill |

这些外部来源带来了 340 个可安装 Skills，加上 PaperSkills Core 的 9 个，构成安装台目前展示的 349 个 Skills。每个 Skill 来自哪里、使用什么开源许可、应该从哪里安装，都记录在 [`registry/academicforge-skills.json`](./registry/academicforge-skills.json) 和 [`registry/skills.json`](./registry/skills.json) 中。

## 给维护者：Registry 是怎样组织的

如果你想了解网站和安装器背后的数据结构，可以从 `registry/` 目录开始：

```text
registry/
├── skills.json                  # PaperSkills Core 的 9 个本地 Skills
├── academicforge-skills.json    # 12 个外部集合或仓库条目，共 340 Skills
├── academicforge-overrides.json # 场景引用的外部 Skills 与本地策展信息
├── scenarios.json               # 12 个科研场景及其完整工作流
└── packs.json                   # 7 个可复用 Skill Packs
```

网站、场景页和安装器都读取这套 Registry，因此同一个 Skill 不需要在多个地方重复维护：

- 场景通过 `skillIds` 组合本地与外部 Skills。
- 集合可以整体安装，也可以展开后只安装单个 Skill。
- 安装器根据 Skill 的仓库、路径和版本生成跨 Agent 命令。
- 网站和 Agent 可以通过结构化接口读取同一份 Skill 数据。

面向 Agent 的入口包括 [`/SKILL.md`](https://www.paperskills.com/SKILL.md)、[`/api/skills`](https://www.paperskills.com/api/skills) 和 [`/api/scenarios`](https://www.paperskills.com/api/scenarios)。

## 仓库结构

```text
.
├── SKILL.md                 # PaperSkills Agent 路由入口
├── skills/                  # PaperSkills 本地 Skills
├── registry/                # Skills、场景、集合与来源元数据
├── docs/                    # 中英文文档
├── assets/                  # 报告模板与共享资源
├── scripts/                 # 网站发布的跨 Agent 安装脚本
└── setup                    # 安装后的链接初始化脚本
```

## 设计原则

- **Scenario-first**：先理解研究者当前要完成的任务，再推荐 Skills 和下一步。
- **Curated**：优先收录真正解决科研问题、能够用于实际工作流的高质量 Skills。
- **Agent-native**：广泛兼容各类 Agent，并为 Claude Code、Codex、Cursor、OpenCode 提供深度适配和可直接运行的安装命令。
- **Composable**：单个 Skill 解决局部任务，多个 Skills 组成完整科研工作流。
- **Traceable**：保留来源仓库、许可、安装路径、场景步骤和预期产物。

## 参考项目与感谢

PaperSkills 所收录的丰富内容，离不开众多 Skill 作者和开源项目维护者。谢谢他们愿意把自己的经验做成可以复用的工具。以下项目也为 PaperSkills 的产品和工作流设计带来了很多启发：

- [HughYau/AcademicForge](https://github.com/HughYau/AcademicForge)：在 Skill Registry、跨 Agent 分发、集合安装和 Skill 选配体验上提供了重要参考。
- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)：整理了 AI 学术研究与写作工具生态中的大量资源。
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code)：在研究写作工作流、引用核验和审稿报告等方向提供了参考。

我们会继续学习这些项目在分发、工具整理和工作流设计上的经验。**PaperSkills，面向科研用户的 AI Agent 学术工作箱。** 当你面对越来越多的 AI 工具，不知道该怎样借力时，希望 PaperSkills 能帮你少一点试错，更快地迈出下一步。

## License

MIT

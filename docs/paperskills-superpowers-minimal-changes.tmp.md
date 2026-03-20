# PaperSkills 借鉴 Superpowers 的最小改造文档

这是一份临时修改文档。

用途：
- 作为接下来修改 `paperskills` 的执行依据
- 限定在“最小改造”范围
- 真正完成对应修改后删除本文件

---

## 目标

在不引入过多新概念的前提下，把 `superpowers` 里最值得借鉴的三类能力落到 `paperskills`：

1. 更强的入口路由纪律
2. 更强的完成前验证纪律
3. 更清晰的跨阶段 handoff 和 brief 合规检查

---

## 修改范围

### 新增 skills

1. `skills/evidence-before-completion/SKILL.md`
2. `skills/brief-compliance-review/SKILL.md`

### 修改现有 skills

1. `skills/using-paperskills/SKILL.md`
2. `skills/writing-paperskills/SKILL.md`
3. `skills/research-scoping/SKILL.md`
4. `skills/literature-review/SKILL.md`
5. `skills/research-design/SKILL.md`
6. `skills/paper-drafting/SKILL.md`
7. `skills/peer-review/SKILL.md`
8. `skills/revision-planning/SKILL.md`

---

## 逐项改造说明

## 1. 强化 `using-paperskills`

文件：
- `skills/using-paperskills/SKILL.md`

新增或调整内容：

- 增加一个更强的总规则：
  - 只要请求可能跨多个研究阶段，必须先做 stage diagnosis
  - 不得先直接起草内容、搜文献、写评论，再回头补路由

- 增加 `Red Flags` 小节，至少覆盖：
  - “先写一版再说”
  - “先搜几篇再判断阶段”
  - “用户要完整论文，所以直接进入 drafting”
  - “后续阶段缺证据也可以先按完成态写”

- 增加简短决策流程：
  - topic 模糊 -> `research-scoping`
  - 要最近论文/近期趋势 -> `paper-tracker`
  - 要综述/gap -> `literature-review`
  - 要研究问题/假设/方法 -> `research-design`
  - 要论文草稿 -> 先检查证据和 manuscript type，不足则回退上游阶段

- 明确“不得越级伪造确定性”：
  - 未完成 evidence gathering 时，不得把输出写成已完成 empirical paper 的口吻

目标效果：
- 让 `using-paperskills` 从“推荐式路由”升级到“强约束入口”

---

## 2. 新增 `evidence-before-completion`

文件：
- `skills/evidence-before-completion/SKILL.md`

定位：
- 这是 `paperskills` 的横切 skill
- 对应科研语境下的“verification before completion”

建议核心规则：

- 没核对来源，不得说“文献表明”或“研究一致认为”
- 没区分显式证据与推断，不得给高置信结论
- 只基于摘要、部分章节、有限材料时，必须标记 `partial`、`low confidence` 或等价限制说明
- brief 必填字段未满足时，不得声称该阶段已完成
- 下游 handoff 字段未明确时，不得声称“可以直接进入下一阶段”

建议适用场景：
- `paper-tracker`
- `literature-review`
- `research-design`
- `paper-drafting`
- `peer-review`
- `revision-planning`

建议结构：
- Overview
- Iron Law
- When to Use
- Common False Claims
- Verification Checklist
- Output Language for Uncertainty
- Common Mistakes

---

## 3. 新增 `brief-compliance-review`

文件：
- `skills/brief-compliance-review/SKILL.md`

定位：
- 审查产物是否符合 brief，而不是先审内容“写得漂不漂亮”

检查重点：

- 是否符合对应 schema / normalized brief
- 是否遗漏用户目标
- 是否保留 `language`
- 是否保留 `manuscript_type`
- 是否保留 `evidence_status` 或等价证据完整度字段
- 是否明确限制和缺口
- 是否越权补写 brief 未给出的强结论

建议使用方式：
- 作为各阶段 skill 的结束前检查
- 必要时再进入更偏内容质量的下游评估

---

## 4. 给核心执行 skills 增加统一的完成前检查与 handoff 纪律

文件：
- `skills/research-scoping/SKILL.md`
- `skills/literature-review/SKILL.md`
- `skills/research-design/SKILL.md`
- `skills/paper-drafting/SKILL.md`
- `skills/peer-review/SKILL.md`
- `skills/revision-planning/SKILL.md`

每个文件建议统一增加两个小节。

### A. Before Claiming Completion

固定表达方向：

- 检查是否满足当前 brief 的必需字段
- 检查是否清楚写出 evidence limits
- 检查是否区分 paper text、source evidence、agent inference
- 检查输出语言、manuscript type、confidence 是否与 brief 一致
- 必要时使用 `paperskills:evidence-before-completion`

### B. Downstream Handoff

固定表达方向：

- 推荐的 next skill 是什么
- 应传递哪一种 brief
- 哪些字段必须持久化：
  - `language`
  - `manuscript_type`
  - `evidence_status`
  - `time_window`
  - `target_artifact`

目标效果：
- 让阶段之间不是“靠上下文猜”，而是靠明示 handoff 契约推进

---

## 5. 扩充 `writing-paperskills`

文件：
- `skills/writing-paperskills/SKILL.md`

新增内容建议：

- `Failure-first authoring`
  - 写 skill 前，先构造 2 到 3 个 prompt
  - 观察没有该 skill 时 agent 会如何误路由、误推断、越级输出

- `Skill test cases`
  - trigger test
  - wrong-skill avoidance test
  - workflow handoff test
  - evidence-boundary test

- `Description anti-patterns`
  - description 只写触发条件
  - 不写 workflow 摘要
  - 不写“它会如何执行”

- `Guardrail design`
  - 每个新 skill 必须明确：
    - evidence boundary
    - allowed inference
    - forbidden claims
    - downstream handoff contract

目标效果：
- 让新增 skill 的质量控制从“有 checklist”升级到“有测试思维和 guardrail 方法”

---

## 推荐实施顺序

1. 先改 `skills/using-paperskills/SKILL.md`
2. 再新增 `skills/evidence-before-completion/SKILL.md`
3. 再改 `skills/writing-paperskills/SKILL.md`
4. 再新增 `skills/brief-compliance-review/SKILL.md`
5. 最后统一补齐各执行 skill 的 completion/handoff 小节

---

## 完成标准

满足以下条件即可删除本文件：

- `using-paperskills` 已具备更强入口约束
- `evidence-before-completion` 已存在并可被下游 skill 引用
- `brief-compliance-review` 已存在并可作为结束前检查
- 核心阶段 skill 已明确 completion discipline 和 downstream handoff
- `writing-paperskills` 已能指导后续 skill 按同一风格继续扩展

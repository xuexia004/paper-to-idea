# Paper to Idea

面向 AI / 计算机方向研究生的科研论文阅读 Skill：从论文证据出发，发现值得验证的问题，形成可证伪的假设与资源可控的实验计划。

**Paper → Understanding → Critical Analysis → Research Gap → Scientific Question → Hypothesis → Experiment → Research Idea**

默认中文，保留专业英文术语。适合 LLM、RAG、Agent、推理与机器学习方向的单篇精读和多篇联合分析。

## 可以用它做什么

| 模式 | 典型请求 | 产物 |
| --- | --- | --- |
| Paper Triage | 这篇是否值得精读或复现？ | 简洁筛选报告 |
| Deep Reading | 作者的问题、假设与实验证据成立吗？ | 结构化精读、证据与局限 |
| Idea Mining | 有哪些具体、可验证的 Research Gaps？ | 通常 3～5 个候选 Idea |
| Novelty & Feasibility | 哪个优先做，是否已有类似工作？ | 查新状态、六维评分、1～2 项优先建议 |
| Experiment Planning | 一张 GPU、六周，先验证什么？ | MVE、公平基线、控制/消融、预算与停止条件 |

区分 **Evidence / Inference / Hypothesis**，核心判断追溯到原文 Section、Equation、Figure、Table 或可识别摘录。不会把“论文未研究”直接当作创新；没有联网时明确标记“创新性尚未验证”。

## 安装到 Codex

将 [skills/paper-to-idea](skills/paper-to-idea/SKILL.md) **整个文件夹**放进 Codex 的 `skills` 目录。默认位置是 `~/.codex/skills/paper-to-idea`；如果设置了 `CODEX_HOME`，使用其下的 `skills/paper-to-idea`。

也可在有 `skill-installer` 的 Codex 中请求：

```text
$skill-installer 请安装 https://github.com/xuexia004/paper-to-idea/tree/main/skills/paper-to-idea
```

Windows 手动安装示例（在想保存仓库的目录执行；已有安装时先检查差异）：

```powershell
git clone https://github.com/xuexia004/paper-to-idea.git
$skillBase = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $env:USERPROFILE '.codex\skills'
}
$skillTarget = Join-Path $skillBase 'paper-to-idea'
if (Test-Path -LiteralPath $skillTarget) { throw '目标已存在，请先检查已有 Skill。' }
New-Item -ItemType Directory -Path $skillBase -Force | Out-Null
Copy-Item -LiteralPath '.\paper-to-idea\skills\paper-to-idea' -Destination $skillTarget -Recurse
```

Skill 本身是 Markdown 与 YAML，无需 Python 运行时。全文读取、检索、代码执行随宿主环境能力提供；缺失时按入口中的降级规则工作。

## 调用示例

```text
$paper-to-idea 快速筛选这篇 RAG 论文，判断是否值得精读，附判断依据。
```

```text
$paper-to-idea 精读这份 PDF，重点检查核心机制、关键公式与实验是否支持结论。
区分作者报告、你的推断与待验证假设，所有关键判断给原文定位。
```

```text
$paper-to-idea 基于这三篇论文做联合分析，找共同瓶颈，生成 3 个候选 Idea。
检索最接近的工作，明确创新性核验范围；不要因为论文没做就声称研究空白。
```

```text
$paper-to-idea 我选择 I01。硕士生，一张 24GB GPU，六周，先设计低成本 MVE。
给公平基线、主指标、消融、资源估算依据和失败停止规则；当前不要启动实验。
```

```text
$paper-to-idea 新增这篇论文，更新当前研究目录中的 literature-map.md。
保留论文和 Idea ID，说明哪些旧判断被新证据改变。
```

## 目录

```text
skills/paper-to-idea/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── reading-framework.md
│   ├── idea-generation.md
│   ├── evaluation-rubric.md
│   └── experiment-design.md
└── assets/templates/
    ├── paper-triage.md
    ├── deep-reading.md
    ├── research-gaps.md
    ├── idea-candidates.md
    ├── idea-evaluation.md
    ├── experiment-plan.md
    └── literature-map.md
```

入口只加载当前模式相关参考。研究记录保存在用户选择的研究目录；Skill 安装目录不存论文笔记，也不自动写入代理全局记忆。

## 演示与验收

- [从单篇精读到三个 Idea、评分与六周实验计划](examples/walkthrough.md)。**使用清楚标记的虚构论文和数字，没有冒充真实文献或实验。**
- [三篇虚构研究的联合比较与增量修订](examples/literature-map.md)。
- [六项行为验收用例](evals/cases.md)与[首次作者自检记录](evals/results.md)。自演练不等于独立评测。

维护者可运行结构检查并打包：

```text
python -m pip install -r requirements-dev.txt
python tools/validate_package.py
python tools/build_package.py
```

打包产物为 `dist/paper-to-idea.zip`，只包含可安装 Skill。开发依赖只用于仓库维护，不是 Skill 使用前提。

结构检查验证元数据、文件与引用能否正确安装和加载；科研判断仍需真实论文、真实检索和实验检验。评分不是原创性证明或录用概率。当前示范没有真实 PDF 解析、查新或训练验证，限制详见自检记录。

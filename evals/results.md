# 首次自检记录

日期：2026-10-16。执行方式：本次构建者读取生成的 Skill 与原始虚构 fixture，完成示范输出，再按 [cases.md](cases.md) 人工核对。**这是作者自演练，不是独立盲测，不是自动化科研正确性评测。** 没有使用真实论文、联网文献检索、模型 API 或训练资源。

| 用例 | 实际产物 | 自检结论与可核查依据 | 保留限制 |
| --- | --- | --- | --- |
| T1 | [walkthrough](../examples/walkthrough.md) §2 | 已覆盖：六项证据、问题/方法/实验/三类局限；正确区分 25% Token 差与等质量结论 | 只覆盖人为摘录，没有真实公式/PDF |
| T2 | [walkthrough](../examples/walkthrough.md) §3 | 已覆盖：三项有条件 Gap，每项有证据、问题、对照；无全领域空白结论 | 真实重要性与已有覆盖尚未查证 |
| T3 | [walkthrough](../examples/walkthrough.md) §4～5 | 已覆盖：三项 Idea 的假设、反证、MVE、风险、检索式；18 项维度评分带来源类别与置信度 | Novelty 为低置信暂评，未验证原创性 |
| T4 | [literature-map](../examples/literature-map.md) | 已覆盖：三论文设置矩阵、表面冲突解释、共同瓶颈、稳定 ID 与增量修订 | 合成材料过短，不能证明真实综述能力 |
| T5 | [unavailable-paper](outputs/unavailable-paper.md) | 已覆盖：拒绝补造 Table 7；区分无法核验与不存在；保留未验证标记 | 只执行一项无材料场景，未穷举不可读图像等情况 |
| T6 | [walkthrough](../examples/walkthrough.md) §6 | 已覆盖：12 项实验计划，100 次 pilot + 800 次验证的预算，实测后估时与停止判据 | 没有真实设备吞吐/数据/模型验证，六周可行性仍是计划 |

结构验证与内容演练分开解释。`tools/validate_package.py` 只检查 Skill 包格式、元数据与资源链接；通过不代表论文判断或模型行为得到独立验证。

本次实际执行的结构检查（两条命令退出码均为 0）：

```text
python -X utf8 <skill-creator>/scripts/quick_validate.py skills/paper-to-idea
Skill is valid!

python -X utf8 tools/validate_package.py
PASS skill frontmatter and installation name
PASS UI metadata and invocation prompt
PASS seven public output templates
PASS 30 local resource links and self-contained Skill paths
```

第一条使用构建环境已有的 `skill-creator` 校验器，路径以中性的 `<skill-creator>` 标记，避免把机器上的私人绝对路径写入公共仓库。第二条是仓库自带命令，可直接复用。

已知后续验证需求：用真实 LLM/RAG 全文测试公式/图表定位；实际查询最近似工作；换执行模型做盲测；以真实数据和设备运行 MVE。以上限制不通过编造结果来补齐。

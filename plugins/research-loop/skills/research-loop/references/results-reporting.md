# Report results: experiment → observation → cause → conclusion

The answer first, every number within reach, and a conclusion a colleague can act on. Rigor shows in how causes were tested and how sure you are, not in hedges.

- Write every analysis of results (page, report section or reply) in four steps and always reach the last: experiment, observation, cause, conclusion (Korean headings 실험, 현상, 원인 규명, 결론). Lead with the answer, then the decisive comparison, then the rest; order by importance, never by run date; keep one name per condition.
- Experiment: the question, and why this comparison answers it: the one difference between arms, what was held equal (model, data, budget, tuning), the prediction. Brief: the experiment page holds the rest.
- Observation: everything measured, and no "because". First the decisive comparison as a table with table.chart titled by its finding: baseline, value, difference, unit, direction (↑/↓) and variation (seeds or runs, spread or interval; each seed when few). Then the rest, including what does not fit. Keep complete tables or link them; a selected average never replaces them.
- Cause: list the plausible explanations, dull ones too (noise, a bug, unequal tuning or budget, leakage, a metric artifact), and what separates them: an ablation, a one-variable comparison, dose-response, error analysis (read failures, count them by kind), a direct measurement of the mechanism, consistency across seeds, data and models. Say which explanation survives and what ruled out each other; if nothing separates them yet, name the check that would. An untested explanation is a labeled hypothesis, never the conclusion.
- Conclusion: answer the question in one sentence a colleague can act on, then how sure and why ("all 3 seeds; the ablation removes the gain"), where it holds, what result would overturn it, and the next decision. State replicated evidence with a separating check plainly; anything weaker as likely, with the reason. Weak evidence still concludes: "not established, because …; this check would settle it". One limit per conclusion, the one that could change it; no hedge without a reason.
- Runs you started: node, GPU, paths, job IDs, commands, commits, environment, durations and run errors go in the 구현 확인 report's runs (section:implementation), which the page links. Run details you only record go under a final ## 재현 정보 section, which collapses. The text keeps hardware or cost only when that is the question, and run problems that change how a result reads (divergence, excluded seeds, a bug that touched numbers).

## Example

Illustrative, not a finding; localize it.

Weak: "B beat A on accuracy. Do not over-read this; more analysis is needed."

Strong:
- Experiment: does reusing the cached prefix (B) keep accuracy and cut latency? A recomputes; same model, data, 3 seeds.
- Observation: accuracy 71.8 ± 0.3 (B) vs 69.7 ± 0.4 (A), +2.1 pt on every seed; latency −38%. The gain is on inputs over 4k tokens (+5.0 pt), none under 1k.
- Cause: not noise (5× the seed spread) or tuning (same sweep). With caching off but B's truncation fix on, the gain stays: the fix explains accuracy, caching only latency.
- Conclusion: adopt B. Its accuracy gain comes from the truncation fix (high confidence: every seed, ablation); it would vanish if A had the fix, so port the fix to A next.

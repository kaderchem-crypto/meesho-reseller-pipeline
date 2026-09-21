# Meesho Reseller Monitoring Agent Specification

## 1. Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

## 2. Tools
- `validate_feed` (Part 2): Input guardrail for CSV data quality checks.
- `mom_growth` (Part 2): Computes Month-on-Month percentage growth.
- `is_flagged` (Part 2): Evaluates growth against the 8% threshold ("flagged", "not_flagged", "escalate_exact_boundary").
- Prompt-pack template-fill function (Part 3): Drafts stakeholder updates using verified context.

## 3. Memory / State
- Retains the previous month's revenue and order counts per category to compute the current run's MoM changes.

## 4. Planner (Ordered Subtasks)
1. Load the monthly revenue feed and run `validate_feed`.
2. If invalid, trigger a **Hard Stop** and report errors.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by absolute magnitude of `mom_pct` descending.
6. Draft a message via Part 3's template for at most the top 3 by magnitude (prevents notification flooding).
7. Log any remaining flagged categories beyond the cap as "suppressed, review manually" without drafting messages.
7b. Log any category whose result is "escalate_exact_boundary" into `escalated_categories`.
8. Emit one structured JSON object per run.

## 5. Feedback Loop
- Human-approval checkpoint before any drafted message is considered "sent" (simulated as a drafted status held for review, with no real email/API integration).

## 6. Guardrails
- **Input:** `validate_feed` must pass with zero errors before execution proceeds.
- **Action:** No message is ever auto-sent; messages are only drafted and held.
- **Output:** Every number in a drafted message must trace back directly to Part 1 / Part 2 values (no invented figures).

## 7. Success and Error Stopping Conditions
- **Success:** Drafts produced successfully (or zero drafts if nothing crossed the threshold) with every number fully traceable.
- **Error:** `validate_feed` returns `False`, causing a Hard Stop that surfaces validation errors.

## 8. Given-When-Then Specifications
1. **GIVEN** April-to-May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** `mom_growth` and `is_flagged` run, **THEN** `mom_growth` returns 77.1 and `is_flagged` returns "flagged".
2. **GIVEN** May-to-June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** evaluated, **THEN** `mom_growth` returns 5.67 and `is_flagged` returns "not_flagged".
3. **GIVEN** a synthetic pair previous = 100000, current = 108000, **WHEN** evaluated, **THEN** `mom_growth` returns exactly 8.0 and `is_flagged` returns "escalate_exact_boundary".
4. **GIVEN** a corrupted feed fixture, **WHEN** `validate_feed` runs, **THEN** it returns `(False, errors)` matching the exact error validation rules.
# Agent Specification: Meesho Reseller Flagged Category Monitor

## 1. Five Core Components of the Agentic System
* **Goal**: Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.
* **Tools**: Functions imported from Part 2 (`validate_feed`, `mom_growth`, `is_flagged`) and Part 3's prompt-pack template-filling logic.
* **Memory/State**: Retains historical monthly revenue records per category to compute the subsequent month's MoM growth transitions.
* **Planner**: An 8-step ordered sequence executing data ingestion, validation, growth calculation, flagging, sorting, capping/suppression, boundary classification, and JSON output emission.
* **Feedback Loop**: A human-approval checkpoint holding all drafted messages (`action_taken: "drafted_and_held_for_approval"`) with zero automatic dispatch.

## 2. Guardrails
* **Input Guardrail**: `validate_feed` must pass successfully before any downstream calculations or pipeline execution can occur.
* **Action Guardrail**: No message is ever auto-sent; messages are strictly drafted and held for human review.
* **Output Guardrail**: Every numeric figure within a drafted message must trace directly back to Part 1 or Part 2 values, preventing hallucinated or invented metrics.

## 3. Success and Error Stopping Conditions
* **Success Condition**: Valid feed input yields structured drafts (or zero drafts if thresholds remain uncrossed) with fully traceable numbers.
* **Error Stopping Condition**: A failed `validate_feed` triggers an immediate **Hard Stop** with validation errors explicitly surfaced, rather than a silent bypass.

## 4. Given-When-Then Specifications
1. **Given** a valid monthly revenue feed, **when** the validation runs, **then** it returns `True` and allows growth computations to proceed.
2. **Given** a corrupted revenue feed with schema errors or missing columns, **when** `validate_feed` executes, **then** it triggers a Hard Stop returning specific error messages and empty category lists.
3. **Given** category revenue data exceeding the 8% absolute MoM threshold, **when** the flagging engine evaluates growth, **then** it correctly tags the category as `"flagged"`.
4. **Given** more than three flagged categories in a single run, **when** the agent planner processes them, **then** it caps active message drafting at the top 3 by absolute magnitude and logs the remaining items as suppressed.
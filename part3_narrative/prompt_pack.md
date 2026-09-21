# Prompt Pack: Flagged Category Stakeholder Update

## Trigger
The specific condition that starts this prompt is when a category's MoM growth engine `is_flagged` validation result returns `"flagged"` (either significant positive growth spike or sharp negative revenue drop exceeding the threshold).

## Input list
* `{category}`: The specific business product category being evaluated (e.g., Ethnic Wear).
* `{previous_revenue}`: The total revenue recorded in the prior month (e.g., INR 59000.00).
* `{current_revenue}`: The total revenue recorded in the current evaluation month (e.g., INR 104520.77).
* `{mom_pct}`: The calculated Month-over-Month percentage change (e.g., 77.10% or -58.74%).
* `{month}`: The current reporting month name explicitly stated (e.g., May).
* `{prev_month}`: The prior comparative month name explicitly stated (e.g., April).

## Prompt
"You are an expert retail data analyst communicating with a regional manager. Using the data for {category} in {month} compared to {prev_month}, write a stakeholder update following the Context -> Insight -> Implication structure. 
- Context: State clearly what metric and period are being measured, referencing {month} vs. {prev_month}.
- Insight: State the exact MoM growth rate of {mom_pct} and current revenue of {current_revenue} ( compared to previous revenue of {previous_revenue}), and label this explicitly as a fact.
- Implication: Propose a concrete, actionable recommendation to investigate or address this performance, and label it explicitly as a hypothesis.
Strict Constraint: Never state any number, category, or month that is not derived directly from the supplied placeholder values. Never expose raw internal names."

## Checklist
1. Does every number and percentage in the generated draft match a supplied placeholder value exactly?
2. Is every analytical claim or metric explicitly labeled as a fact, and every proposed cause or recommendation labeled as a hypothesis?
3. Is the recommendation specific and actionable for a regional manager rather than vague?
4. Are all entities and resellers referenced only by coded alias or general terms, ensuring no raw internal names leak into the text?
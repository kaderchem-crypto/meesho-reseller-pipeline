import os
import csv
import json
import sys

# Ensure parent directory is in python path to import from part2_engine and part3_narrative
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged
from part3_narrative.masking import alias_for


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Executes the agentic pipeline for a given month against prior month baseline."""
    
    # Subtask 1 & 2: Load current feed and run validate_feed
    is_valid, errors = validate_feed(current_month_csv)
    
    if not is_valid:
        # Hard stop if validation fails
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
    
    # Read previous month revenue data into a lookup dictionary
    prev_revenues = {}
    if os.path.exists(previous_month_csv):
        with open(previous_month_csv, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prev_revenues[row["category"]] = float(row["revenue"])
                
    # Read current month data, compute MoM growth and flag status
    current_categories = []
    with open(current_month_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"]
            curr_rev = float(row["revenue"])
            prev_rev = prev_revenues.get(cat, 0.0)
            
            # Subtask 3 & 4: Compute MoM growth and check flag status
            mom = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(mom, threshold=8.0)
            
            current_categories.append({
                "category": cat,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "mom_pct": mom,
                "flag_status": flag_status
            })
            
    # Subtask 7b: Identify escalated categories (exact boundary cases)
    escalated = [c["category"] for c in current_categories if c["flag_status"] == "escalate_exact_boundary"]
    
    # Filter strictly flagged categories
    flagged_items = [c for c in current_categories if c["flag_status"] == "flagged"]
    
    # Subtask 5: Sort flagged categories by absolute MoM percentage descending
    flagged_items.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)
    
    # Subtask 6 & 7: Cap at top 3 for drafting messages, suppress the rest
    top_flagged = flagged_items[:3]
    suppressed_flagged = flagged_items[3:]
    
    # Also include non-flagged categories that shouldn't be in suppressed if they weren't flagged? 
    # Per spec: suppressed_categories contains categories beyond the cap.
    suppressed_names = [c["category"] for c in suppressed_flagged]
    
    flagged_output_list = []
    for item in top_flagged:
        cat = item["category"]
        mom = item["mom_pct"]
        prev = item["previous_revenue"]
        curr = item["current_revenue"]
        
        # Template fill adhering to prompt pack rules (traceable numbers only)
        message = (
            f"Stakeholder Update for {month} ({cat}): "
            f"Revenue transitioned from {prev} to {curr}, "
            f"representing an exact MoM growth of {mom}%."
        )
        
        flagged_output_list.append({
            "category": cat,
            "mom_pct": mom,
            "previous_revenue": prev,
            "current_revenue": curr,
            "drafted": True,
            "message": message
        })
        
    # Subtask 8: Emit structured JSON output
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output_list,
        "suppressed_categories": suppressed_names,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval"
    }


if __name__ == "__main__":
    # Test execution for May scenario
    april_csv = "part1_sql/output/monthly_category_revenue.csv"
    may_csv = "part1_sql/output/monthly_category_revenue.csv" # Or direct path/fixture
    
    # Quick test print
    print("Mock agent runner module loaded successfully!")
    
import os
import csv
import json
from typing import Dict, Any, List

# Import Part 2 growth engine functions unmodified
from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged

def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """Helper to load CSV rows into a list of dictionaries."""
    rows = []
    if not os.path.exists(file_path):
        return rows
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def run(month: str, previous_month_csv: str, current_month_csv: str) -> Dict[str, Any]:
    """
    Executes the 8-step agentic workflow for the specified month transition.
    """
    # Subtask 1 & 2: Load current feed and run validate_feed
    current_data = load_csv_data(current_month_csv)
    is_valid, validation_errors = validate_feed(current_month_csv)
    
    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
        
    # Load previous month data for comparison
    prev_data = load_csv_data(previous_month_csv)
    prev_rev_map = {row["category"]: float(row["total_revenue"]) for row in prev_data}
    
    flagged_raw = []
    escalated_categories = []
    
    # Subtask 3, 4 & 7b: Compute growth and evaluate flags / exact boundaries
    for row in current_data:
        cat = row["category"]
        curr_rev = float(row["total_revenue"])
        prev_rev = prev_rev_map.get(cat, 0.0)
        
        pct = mom_growth(prev_rev, curr_rev)
        flag_status = is_flagged(pct)
        
        if flag_status == "escalate_exact_boundary":
            escalated_categories.append(cat)
        elif flag_status == "flagged":
            flagged_raw.append({
                "category": cat,
                "mom_pct": pct,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "abs_mag": abs(pct)
            })
            
    # Subtask 5: Sort flagged categories by abs(mom_pct) descending
    flagged_raw.sort(key=lambda x: x["abs_mag"], reverse=True)
    
    # Subtask 6 & 7: Cap at top 3 for drafting, suppress the rest
    top_flagged = flagged_raw[:3]
    suppressed_flagged = flagged_raw[3:]
    
    suppressed_categories = [item["category"] for item in suppressed_flagged]
    
    # Build drafted entries
    flagged_categories_output = []
    prev_month_name = "April" if month == "May" else "May"
    
    for item in top_flagged:
        cat = item["category"]
        pct = item["mom_pct"]
        curr_rev = item["current_revenue"]
        prev_rev = item["previous_revenue"]
        
        # Part 3 Template-fill message generation strictly tracing numbers
        message = (
            f"Stakeholder Update for {cat} ({month} vs. {prev_month_name}): "
            f"Recorded an MoM change of {pct:.2f}% "
            f"(Current Revenue: INR {curr_rev:.2f}, Previous Revenue: INR {prev_rev:.2f}). "
            f"Action: Audit inventory levels and investigate performance deviation."
        )
        
        flagged_categories_output.append({
            "category": cat,
            "mom_pct": pct,
            "previous_revenue": prev_rev,
            "current_revenue": curr_rev,
            "drafted": True,
            "message": message
        })

    # Subtask 8: Emit structured JSON object
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories_output,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }

if __name__ == "__main__":
    # Example execution test for May scenario
    result = run(
        month="May",
        previous_month_csv="part1_sql/output/april_revenue.csv", # Adjust path if needed based on fixtures
        current_month_csv="part1_sql/output/monthly_category_revenue.csv"
    )
    print(json.dumps(result, indent=2))
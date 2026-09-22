import os
import csv
import json
import sys
from typing import Dict, Any, List

# Add project root directory to sys.path for robust module importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged

def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """Helper function to load CSV rows into a list of dictionaries."""
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
    # Safe validation call handling potential return structures
    validation_result = validate_feed(current_month_csv)
    if isinstance(validation_result, tuple):
        is_valid, validation_errors = validation_result
    else:
        is_valid = bool(validation_result)
        validation_errors = [] if is_valid else ["Feed validation failed."]
        
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
        
    current_data = load_csv_data(current_month_csv)
    prev_data = load_csv_data(previous_month_csv)
    prev_rev_map = {row["category"]: float(row["total_revenue"]) for row in prev_data}
    
    flagged_raw = []
    escalated_categories = []
    
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
            
    flagged_raw.sort(key=lambda x: x["abs_mag"], reverse=True)
    
    top_flagged = flagged_raw[:3]
    suppressed_flagged = flagged_raw[3:]
    suppressed_categories = [item["category"] for item in suppressed_flagged]
    
    flagged_categories_output = []
    prev_month_name = "April" if month == "May" else "May"
    
    for item in top_flagged:
        cat = item["category"]
        pct = item["mom_pct"]
        curr_rev = item["current_revenue"]
        prev_rev = item["previous_revenue"]
        
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
    result = run(
        month="May",
        previous_month_csv="part2_engine/fixtures/monthly_category_revenue.csv",
        current_month_csv="part2_engine/fixtures/monthly_category_revenue.csv"
    )
    print(json.dumps(result, indent=2))
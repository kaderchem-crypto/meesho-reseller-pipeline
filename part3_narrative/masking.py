import os
import csv
import json
import sys

# Import growth engine functions from Part 2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../part2_engine')))
from growth_engine import validate_feed, mom_growth, is_flagged

def load_revenue_csv(filepath):
    data = {}
    if not os.path.exists(filepath):
        return data
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row['category'].strip()
            rev = float(row['revenue'])
            n_ord = int(row['n_orders'])
            data[cat] = {'revenue': rev, 'n_orders': n_ord, 'month': row['month'].strip()}
    return data

def run_agent(run_month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    # Subtask 1 & 2: Validate current month feed
    is_valid, errors = validate_feed(current_month_csv)
    
    if not is_valid:
        return {
            "run_month": run_month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
    
    # Load data for comparison
    prev_data = load_revenue_csv(previous_month_csv)
    curr_data = load_revenue_csv(current_month_csv)
    
    evaluated_categories = []
    suppressed_categories = []
    escalated_categories = []
    
    # Subtask 3 & 4: Compute growth and check flags
    for cat, curr_info in curr_data.items():
        if cat in prev_data:
            prev_rev = prev_data[cat]['revenue']
            curr_rev = curr_info['revenue']
            pct = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(pct)
            
            item_info = {
                "category": cat,
                "mom_pct": pct,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "flag_status": flag_status,
                "abs_magnitude": abs(pct)
            }
            
            if flag_status == "flagged":
                evaluated_categories.append(item_info)
            elif flag_status == "escalate_exact_boundary":
                escalated_categories.append(cat)
                
    # Subtask 5: Sort flagged categories by abs(mom_pct) descending
    evaluated_categories.sort(key=lambda x: x['abs_magnitude'], reverse=True)
    
    # Subtask 6 & 7: Cap at top 3 for drafting, suppress the rest
    top_3 = evaluated_categories[:3]
    beyond_top_3 = evaluated_categories[3:]
    
    flagged_output_list = []
    for item in top_3:
        # Template draft generation (Part 3 integration)
        msg = (f"Context: {item['category']} performance update for {run_month}. "
               f"Insight: Revenue moved from {item['previous_revenue']} to {item['current_revenue']} "
               f"with a MoM growth of {item['mom_pct']}%. "
               f"Implication: Review category drivers and adjust inventory targets.")
        
        flagged_output_list.append({
            "category": item['category'],
            "mom_pct": item['mom_pct'],
            "previous_revenue": item['previous_revenue'],
            "current_revenue": item['current_revenue'],
            "drafted": True,
            "message": msg
        })
        
    for item in beyond_top_3:
        suppressed_categories.append(item['category'])
        
    return {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output_list,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }

if __name__ == "__main__":
    # Test May Scenario (April vs May)
    print("--- MAY SCENARIO ---")
    may_result = run_agent(
        "May", 
        "../part1_sql/output/monthly_category_revenue.csv", 
        "../part1_sql/output/monthly_category_revenue.csv"
    )
    print(json.dumps(may_result, indent=2))
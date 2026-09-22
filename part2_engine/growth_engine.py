import csv
import os


def mom_growth(previous: float, current: float) -> float:
    """Computes Month-on-Month growth percentage rounded to 2 decimals."""
    if previous == 0:
        if current == 0:
            return 0.0
        return 100.0 if current > 0 else -100.0
    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Evaluates whether growth percentage crosses the threshold."""
    abs_pct = abs(mom_pct)
    if abs_pct == threshold:
        return "escalate_exact_boundary"
    if abs_pct > threshold:
        return "flagged"
    return "not_flagged"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validates input revenue feed CSV for missing, non-numeric, or negative values."""
    errors = []
    if not os.path.exists(csv_path):
        return False, [f"File not found: {csv_path}"]

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return False, ["File is empty or missing header"]

        for idx, row in enumerate(reader, start=2):
            if len(row) < 4:
                errors.append(f"line {idx}: incomplete row: expected 4 columns, found {len(row)}")
                continue

            month, category, revenue_str, n_orders_str = (
                row[0].strip(),
                row[1].strip(),
                row[2].strip(),
                row[3].strip(),
            )

            if not month:
                errors.append(f"line {idx}: missing month")

            if not category:
                errors.append(f"line {idx}: missing category (month {month})")

            if not revenue_str:
                errors.append(f"line {idx}: missing revenue (category={category or 'unknown'})")
            else:
                try:
                    revenue = float(revenue_str)
                except ValueError:
                    errors.append(f"line {idx}: revenue not numeric: {revenue_str!r}")
                else:
                    if revenue < 0:
                        errors.append(f"Line {idx}: negative revenue ({revenue}) for category={category}")

            if not n_orders_str:
                errors.append(f"line {idx}: missing order count (category={category or 'unknown'})")
            else:
                try:
                    n_orders = int(float(n_orders_str))
                except ValueError:
                    errors.append(f"line {idx}: order count not numeric: {n_orders_str!r}")
                else:
                    if n_orders < 0:
                        errors.append(f"line {idx}: negative order count ({n_orders}) for category={category or 'unknown'}")

    if errors:
        return False, errors

    return True, []
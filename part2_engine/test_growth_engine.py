import os
import tempfile

from growth_engine import is_flagged, mom_growth, validate_feed


def test_mom_growth_zero_baseline():
    assert mom_growth(0, 50) == 100.0
    assert mom_growth(0, 0) == 0.0


def test_is_flagged_threshold_behavior():
    assert is_flagged(8.0) == "escalate_exact_boundary"
    assert is_flagged(8.1) == "flagged"
    assert is_flagged(7.9) == "not_flagged"


def test_validate_feed_rejects_invalid_rows():
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("month,category,revenue,n_orders\n")
            f.write("April,Ethnic Wear,1200,10\n")
            f.write("May,Western Wear,-100,5\n")
            f.write("June,,900,4\n")
            f.write("July,Kids Wear,abc,2\n")
            f.write("August,Home & Kitchen,500,\n")
            f.write("September,Beauty & Personal Care,450,-1\n")

        ok, errors = validate_feed(path)
        assert ok is False
        assert any("negative revenue" in e for e in errors)
        assert any("missing category" in e for e in errors)
        assert any("order count" in e for e in errors)
    finally:
        os.remove(path)


if __name__ == "__main__":
    test_mom_growth_zero_baseline()
    test_is_flagged_threshold_behavior()
    test_validate_feed_rejects_invalid_rows()
    print("All tests passed successfully!")
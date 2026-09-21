from masking import alias_for, assert_no_raw_names_leak

def test_masking_functions():
    # Test alias generation
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"
    print("Alias generation tests passed!")

    # Define a list of raw reseller names from Part 1
    raw_names = ["Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6"]

    # Test safe text (contains alias, no raw names)
    safe_text = "Top performance was driven by ALIAS-19 in the West region."
    assert assert_no_raw_names_leak(safe_text, raw_names) is True

    # Test unsafe text (contains raw name leak)
    unsafe_text = "Top performance was driven by Mumbai Reseller 1 in the West region."
    assert assert_no_raw_names_leak(unsafe_text, raw_names) is False
    print("Leak detection tests passed successfully!")

if __name__ == "__main__":
    test_masking_functions()
from SRS import SRS
from PMM import PMM


def main():
    # test_srs_path = "test.srs"
    # test_srs = SRS()
    # test_srs.load_terms_from_file(test_srs_path)

    # test_srs.print_terms()
    basic_pmm_test()


def basic_pmm_test():
    test_pmm = PMM()
    test_states = [
        {"h": 1, "s": 3},
        {"e": 2, "i": 6},
        {"r": 8},
        {"h": 4},
        {"e": 5},
        {},
        {"s": 7},
        {},
        {"s": 9},
        {},
    ]
    # test_pmm.states = test_states
    print(test_states)
    keywords = ["he", "she", "his", "hers"]
    test_pmm.construct_goto(keywords)
    print(test_pmm.states)
    test_pmm.failure_table = [0, 0, 0, 1, 2, 0, 3, 0, 3]
    test_output = {2: ["he"], 5: ["she", "he"], 7: ["his"], 9: ["hers"]}
    test_pmm.output = test_output
    matches = test_pmm.find_match("ushers")
    print(matches)


main()

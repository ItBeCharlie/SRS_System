from SRS import SRS
from PMM import PMM


def main():
    # test_srs_path = "test.srs"
    # test_srs = SRS()
    # test_srs.load_terms_from_file(test_srs_path)

    # test_srs.print_terms()
    basic_pmm_test()


def basic_pmm_test():
    keywords = ["he", "she", "his", "hers"]
    alphabet = "usheri"
    test_pmm = PMM(keywords, alphabet)
    test_pmm.print_transition_table()
    test_pmm.print_failure_function()
    test_pmm.print_output_function()
    matches = test_pmm.find_match("ushers")
    print(matches)

    pmm2 = PMM(["aba", "bb"], "ab")
    pmm2.print_transition_table()
    pmm2.print_failure_function()
    pmm2.print_output_function()


main()

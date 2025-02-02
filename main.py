from SRS import SRS
from PMM import PMM
import sys


def main():
    srs_path = sys.argv[1]
    srs = SRS(srs_path)

    srs.print_terms()

    srs.PMM.print_transition_table()
    srs.PMM.print_failure_function()
    srs.PMM.print_output_function()
    # basic_pmm_test()


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

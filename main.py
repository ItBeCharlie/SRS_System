from SRS import SRS
from PMM import PMM
from Helper import KMPSearch, computeOverlap
import sys


def main():
    # srs_path = sys.argv[1]
    # srs = SRS(srs_path)

    # srs.print_terms()

    # srs.PMM.print_transition_table()
    # srs.PMM.print_failure_function()
    # srs.PMM.print_output_function()

    # srs.is_church_rosser()

    # pat = "aa"
    # txt = "bbaababbaabb"

    # matches = KMPSearch(pat, txt)
    # print(matches)
    # for match in matches:
    #     print(txt[0:match], pat, txt[match + len(pat) :])
    print(computeOverlap("ababcababa"))
    # basic_pmm_test()

    # print(srs.find_normal_form("bbaababbabbbaabaababb", True))


def basic_pmm_test():
    keywords = ["he", "she", "his", "hers"]
    alphabet = "usheri"
    test_pmm = PMM(keywords, alphabet)
    test_pmm.print_transition_table()
    test_pmm.print_failure_function()
    test_pmm.print_output_function()
    matches = test_pmm.find_match("ushers")
    print(matches)


main()

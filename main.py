import random as r
from SRS import SRS
from PMM import PMM
from Helper import KMPSearch, computeOverlap
import sys
import os


def main():
    # srs_path = sys.argv[1]
    # srs = SRS(srs_path)

    # srs.print_terms()

    # srs.PMM.print_transition_table()
    # srs.PMM.print_failure_function()
    # srs.PMM.print_output_function()

    # print(srs.is_church_rosser())

    # srs.export("exporttest.srs")

    # pat = "aa"
    # txt = "bbaababbaabb"

    # matches = KMPSearch(pat, txt)
    # print(matches)
    # for match in matches:
    #     print(txt[0:match], pat, txt[match + len(pat) :])
    # print(computeOverlap("ababcababa"))
    # basic_pmm_test()

    # print(srs.find_normal_form("bbaababbabbbaabaababb", True))

    # print(10 ** (3**4))

    # string_generator("ab", 0, 5)

    srs_batch_generator("ab", num_systems=100, max_lhs_len=3, max_rhs_len=3)
    # srs_generator("ab", max_lhs_len=3, max_rhs_len=3, seed=6238478396790087245)


def basic_pmm_test():
    keywords = ["he", "she", "his", "hers"]
    alphabet = "usheri"
    test_pmm = PMM(keywords, alphabet)
    test_pmm.print_transition_table()
    test_pmm.print_failure_function()
    test_pmm.print_output_function()
    matches = test_pmm.find_match("ushers")
    print(matches)


"""
    10 ** (3**5 + 3**4 + 3**3 + 3**2 + 3**1)

"""


def srs_batch_generator(
    alphabet,
    max_lhs_len=5,
    max_rhs_len=5,
    min_lhs_len=1,
    min_rhs_len=0,
    num_systems=5,
    num_rules=5,
):
    for i in range(num_systems):
        print(i)
        srs_generator(
            alphabet, max_lhs_len, max_rhs_len, min_lhs_len, min_rhs_len, num_rules
        )


def srs_generator(
    alphabet,
    max_lhs_len=5,
    max_rhs_len=5,
    min_lhs_len=1,
    min_rhs_len=0,
    num_rules=5,
    seed=None,
):
    current_srs = SRS(alphabet=alphabet)
    if seed == None:
        seed = r.randrange(sys.maxsize)
    r.seed(seed)
    for _ in range(num_rules):
        lhs = ""
        rhs = ""
        while lhs == rhs:
            lhs = rand_string(alphabet, r.randint(min_lhs_len, max_lhs_len))
            rhs = rand_string(
                alphabet, min(r.randint(min_rhs_len, max_rhs_len), len(lhs))
            )
        current_srs.add_term(lhs, rhs)
    current_srs.complete_initialization()
    if current_srs.is_church_rosser(True):
        current_srs.export(os.path.join("church-rosser", f"{alphabet}_{str(seed)}.srs"))
        print("Church-Rosser Found!")
    current_srs.print_terms()


def rand_string(alphabet, length):
    out = ""
    for _ in range(length):
        out += alphabet[r.randint(0, len(alphabet) - 1)]
    return out


main()

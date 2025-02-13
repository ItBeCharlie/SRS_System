import re
from PMM import PMM
from Helper import KMPSearch

import time


class SRS:
    def __init__(self, file_path):
        self.terms = {}
        self.longest_lhs_length = 0
        self.PMM = None
        self.alphabet = ""
        self.load_terms_from_file(file_path)
        self.determine_alphabet()
        self.generate_pmm()

    def load_terms_from_file(self, file_path):
        """
        Given an input file, will parse the file and populate the terms dictionary.
        Terms in the input file take the form of "{lhs} -> {rhs}"
        """
        with open(file_path, "r") as file:
            parsed_lines = []
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                match = re.search(r"^(.*) -> (.*)$", stripped_line)
                if match:
                    lhs = match.group(1)
                    rhs = match.group(2)
                    # Update the longest lhs length if found for printing purposes
                    self.longest_lhs_length = max(len(lhs), self.longest_lhs_length)
                    # Initialize LHS
                    self.terms.setdefault(lhs, [])
                    # Add RHS to LHS
                    self.terms[lhs].append(rhs)
            # print(self.terms)

    def determine_alphabet(self):
        """
        Based on the rules of lhs and rhs, will add all present characters to the alphabet
        """
        for lhs in self.terms:
            self.add_to_alphabet(lhs)
            for rhs in self.terms[lhs]:
                self.add_to_alphabet(rhs)

    def add_to_alphabet(self, string):
        for symbol in string:
            if symbol not in self.alphabet:
                self.alphabet += symbol

    def generate_pmm(self):
        """
        Will generate a Pattern Matching Machines based on the lhs rules
        """
        lhs_list = list(self.terms.keys())
        self.PMM = PMM(lhs_list, self.alphabet)

    def find_normal_form(self, input_string, debug=False):
        """
        Given a string, find the normal form of it using the method described in section 3 of Dran paper
        """
        # Keeps track of current character being edited in string
        index = 0
        # Form will be reduced until normal form is found
        form = input_string
        # Current state of Trie
        state = 0
        # History of previous states
        state_stack = [state]
        if debug:
            print(form)
            print(f"\t{state}")
        while index < len(form):
            if debug:
                print(form[index])
            state = self.PMM.perform_operation_cycle(state, form[index])
            state_stack.append(state)
            if debug:
                print(f"\t{state}")
            # If state is one of the output states, a reduction can be performed
            if state in self.PMM.output:
                # Grab one of the rules from PMM, the exact rule does not matter
                lhs_rule = self.PMM.output[state][0]
                # Perform the reduction on our form
                w_1 = form[0 : index - len(lhs_rule) + 1]
                R_i = self.terms[lhs_rule][0]
                w_2 = form[index + 1 :]
                form = w_1 + R_i + w_2
                if debug:
                    print(f"{lhs_rule} -> {R_i}")
                    print(form)
                # Bring index back to beginning of string replaced
                index -= len(lhs_rule) - 1
                # Restore state back to one before reduction
                state_stack = state_stack[0 : index + 1]
                state = state_stack[-1]
                if debug:
                    print(f"\t{state}")

                # exit()
            else:
                index += 1
        return form

    def get_sorted_lhs(self):
        """
        Will return a list of the rules sorted in descending length of lhs.
        If a lhs has multiple rules, there will be an entry for each lhs
        """
        term_pairs = []
        for lhs in self.terms:
            for rhs in self.terms[lhs]:
                term_pairs.append((lhs, rhs))
        sorted_pairs = sorted(term_pairs, key=lambda x: len(x[0]), reverse=True)
        return sorted_pairs

    def check_substring_condition(self, debug=False):
        """
        Checks that a given system S meets the following condition:

        Given i != j, L_i -> R_i and L_j -> R_j, and L_j is a substring of L_i
        such that is can be decomposed as L_i = xL_jy, check whether the normal
        form of R_i and xR_jy are the same. If they are not, then the system cannot
        be Church-Rosser
        """
        invalid_pairs = []
        invalid_normals = []
        pairs = self.get_sorted_lhs()
        # Get two pairs of distinct rules where |L_i| >= |L_j|
        for i in range(len(pairs)):
            l_i, r_i = pairs[i]
            for j in range(i + 1, len(pairs)):
                l_j, r_j = pairs[j]
                # Find all substrings of L_j in L_i
                subtring_indexes = KMPSearch(l_j, l_i)
                # For all substrings, check if the normal forms of
                # R_i and xR_jy are the same
                for indexes in subtring_indexes:
                    x = l_i[0:indexes]
                    y = l_i[indexes + len(l_j) :]
                    if debug:
                        print(f"i: {pairs[i]}")
                        print(f"j: {pairs[j]}")
                        print("x L_j y")
                        print(x, l_j, y)
                    normal_i = self.find_normal_form(r_i)
                    normal_j = self.find_normal_form(x + r_j + y)
                    if debug:
                        print(f"Normals: {normal_i}, {normal_j}\n")
                    # Log the invalid form, to optimize, could simply return False here
                    if normal_i != normal_j:
                        invalid_pairs.append((pairs[i], pairs[j]))
                        invalid_normals.append((normal_i, normal_j))
        if debug:
            for i in range(len(invalid_pairs)):
                print(invalid_pairs[i], invalid_normals[i])
        return len(invalid_pairs) == 0

    def check_overlaps_condition(self):
        """
        Checks that a given system S follows the following condition:

        For all i and j where L_i and L_j properly overlap, consider all
        possible overlapped strings. For every overlapped string L_iv = uL_j,
        check whether the normal form of R_iv and uR_j are the same.
        """

    def is_church_rosser(self):
        """
        Returns true if the given SRS has the Church-Rosser property based on Dran paper
        """
        self.check_substring_condition(True)

    def print_terms(self):
        """
        Print the terms in self.terms in an easy to read format
        """
        for key in self.terms:
            # Get list of right hand sides
            rhses = self.terms[key]
            print(f"{key:{self.longest_lhs_length}} -> {rhses[0]}")
            for index in range(1, len(rhses)):
                print(f"{' ' * (self.longest_lhs_length)} -> {rhses[index]}")
            print("\n")

    def terms_to_tex(self):
        pass

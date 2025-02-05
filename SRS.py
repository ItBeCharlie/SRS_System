import re
from PMM import PMM

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
        
    def find_normal_form(self, input_string):
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
        while index < len(form):
            print(f"\t{state}")
            state = self.PMM.perform_operation_cycle(state, form[index])
            print(form[index])
            state_stack.append(state)
            # If state is one of the output states, a reduction can be performed
            if state in self.PMM.output:
                print(f"\t{state}")
                # Grab one of the rules from PMM, the exact rule does not matter
                print(f"index: {index}")
                lhs_rule = self.PMM.output[state][0]
                print(lhs_rule)
                # Perform the reduction on our form
                w_1 = form[0:index-len(lhs_rule)+1] 
                R_i = self.terms[lhs_rule][0] 
                w_2 = form[index+1:]
                print(f"{w_1}, {R_i}, {w_2}")
                print(form)
                form = w_1 + R_i + w_2
                print(form)
                # Bring index back to beginning of string replaced
                index -= len(lhs_rule)
                print(index)
                # Restore state back to one before reduction
                print(state_stack)
                state_stack = state_stack[0:index+2]
                state = state_stack[-1]
                print(state_stack)
                # exit()
            else:
                index += 1
            time.sleep(0.5)
        return form
                

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
            print()

    def terms_to_tex(self):
        pass

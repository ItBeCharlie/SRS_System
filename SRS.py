import re

class SRS:
    def __init__(self):
        self.terms = {}
        self.longest_lhs_length = 0
        
    def load_terms_from_file(self, file_path):
        """
        Given an input file, will parse the file and populate the terms dictionary.
        Terms in the input file take the form of "{lhs} -> {rhs}"
        """
        with open(file_path, 'r') as file:
            parsed_lines = []
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                match = re.search(r'^(.*) -> (.*)$', stripped_line)
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
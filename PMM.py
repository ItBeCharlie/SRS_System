class PMM:
    def __init__(self, keywords, alphabet):
        self.keywords = keywords
        self.states = []
        self.output = {}
        self.failure_table = []
        self.alphabet = alphabet
        self.construct_goto()
        self.construct_failure()

    def goto(self, state, symbol):
        # If state is undefined, return fail
        if state == None or state >= len(self.states):
            return "fail"
        return self.states[state][symbol]

    def failure(self, state):
        return self.failure_table[state]

    def find_match(self, test_string):
        state = 0
        n = len(test_string)
        matches = []
        for i in range(0, n):
            print(f"\t{state}")
            state = self.perform_operation_cycle(state, test_string[i])
            if state in self.output:
                matches.append((i, self.output[state]))
        print(f"\t{state}")
        return matches
    
    def perform_operation_cycle(self, state, symbol):
        while self.goto(state, symbol) == "fail":
            state = self.failure(state)
            print(f"\t{state}")
        state = self.goto(state, symbol)
        print(symbol)
        return state

    def construct_goto(self):
        newstate = 0
        # Create state 0
        self.initialize_state()
        k = len(self.keywords)
        for i in range(0, k):
            keyword = self.keywords[i]
            state = 0
            j = 0
            m = len(keyword)
            # While the next state is valid, continue to traverse Trie until a new branch must be created
            while j < m and self.goto(state, keyword[j]) != "fail":
                state = self.goto(state, keyword[j])
                j += 1

            # Once the beginning of the new branch is met, continually add nodes to add rest of string to Trie
            for p in range(j, m):
                newstate += 1
                # Assign all characters to fail by default. May not be needed
                self.initialize_state()
                # Add transition from current state to new state on current character
                self.states[state][keyword[p]] = newstate
                # Advance to next state
                state = newstate
            # Initialize output set
            if state not in self.output:
                self.output[state] = []
            # Add current string to output function
            self.output[state].append(keyword)
        # Make all fail transitions on state 0 go to itself
        for symbol in self.states[0]:
            if self.states[0][symbol] == "fail":
                self.states[0][symbol] = 0

    def initialize_state(self):
        newstate = {}
        for symbol in self.alphabet:
            newstate[symbol] = "fail"
        self.states.append(newstate)

    def construct_failure(self):
        self.failure_table = [None] * len(self.states)
        queue = []
        # For each symbol that points to a state other than 0, add to queue and set failure function to 0 for that state
        for symbol in self.states[0]:
            if self.goto(0, symbol) != 0:
                queue.append(self.goto(0, symbol))
                self.failure_table[self.goto(0, symbol)] = 0

        while len(queue) != 0:
            # Pop state r off the front of queue
            r = queue.pop(0)
            # For each symbol that points to a valid state (isn't fail), do the following process
            for symbol in self.states[r]:
                s = self.goto(r, symbol)
                if s != "fail":
                    # Add state to end of queue
                    queue.append(s)
                    # Continually traverse failure states until a transition doesn't fail
                    state = self.failure(r)
                    while self.goto(state, symbol) == "fail":
                        state = self.failure(state)
                    # Update failure function for state processed
                    self.failure_table[s] = self.goto(state, symbol)
                    # Update output table
                    if self.failure(s) in self.output:
                        for output_keyword in self.output[self.failure(s)]:
                            if output_keyword not in self.output[s]:
                                self.output[s].append(output_keyword)

    def print_transition_table(self):
        print("----- GOTO FUNCTION -----")
        i = 0
        for state in self.states:
            print(i)
            for symbol in state:
                if state[symbol] != "fail":
                    print(symbol, state[symbol])
            print()
            i += 1
        print("-------------------------")

    def print_failure_function(self):
        print("----- FAILURE FUNCTION -----")
        print(f"i{' ' * 5}", end="")
        fail_str_len = len(str(len(self.failure_table)))
        for i in range(1, len(self.failure_table)):
            print(f"{i:{fail_str_len}} ", end="")
        print()
        print(f"f(i){' ' * 2}", end="")
        for i in range(1, len(self.failure_table)):
            print(f"{self.failure(i):{fail_str_len}} ", end="")
        print()
        print("----------------------------")

    def print_output_function(self):
        print("----- OUTPUT FUNCTION -----")
        fail_str_len = len(str(len(self.failure_table)))
        print(f"i{' ' * (fail_str_len+2)}output(i)")
        for state in self.output:
            print(f"{state}    {self.output[state]}")
        print("---------------------------")

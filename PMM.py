class PMM:
    def __init__(self):
        self.keywords = []
        self.states = []
        self.output = {}
        self.failure_table = []

    def goto(self, state, symbol):
        # If state is undefined, return fail
        if state >= len(self.states):
            return "fail"
        # Get the transition table for current state
        current = self.states[state]
        # Get the 'index' of the next state to transition to
        if symbol in current:
            next = current[symbol]
            return next
        # If the state does not have a valid transition
        return "fail"

    def failure(self, state):
        return self.failure_table[state - 1]

    def find_match(self, test_string):
        state = 0
        n = len(test_string)
        matches = []
        for i in range(0, n):
            print(f"\t{state}")
            while self.goto(state, test_string[i]) == "fail":
                state = self.failure(state)
                print(f"\t{state}")
            state = self.goto(state, test_string[i])
            print(test_string[i])
            if state in self.output:
                matches.append((i, self.output[state]))
        print(f"\t{state}")
        return matches

    def construct_goto(self, keywords, alphabet):
        newstate = 0
        # Create state 0
        self.initialize_state(alphabet)
        k = len(keywords)
        for i in range(0, k):
            keyword = keywords[i]
            state = 0
            j = 0
            m = len(keyword)
            # While the next state is valid, continue to traverse Trie until a new branch must be created
            while self.goto(state, keyword[j]) != "fail":
                state = self.goto(state, keyword[j])
                j += 1
            # Once the beginning of the new branch is met, continually add nodes to add rest of string to Trie
            for p in range(j, m):
                newstate += 1
                # Assign all characters to fail by default. May not be needed
                self.initialize_state(alphabet)
                # Add transition from current state to new state on current character
                self.states[state][keyword[p]] = newstate
                # Advance to next state
                state = newstate
            # Initialize output set
            if state not in self.output:
                self.output[state] = {}
            # Add current string to output function
            self.output[state] = keyword
        # Make all fail transitions on state 0 go to itself
        for symbol in self.states[0]:
            if self.states[0][symbol] == "fail":
                self.states[0][symbol] = 0

    def initialize_state(self, alphabet):
        newstate = {}
        for symbol in alphabet:
            newstate[symbol] = "fail"
        self.states.append(newstate)

    def print_transition_table(self):
        i = 0
        for state in self.states:
            print(i)
            for symbol in state:
                if state[symbol] != "fail":
                    print(symbol, state[symbol])
            print()
            i += 1

class PMM:
    def __init__(self):
        self.keywords = []
        self.states = []
        self.output = {}
        self.failure_table = []

    def goto(self, state, symbol):
        # Get the transition table for current state
        current = self.states[state]
        # Get the 'index' of the next state to transition to
        if symbol in current:
            next = current[symbol]
            return next
        # If the state does not have a valid transition
        # If state is 0, this is special and transitions to itself on all invalid symbols
        if state == 0:
            return 0
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

# treatment_stack.py

class TreatmentNode:
    def __init__(self, treatment, next_node=None):
        self.treatment = treatment
        self.next = next_node

class TreatmentStack:
    def __init__(self):
        self.top = None

    def push(self, treatment):
        """Add a treatment to the top of the stack."""
        new_node = TreatmentNode(treatment, self.top)
        self.top = new_node

    def pop(self):
        """Remove and return the last treatment (LIFO)."""
        if self.top is None:
            return None
        treatment = self.top.treatment
        self.top = self.top.next
        return treatment

    def peek(self):
        """View the treatment at the top of the stack without removing it."""
        return self.top.treatment if self.top else None

    def is_empty(self):
        return self.top is None

    def get_all(self):
        """Return all treatments from top to bottom as a list."""
        treatments = []
        current = self.top
        while current:
            treatments.append(current.treatment)
            current = current.next
        return treatments

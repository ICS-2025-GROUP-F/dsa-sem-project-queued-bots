# department_tree.py

class DepartmentNode:
    def __init__(self, name):
        self.name = name
        self.sub_departments = []

    def add_sub_department(self, sub_dept_node):
        self.sub_departments.append(sub_dept_node)

    def display_tree(self, level=0):
        lines = ["  " * level + f"- {self.name}"]
        for sub in self.sub_departments:
            lines.extend(sub.display_tree(level + 1))
        return lines

    def traverse_tree(self):
        names = [self.name]
        for sub in self.sub_departments:
            names.extend(sub.traverse_tree())
        return names

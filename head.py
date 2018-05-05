import pickle
import csv


def indent_tree(tree):
    det = '---'
    split_tree = tree.split('\n')
    if split_tree[-1] == '':
        del split_tree[-1]
    new_branches = []
    for branch in split_tree:
        new_branches.append(det + branch)
    return "\n".join(new_branches) + '\n'


class HP(object):
    def __init__(self, id, hp_dict):
        self.id = id
        self.hp_dict = hp_dict
        self.name = None
        self.children = {}
        self.parents = []
        self.genes = []

    def __str__(self):
        return self.id

    def add_child(self, hp):
        self.children[str(hp)] = hp

    def add_parent(self, hp_id):
        self.parents.append(hp_id)

    def has_genes(self):
        return self.genes != []

    def children_has_genes(self):
        for id, child in self.children.items():
            if child.has_genes():
                return True
            elif child.children_has_genes():
                return True
        return False

    def get_children_ids(self):
        children_ids = [id for id, child in self.children.items()]
        return children_ids

    def get_children(self):
        children = [child for child_id, child in self.children.items()]
        return children

    def get_parents_ids(self):
        return self.parents

    def get_parents(self):
        parents = []
        for parent in self.parents:
            parents.append(self.hp_dict[parent])
        return parents

    def get_genes(self, sort=False):
        if sort:
            return sorted(self.genes)
        return self.genes

    def get_children_genes(self, unique=False, sort=False):
        children_genes = []
        for id, child in self.children.items():
            children_genes.extend(child.get_genes())
            children_genes.extend(child.get_children_genes())
        if unique:
            children_genes = list(set(children_genes))
        if sort:
            return sorted(children_genes)
        return children_genes

    def get_all_genes(self, unique=False, sort=False):
        all_genes = []
        all_genes.extend(self.genes)
        all_genes.extend(self.get_children_genes())
        if unique:
            all_genes = list(set(all_genes))
        if sort:
            return sorted(all_genes)
        return all_genes

    def up(self, parent=''):
        if isinstance(parent, str) and not parent:
            if len(self.parents) == 1:
                return self.get_parents()[0]
            elif len(self.parents) > 1:
                print("Choose parent (id or idx): ", self.get_parents_ids())
            else:
                print("No parents. Root?")
        else:
            if parent in self.get_parents_ids():
                return self.hp_dict[parent]
            elif isinstance(parent, int) and 0 <= parent <= len(self.get_parents_ids()):
                parent_idx = parent
                return self.hp_dict[self.get_parents_ids()[parent_idx]]
            else:
                print("Parent doesn't exist. Available parents (id or idx): ", self.get_parents_ids())
        return ''

    def down(self, child=''):
        if isinstance(child, str) and not child:
            if len(self.children) == 1:
                return self.get_children()[0]
            elif len(self.children) > 1:
                print("Choose child (id or idx): ", self.get_children_ids())
            else:
                print("No children. Leaf?")
        else:
            if child in self.get_children_ids():
                return self.children[child]
            elif isinstance(child, int) and 0 <= child <= len(self.get_children_ids()):
                child_idx = child
                return self.get_children()[child_idx]
            else:
                print("Child doesn't exist. Available children (id or idx): ", self.get_children_ids())
        return ''

    def tree(self, depth=-1, drop_empty=False):
        s = self.id
        if not self.genes:
            s += ' {}\n'.format(self.name)
        else:
            s += ' ({}) {}\n'.format(len(self.genes), self.name)
        for id, child in self.children.items():
            if drop_empty:
                if child.children_has_genes() or child.has_genes():
                    s += indent_tree(child.tree(drop_empty=drop_empty))
            else:
                s += indent_tree(child.tree())
        # Ugly way to trim tree to given depth
        if depth != -1:
            new_tree = []
            for branch in s.split('\n'):
                if len(branch.split('HP')[0]) // 3 <= depth:
                    new_tree.append(branch)
            s = '\n'.join(new_tree)
        return s

    def dump(self, all_genes=False):
        file_name = str(self).replace(':', '_')
        with open(file_name, 'w') as file:
            if all_genes:
                file.write('\n'.join(self.get_all_genes()))
            file.write('\n'.join(self.get_genes()))
        return file_name


def write_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output)  # ,pickle.HIGHEST_PROTOCOL)


def read_object(filename):
    with open(filename, 'rb') as input:  # Overwrites any existing file.
        return pickle.load(input)


def read_lines(filename):
    with open(filename) as hp_file:
        out = hp_file.readlines()
    return out

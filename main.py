import bte


class Backbone:
    def __init__(self, tree):
        self.tree = tree

    @staticmethod
    def has_one_tip_child(node):
        for child in node.children:
            if child.is_leaf():
                return True
        return False

    def get_internal_nodes_with_tip_children(self):
        """

        :return: A set of internal nodes ids as strings with at least one leaf children
        """
        internal_nodes = set()
        leaves = self.tree.get_leaves()
        for leaf in leaves:
            internal_nodes.add(leaf.parent.id)
        return internal_nodes

    def prune_nodes(self, threshold=2):
        """

        :param threshold:
        :return: a set of MATNode that are the nodes we want to prune
        """
        # TODO: maybe check each internal for have at least threshold childs
        # TODO: check prunning on the fly as it might work and make the program faster

        internal_node_ids = self.get_internal_nodes_with_tip_children()

        prune_set = set()
        for internal_node_id in internal_node_ids:
            internal_node = self.tree.get_node(internal_node_id)
            # print(internal_node)
            counter = 0
            for child in internal_node.children:
                if len(child.mutations) >= 1 and child.is_leaf():  # TODO: check if should just prune tip nodes
                    prune_set.add(child.id)
                else:
                    counter += 1
            if counter < threshold:
                for child in internal_node.children:
                    if child.is_leaf():
                        prune_set.add(child.id)

        return prune_set

    def backbone_tree(self, threshold=2):
        prunning_nodes = self.prune_nodes(threshold)
        for id in prunning_nodes:
            self.tree.remove_node(id)
        return self.tree


# texoniom

if __name__ == '__main__':
    import time

    first = time.time()
    file_name = 'public-2021-07-07.all.masked.pb.gz'
    tree = bte.MATree(file_name)
    backbone = Backbone(tree)
    print("original tree", tree)
    print('original tree parsimony score', tree.get_parsimony_score())
    new_tree = backbone.backbone_tree(5)
    print("backbone tree", new_tree)
    print("new tree parsimony score", new_tree.get_parsimony_score())
    print(time.time() - first)
    new_tree.save_pb(file_name[:-5] + "pruned_tree.pb")

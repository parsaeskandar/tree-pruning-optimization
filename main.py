import bte
import allel


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
        # Trying pruning one the fly led to segmentation fault

        internal_node_ids = self.get_internal_nodes_with_tip_children()

        prune_set = set()
        for internal_node_id in internal_node_ids:
            internal_node = self.tree.get_node(internal_node_id)
            # print(internal_node)
            counter = 0
            for child in internal_node.children:
                if len(child.mutations) >= 1 and child.is_leaf():  # should just prune tip nodes
                    prune_set.add(child.id)
                else:
                    counter += 1
            if counter < threshold:
                for child in internal_node.children:
                    if child.is_leaf():
                        prune_set.add(child.id)

        return prune_set

    def backbone_tree(self, threshold=2):
        pruning_nodes = self.prune_nodes(threshold)
        for id in pruning_nodes:
            self.tree.remove_node(id)
        return self.tree


if __name__ == '__main__':
    import time

    # TODO: saving pruned nodes can be with string type and then get all the node info from the actual tree
    # first = time.time()
    # # file_path = 'Data/public-latest.all.masked.pruned_tree_10_optimized_vcf_enabled.pb'
    file_path = 'Data/public-latest.all.masked/public-latest.all.masked.pb.gz'
    file_name = 'public-latest.all.masked.pb.gz'
    tree = bte.MATree(file_path)

    # print(len(tree.get_leaves()))
    threshold = 10
    backbone = Backbone(tree)
    new_tree = backbone.backbone_tree(threshold)
    # Writing the retained ids to a file
    #retained_nodes = new_tree.get_leaves()
    #with open("retained_nodes_ids.txt", 'w') as f:
    #    for item in retained_nodes:
    #        f.write("%s\n" % item.id)

    print(new_tree.get_parsimony_score())
    # new_tree.save_pb(file_name[:-5] + "pruned_tree_new_k10.pb")
    # print(new_tree.get_node("USA/UT-UPHL-220611544008/2022|ON787347.1|2022-05-23"))
    # print("backbone tree", new_tree)
    # print("new tree parsimony score", new_tree.get_parsimony_score())
    # print(time.time() - first)
    # print(pruned_ids)
    # vcf = allel.read_vcf('sample.vcf')
    
    # print(vcf.headers)

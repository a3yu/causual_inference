import random

class Graph:
    def __init__(self, size) -> None:
        self.size = size
        self._generate_graph()

    
    def _generate_graph(self):
        self.adjList = [0 for _ in range(self.size)]

    
    def __getitem__(self, key):
        return self.adjList[key]
    

    def __setitem__(self, key, value):
        self.adjList[key] = value

    def __len__(self):
        return len(self.adjList)

class SBM(Graph):
    def __init__(self, size, partition, probabilities) -> None:
        self.partition = partition
        self.probabilities = probabilities
        super().__init__(size)

    def _generate_graph(self):
        '''
        Stochastic Block Model
        size (int): number of nodes in the graph
        partition (list[list[int]]): 2d list encoding the grouping of the nodes: must be disjoint
        probabilities (list[list[float]]): 2d list encoding probabilities for edges b/w each partition
        Returns: adjlist (list[list[int]])
        '''
        # precompute node-to-partition mapping
        node_to_partition = {}
        for partition_index, nodes in enumerate(self.partition):
            for node in nodes:
                node_to_partition[node] = partition_index

        adjList = [[] for _ in range(self.size)]
        
        for i in range(self.size):
            adjList[i].append(i)  # add self loop
            for j in range(self.size):
                if i != j:
                    partition_i = node_to_partition[i]
                    partition_j = node_to_partition[j]
                    if random.random() < self.probabilities[partition_i][partition_j]:
                        adjList[j].append(i)  # add directed edge from i to j
        
        self.adjList = adjList
class SimpleSBM(Graph):
    def __init__(self, size, partitionAmount, inside, outside) -> None:
        self.size = size
        self.partitionAmount = partitionAmount
        self.inside = inside
        self.outside = outside
        super().__init__(size)

    def _generate_graph(self):
        # Divide nodes into roughly equal partitions and create node-to-partition mapping
        node_to_partition = {}
        partition_size = self.size // self.partitionAmount
        for p in range(self.partitionAmount):
            for node in range(p * partition_size, min((p + 1) * partition_size, self.size)):
                node_to_partition[node] = p

        # Handle any remaining nodes in case of uneven division
        for node in range(self.partitionAmount * partition_size, self.size):
            node_to_partition[node] = self.partitionAmount - 1

        adjList = [[] for _ in range(self.size)]

        for i in range(self.size):
            adjList[i].append(i)  # add self loop
            for j in range(self.size):
                if i != j:
                    partition_i = node_to_partition[i]
                    partition_j = node_to_partition[j]
                    probability = self.inside if partition_i == partition_j else self.outside

                    if random.random() < probability:
                        adjList[i].append(j)  # add directed edge from i to j

        self.adjList = adjList

class ER(SBM):
    def __init__(self, size, partition, p) -> None:
        r = len(partition)
        probabilities = [[p for _ in range(r)] for _ in range(r)]
        super().__init__(size, partition, probabilities)   

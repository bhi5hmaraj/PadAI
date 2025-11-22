"""
Graph model for software tensegrity structure.

Wraps NetworkX with software-specific methods and Laplacian computation.
"""

import networkx as nx
import numpy as np
from typing import List, Tuple


class TensegrityGraph:
    """
    Wrapper around NetworkX with software-specific methods.

    Represents the software system as a graph where:
    - Nodes = modules/components
    - Edges = dependencies with coupling weights
    - Laplacian matrix encodes neighbor disagreement

    Attributes:
        G: NetworkX graph
        L: Laplacian matrix (numpy array)
    """

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str, float]]):
        """
        Initialize tensegrity graph.

        Args:
            nodes: List of node identifiers (module names)
            edges: List of (node_i, node_j, weight) tuples
                  weight represents coupling strength
        """
        self.G = nx.Graph()
        self._initialize_nodes(nodes)
        self._initialize_edges(edges)
        self.L = None  # Laplacian matrix
        self._update_laplacian()

    def _initialize_nodes(self, nodes: List[str]):
        """Add nodes to graph."""
        for node_id in nodes:
            self.G.add_node(node_id)

    def _initialize_edges(self, edges: List[Tuple[str, str, float]]):
        """Add weighted edges to graph."""
        for (i, j, weight) in edges:
            self.G.add_edge(i, j, weight=weight)

    def _update_laplacian(self):
        """
        Compute and cache Laplacian matrix.

        L = D - A where:
        - D is degree matrix (diagonal)
        - A is adjacency matrix (weighted)

        Properties:
        - L is symmetric
        - L is positive semi-definite
        - Row sums = 0
        - Smallest eigenvalue = 0 (if connected)
        """
        self.L = nx.laplacian_matrix(self.G, weight='weight').toarray()

    def add_edge_weighted(self, i: str, j: str, weight: float):
        """
        Add or update edge with weight, recompute Laplacian.

        Args:
            i: Source node
            j: Target node
            weight: Coupling strength (positive)
        """
        self.G.add_edge(i, j, weight=weight)
        self._update_laplacian()

    def remove_edge_safe(self, i: str, j: str):
        """
        Remove edge if exists, recompute Laplacian.

        Args:
            i: Source node
            j: Target node
        """
        if self.G.has_edge(i, j):
            self.G.remove_edge(i, j)
            self._update_laplacian()

    def get_neighbors(self, node: str) -> List[str]:
        """
        Get list of neighboring nodes.

        Args:
            node: Node identifier

        Returns:
            List of neighbor node identifiers
        """
        return list(self.G.neighbors(node))

    def edges_touching(self, node: str) -> List[Tuple[str, str, dict]]:
        """
        Get all edges incident to a node.

        Args:
            node: Node identifier

        Returns:
            List of (source, target, edge_data) tuples
        """
        return list(self.G.edges(node, data=True))

    def node_count(self) -> int:
        """Return number of nodes."""
        return self.G.number_of_nodes()

    def edge_count(self) -> int:
        """Return number of edges."""
        return self.G.number_of_edges()

    def degree(self, node: str) -> int:
        """
        Get degree of a node (number of neighbors).

        Args:
            node: Node identifier

        Returns:
            Node degree
        """
        return self.G.degree[node]

    def weighted_degree(self, node: str) -> float:
        """
        Get weighted degree (sum of edge weights).

        Args:
            node: Node identifier

        Returns:
            Sum of weights of incident edges
        """
        return sum(self.G[node][neighbor]['weight']
                   for neighbor in self.G.neighbors(node))

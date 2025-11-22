"""
Energy calculations for software tensegrity physics.

Implements the Hamiltonian H = T + V where:
- T = kinetic energy (rate of change)
- V = potential energy (structural + business tension)
"""

import numpy as np
import networkx as nx
from typing import Dict


def compute_structural_potential(L: np.ndarray, bad: np.ndarray) -> float:
    """
    Compute structural potential energy (Dirichlet energy).

    V_struct = ½ bad^T L bad = ½ Σ w_ij (bad[i] - bad[j])²

    This measures the "stress" in the structure due to neighbor disagreement.
    High when coupled nodes have mismatched badness.

    Args:
        L: Laplacian matrix (n×n)
        bad: Badness vector (n,)

    Returns:
        Structural potential energy (scalar >= 0)

    Note:
        L must be positive semi-definite (PSD), so V_struct >= 0.
    """
    return 0.5 * bad.T @ L @ bad


def compute_business_potential(
    demand: Dict[str, float],
    health: Dict[str, float],
    complexity: Dict[str, float],
    λ1: float = 0.6,
    λ2: float = 0.4
) -> float:
    """
    Compute business potential energy.

    V_bus = Σ demand[i] · [λ1(1-health[i]) + λ2·complexity[i]]

    This measures "business cost" of unhealthy or complex high-demand modules.

    Args:
        demand: Dict mapping node -> demand value [0,1]
        health: Dict mapping node -> health value [0,1]
        complexity: Dict mapping node -> complexity value [0,1]
        λ1: Weight for health component (default 0.6)
        λ2: Weight for complexity component (default 0.4)

    Returns:
        Business potential energy (scalar >= 0)

    Note:
        λ1 + λ2 should = 1.0 (normalized weights)
    """
    V = 0.0
    for node_id in demand.keys():
        V += demand[node_id] * (λ1 * (1 - health[node_id]) + λ2 * complexity[node_id])
    return V


def compute_kinetic_energy(
    bad_curr: np.ndarray,
    bad_prev: np.ndarray,
    mass: np.ndarray = None
) -> float:
    """
    Compute kinetic energy (rate of change of badness).

    T = ½ Σ m_i (Δbad[i])²

    where Δbad[i] = bad_curr[i] - bad_prev[i]

    Args:
        bad_curr: Current badness vector (n,)
        bad_prev: Previous badness vector (n,)
        mass: Mass vector (n,). If None, uses m_i = 1 (uniform mass)

    Returns:
        Kinetic energy (scalar >= 0)

    Note:
        CONFUSION #1 RESOLVED: For MVP, use uniform mass m_i = 1
        This gives: T = 0.5 * np.sum((bad_curr - bad_prev)**2)

        Post-MVP: Could use m_i = demand[i] (business-weighted mass)
    """
    delta_bad = bad_curr - bad_prev

    if mass is None:
        # MVP: Uniform mass m_i = 1 for all nodes
        return 0.5 * np.sum(delta_bad**2)
    else:
        # General case: weighted by mass
        return 0.5 * np.sum(mass * delta_bad**2)


def compute_local_dirichlet_energy(
    G: nx.Graph,
    bad: Dict[str, float],
    node: str
) -> float:
    """
    Compute local Dirichlet energy at a node.

    E_local[i] = ½ Σ_{j∈neighbors(i)} w_ij (bad[i] - bad[j])²

    This measures local structural stress at node i.
    Used for early warning signals - high E_local at hubs predicts incidents.

    Args:
        G: NetworkX graph with 'weight' edge attribute
        bad: Dict mapping node -> badness value
        node: Node identifier

    Returns:
        Local energy at node (scalar >= 0)

    Note:
        This is the key metric for Experiment 02 (Laplacian early warning).
        Hypothesis: E_local spikes ~10 steps before incidents at hubs.
    """
    E = 0.0
    for neighbor in G.neighbors(node):
        w = G[node][neighbor].get('weight', 1.0)  # Default weight = 1.0
        diff = bad[node] - bad[neighbor]
        E += 0.5 * w * diff**2
    return E


def compute_hamiltonian(
    T: float,
    V_struct: float,
    V_bus: float
) -> float:
    """
    Compute total Hamiltonian (system stress).

    H = T + V = T + V_struct + V_bus

    This is the total "crisis energy" of the system.

    Args:
        T: Kinetic energy
        V_struct: Structural potential
        V_bus: Business potential

    Returns:
        Hamiltonian (scalar >= 0)

    Note:
        Used for governance thresholds (e.g., if H > H_max, trigger emergency brake)
    """
    return T + V_struct + V_bus


def compute_lagrangian(T: float, V: float) -> float:
    """
    Compute Lagrangian.

    L = T - V

    In classical mechanics, action = ∫ L dt.
    For our purposes, mainly diagnostic (not used for governance yet).

    Args:
        T: Kinetic energy
        V: Total potential energy

    Returns:
        Lagrangian (can be negative)
    """
    return T - V


def compute_phase_coordinates(T: float, V: float) -> tuple:
    """
    Compute phase space coordinates (T, V).

    Used to classify system regime:
    - Healthy flow: Low T, low V
    - Chaotic thrash: High T, high V
    - Frozen bureaucracy: Low T, high V
    - Stable equilibrium: Moderate T, moderate V

    Args:
        T: Kinetic energy
        V: Total potential energy

    Returns:
        (T, V) tuple

    Note:
        See research/diagrams/phase-space-regimes.svg for visualization.
    """
    return (T, V)


def incident_probability(
    bad_i: float,
    threshold: float = 0.6,
    steepness: float = 10.0,
    max_prob: float = 0.05
) -> float:
    """
    Compute incident probability based on badness.

    P(incident) = max_prob * sigmoid(steepness * (bad_i - threshold))

    Args:
        bad_i: Badness value [0,1]
        threshold: Badness value where P = max_prob/2 (default 0.6)
        steepness: How sharp the transition (default 10)
        max_prob: Maximum incident probability per step (default 0.05 = 5%)

    Returns:
        Probability of incident occurring this step [0, max_prob]

    Note:
        CONFUSION #4 RESOLVED: Use sigmoid for smooth transition.

        Calibration for MVP:
        - threshold = 0.6 (incidents unlikely below this)
        - steepness = 10 (fairly sharp)
        - max_prob = 0.05 (5% per step when very bad)
        - Expected: ~2-5 incidents per 100 steps in baseline

        If too many/few incidents: Adjust threshold or max_prob.
    """
    from scipy.special import expit  # Logistic sigmoid
    return max_prob * expit(steepness * (bad_i - threshold))

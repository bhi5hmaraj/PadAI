"""
Simulation state management.

Contains the complete state of the simulation at one time step,
including fields, energies, and diagnostic information.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np

from .graph_model import TensegrityGraph
from .energy import (
    compute_structural_potential,
    compute_business_potential,
    compute_kinetic_energy,
    compute_local_dirichlet_energy,
    compute_hamiltonian,
    compute_lagrangian,
)


@dataclass
class SimulationState:
    """
    Complete state of the simulation at one time step.

    Contains:
    - Graph structure
    - Scalar fields (health, complexity, risk, demand, badness)
    - Vector fields (flow, gradient)
    - Energy values (T, V, H, L)
    - Diagnostic information (E_local, incidents)

    Fields are stored as dicts mapping node_id -> value.
    """

    # Graph structure
    graph: TensegrityGraph

    # Primitive scalar fields [0, 1]
    health: Dict[str, float]
    complexity: Dict[str, float]
    demand: Dict[str, float]

    # Derived scalar fields
    risk: Dict[str, float] = field(default_factory=dict)
    bad: Dict[str, float] = field(default_factory=dict)
    bad_prev: Dict[str, float] = field(default_factory=dict)

    # Vector fields (2D vectors stored as tuples)
    flow: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    grad_V: Dict[str, float] = field(default_factory=dict)

    # Energy values
    V_struct: float = 0.0
    V_bus: float = 0.0
    V: float = 0.0
    T: float = 0.0
    H: float = 0.0
    L: float = 0.0  # Lagrangian

    # Diagnostic information
    E_local: Dict[str, float] = field(default_factory=dict)

    # Incident tracking
    incidents: List[Dict] = field(default_factory=list)

    # Time step counter
    time_step: int = 0

    def update_derived_fields(self, α: float = 0.4, β: float = 0.3, γ: float = 0.3):
        """
        Compute all derived fields from primitives.

        Order of computation (CONFUSION #2 RESOLVED):
        1. Update primitive fields (health, complexity, demand) - done externally
        2. Compute risk from health and complexity
        3. Compute badness from health, complexity, risk
        4. Compute gradient from badness
        5. Compute flow from demand and gradient

        Args:
            α: Weight for health component in badness (default 0.4)
            β: Weight for complexity component in badness (default 0.3)
            γ: Weight for risk component in badness (default 0.3)

        Note:
            CONFUSION #2 RESOLVED: risk = complexity × (1 - health)
            This breaks the circularity - risk is DERIVED, not primitive.

            Badness formula (expanded):
            bad[i] = α*(1 - health[i]) + β*complexity[i] + γ*complexity[i]*(1 - health[i])
                   = α*(1 - health[i]) + (β + γ*(1 - health[i]))*complexity[i]

            For MVP, use γ = 0.3 (risk contributes 30% weight).
        """
        # Step 1: Compute derived risk field
        for node in self.graph.G.nodes:
            self.risk[node] = self.complexity[node] * (1 - self.health[node])

        # Step 2: Compute badness using risk
        for node in self.graph.G.nodes:
            self.bad[node] = (
                α * (1 - self.health[node]) +
                β * self.complexity[node] +
                γ * self.risk[node]
            )

        # Step 3: Compute gradient (discrete Laplacian operator)
        for node in self.graph.G.nodes:
            grad = 0.0
            for neighbor in self.graph.get_neighbors(node):
                w = self.graph.G[node][neighbor]['weight']
                grad += w * (self.bad[node] - self.bad[neighbor])
            self.grad_V[node] = grad

        # Step 4: Compute flow field (business + stability)
        for node in self.graph.G.nodes:
            # Flow components
            business_x = self.demand[node]
            stability_y = -self.grad_V[node]

            # Flow weights (CONFUSION #5: How to interpret flow?)
            # For now, simple weighted combination
            α_flow, β_flow = 0.6, 0.4
            flow_x = α_flow * business_x
            flow_y = β_flow * stability_y

            self.flow[node] = (flow_x, flow_y)

    def update_energies(self):
        """
        Recompute all energy values from current fields.

        Computes:
        - V_struct: Structural potential (Dirichlet energy)
        - V_bus: Business potential
        - V: Total potential = V_struct + V_bus
        - T: Kinetic energy (rate of change)
        - H: Hamiltonian = T + V
        - L: Lagrangian = T - V
        - E_local[i]: Local energy at each node

        Note:
            Must be called after update_derived_fields() to have current badness.
        """
        # Convert dicts to arrays (ordered by graph node order)
        nodes = list(self.graph.G.nodes)
        bad_array = np.array([self.bad[n] for n in nodes])
        bad_prev_array = np.array([self.bad_prev.get(n, 0.0) for n in nodes])

        # Compute potential energies
        self.V_struct = compute_structural_potential(self.graph.L, bad_array)
        self.V_bus = compute_business_potential(
            self.demand, self.health, self.complexity
        )
        self.V = self.V_struct + self.V_bus

        # Compute kinetic energy (CONFUSION #1 RESOLVED: uniform mass)
        self.T = compute_kinetic_energy(bad_array, bad_prev_array, mass=None)

        # Compute Hamiltonian and Lagrangian
        self.H = compute_hamiltonian(self.T, self.V_struct, self.V_bus)
        self.L = compute_lagrangian(self.T, self.V)

        # Compute local energies (for early warning)
        for node in self.graph.G.nodes:
            self.E_local[node] = compute_local_dirichlet_energy(
                self.graph.G, self.bad, node
            )

    def step_forward(self):
        """
        Prepare for next time step.

        Saves current badness as previous and increments time counter.
        Call this at the end of each simulation step.
        """
        # Save current badness for next kinetic energy calculation
        self.bad_prev = self.bad.copy()

        # Increment time step
        self.time_step += 1

    def record_incident(self, node: str, incident_type: str, severity: float = 1.0):
        """
        Record an incident occurrence.

        Args:
            node: Node where incident occurred
            incident_type: Type of incident (e.g., "bug", "outage", "breach")
            severity: Severity of incident [0, 1]
        """
        self.incidents.append({
            'time_step': self.time_step,
            'node': node,
            'type': incident_type,
            'severity': severity,
            'bad': self.bad[node],
            'E_local': self.E_local[node],
            'health': self.health[node],
            'complexity': self.complexity[node],
        })

    def get_high_risk_nodes(self, threshold: float = 0.7) -> List[str]:
        """
        Get nodes with high badness (at risk).

        Args:
            threshold: Badness threshold [0, 1]

        Returns:
            List of node identifiers with bad[node] > threshold
        """
        return [node for node, bad_val in self.bad.items() if bad_val > threshold]

    def get_high_energy_hubs(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Get nodes with highest local Dirichlet energy.

        These are candidates for early warning signals.

        Args:
            top_n: Number of top nodes to return

        Returns:
            List of (node, E_local) tuples, sorted by E_local descending
        """
        sorted_nodes = sorted(
            self.E_local.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_nodes[:top_n]

    def get_phase_coordinates(self) -> Tuple[float, float]:
        """
        Get phase space coordinates (T, V).

        Returns:
            (T, V) tuple for phase space visualization
        """
        return (self.T, self.V)

    def summary_stats(self) -> Dict:
        """
        Compute summary statistics for current state.

        Returns:
            Dict with mean/std of fields and energies
        """
        nodes = list(self.graph.G.nodes)

        return {
            'time_step': self.time_step,
            'health_mean': np.mean([self.health[n] for n in nodes]),
            'health_std': np.std([self.health[n] for n in nodes]),
            'complexity_mean': np.mean([self.complexity[n] for n in nodes]),
            'complexity_std': np.std([self.complexity[n] for n in nodes]),
            'bad_mean': np.mean([self.bad[n] for n in nodes]),
            'bad_std': np.std([self.bad[n] for n in nodes]),
            'T': self.T,
            'V': self.V,
            'H': self.H,
            'L': self.L,
            'V_struct': self.V_struct,
            'V_bus': self.V_bus,
            'incident_count': len(self.incidents),
        }

    def __str__(self) -> str:
        """Human-readable state summary."""
        return (
            f"SimulationState(t={self.time_step}, "
            f"H={self.H:.3f}, T={self.T:.3f}, V={self.V:.3f}, "
            f"incidents={len(self.incidents)})"
        )

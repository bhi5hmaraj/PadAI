"""
Unit tests for Phase 1 core infrastructure.

Tests:
- Graph model (TensegrityGraph)
- Energy calculations
- Simulation state management
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulation.core import (
    TensegrityGraph,
    compute_structural_potential,
    compute_business_potential,
    compute_kinetic_energy,
    compute_local_dirichlet_energy,
    SimulationState,
)


class TestTensegrityGraph:
    """Test graph model creation and operations."""

    def test_graph_creation(self):
        """Test basic graph initialization."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('B', 'C', 0.5)]

        graph = TensegrityGraph(nodes, edges)

        assert graph.node_count() == 3
        assert graph.edge_count() == 2
        assert graph.L is not None

    def test_laplacian_properties(self):
        """Test Laplacian matrix properties."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('B', 'C', 1.0), ('C', 'A', 1.0)]

        graph = TensegrityGraph(nodes, edges)
        L = graph.L

        # Property 1: Symmetric
        assert np.allclose(L, L.T), "Laplacian should be symmetric"

        # Property 2: Row sums = 0
        row_sums = np.sum(L, axis=1)
        assert np.allclose(row_sums, 0), "Laplacian row sums should be 0"

        # Property 3: Positive semi-definite (all eigenvalues >= 0)
        eigenvalues = np.linalg.eigvalsh(L)
        assert np.all(eigenvalues >= -1e-10), "Laplacian should be PSD"

        # Property 4: Smallest eigenvalue ≈ 0 (connected graph)
        assert np.abs(eigenvalues[0]) < 1e-10, "Smallest eigenvalue should be ~0"

    def test_add_edge(self):
        """Test adding edges updates Laplacian."""
        nodes = ['A', 'B']
        edges = []

        graph = TensegrityGraph(nodes, edges)
        assert graph.edge_count() == 0

        graph.add_edge_weighted('A', 'B', 1.0)
        assert graph.edge_count() == 1
        assert graph.L is not None

    def test_remove_edge(self):
        """Test removing edges updates Laplacian."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('B', 'C', 1.0)]

        graph = TensegrityGraph(nodes, edges)
        assert graph.edge_count() == 2

        graph.remove_edge_safe('A', 'B')
        assert graph.edge_count() == 1

    def test_neighbors(self):
        """Test neighbor retrieval."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('A', 'C', 1.0)]

        graph = TensegrityGraph(nodes, edges)

        neighbors_A = graph.get_neighbors('A')
        assert set(neighbors_A) == {'B', 'C'}

        neighbors_B = graph.get_neighbors('B')
        assert neighbors_B == ['A']


class TestEnergyCalculations:
    """Test energy computation functions."""

    def test_structural_potential_simple(self):
        """Test structural potential on simple 3-node graph."""
        # Triangle graph with uniform weights
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('B', 'C', 1.0), ('C', 'A', 1.0)]
        graph = TensegrityGraph(nodes, edges)

        # All nodes have same badness → no tension → V_struct = 0
        bad = np.array([0.5, 0.5, 0.5])
        V_struct = compute_structural_potential(graph.L, bad)
        assert np.abs(V_struct) < 1e-10, "Uniform badness should give V_struct ≈ 0"

        # One node different → tension
        bad = np.array([1.0, 0.0, 0.0])
        V_struct = compute_structural_potential(graph.L, bad)
        assert V_struct > 0, "Non-uniform badness should give V_struct > 0"

    def test_business_potential(self):
        """Test business potential calculation."""
        demand = {'A': 1.0, 'B': 0.5, 'C': 0.0}
        health = {'A': 1.0, 'B': 0.5, 'C': 0.0}  # A healthy, B medium, C unhealthy
        complexity = {'A': 0.0, 'B': 0.5, 'C': 1.0}

        V_bus = compute_business_potential(demand, health, complexity, λ1=0.6, λ2=0.4)

        # A: high demand, high health, low complexity → low contribution
        # C: no demand → zero contribution
        # B: medium demand, medium health, medium complexity → medium contribution
        assert V_bus > 0, "Should have positive business potential"

    def test_kinetic_energy_uniform_mass(self):
        """Test kinetic energy with uniform mass (MVP default)."""
        bad_curr = np.array([0.6, 0.4, 0.5])
        bad_prev = np.array([0.5, 0.5, 0.5])

        # T = 0.5 * sum((delta_bad)^2)
        # delta = [0.1, -0.1, 0.0]
        # T = 0.5 * (0.01 + 0.01 + 0) = 0.01
        T = compute_kinetic_energy(bad_curr, bad_prev, mass=None)

        expected = 0.5 * (0.1**2 + 0.1**2 + 0.0**2)
        assert np.abs(T - expected) < 1e-10

    def test_kinetic_energy_no_change(self):
        """Test kinetic energy is zero when no change."""
        bad = np.array([0.5, 0.5, 0.5])

        T = compute_kinetic_energy(bad, bad, mass=None)
        assert np.abs(T) < 1e-10, "No change should give T = 0"

    def test_local_dirichlet_energy(self):
        """Test local energy calculation."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1.0), ('A', 'C', 1.0)]
        graph = TensegrityGraph(nodes, edges)

        bad = {'A': 1.0, 'B': 0.0, 'C': 0.0}

        # E_local[A] = 0.5 * [1.0*(1-0)^2 + 1.0*(1-0)^2] = 1.0
        E_A = compute_local_dirichlet_energy(graph.G, bad, 'A')
        assert np.abs(E_A - 1.0) < 1e-10

        # E_local[B] = 0.5 * [1.0*(0-1)^2] = 0.5
        E_B = compute_local_dirichlet_energy(graph.G, bad, 'B')
        assert np.abs(E_B - 0.5) < 1e-10


class TestSimulationState:
    """Test simulation state management."""

    def test_state_initialization(self):
        """Test state initialization with all required fields."""
        nodes = ['A', 'B']
        edges = [('A', 'B', 1.0)]
        graph = TensegrityGraph(nodes, edges)

        health = {'A': 1.0, 'B': 0.8}
        complexity = {'A': 0.2, 'B': 0.4}
        demand = {'A': 0.5, 'B': 0.5}

        state = SimulationState(
            graph=graph,
            health=health,
            complexity=complexity,
            demand=demand
        )

        assert state.time_step == 0
        assert state.H == 0.0  # Not computed yet

    def test_risk_computation(self):
        """Test risk field computation (CONFUSION #2)."""
        nodes = ['A', 'B']
        edges = [('A', 'B', 1.0)]
        graph = TensegrityGraph(nodes, edges)

        # A: healthy, high complexity → low risk
        # B: unhealthy, high complexity → high risk
        health = {'A': 0.9, 'B': 0.2}
        complexity = {'A': 0.8, 'B': 0.8}
        demand = {'A': 0.5, 'B': 0.5}

        state = SimulationState(
            graph=graph,
            health=health,
            complexity=complexity,
            demand=demand
        )

        state.update_derived_fields()

        # risk = complexity * (1 - health)
        assert np.abs(state.risk['A'] - 0.8 * 0.1) < 1e-10
        assert np.abs(state.risk['B'] - 0.8 * 0.8) < 1e-10

    def test_badness_computation(self):
        """Test badness field computation."""
        nodes = ['A']
        edges = []
        graph = TensegrityGraph(nodes, edges)

        health = {'A': 0.5}
        complexity = {'A': 0.6}
        demand = {'A': 0.5}

        state = SimulationState(
            graph=graph,
            health=health,
            complexity=complexity,
            demand=demand
        )

        state.update_derived_fields(α=0.4, β=0.3, γ=0.3)

        # bad = α*(1-health) + β*complexity + γ*risk
        # risk = complexity * (1 - health) = 0.6 * 0.5 = 0.3
        # bad = 0.4*0.5 + 0.3*0.6 + 0.3*0.3 = 0.2 + 0.18 + 0.09 = 0.47
        expected_bad = 0.4 * 0.5 + 0.3 * 0.6 + 0.3 * 0.3
        assert np.abs(state.bad['A'] - expected_bad) < 1e-10

    def test_energy_update(self):
        """Test that update_energies computes H correctly."""
        nodes = ['A', 'B']
        edges = [('A', 'B', 1.0)]
        graph = TensegrityGraph(nodes, edges)

        health = {'A': 1.0, 'B': 0.5}
        complexity = {'A': 0.2, 'B': 0.6}
        demand = {'A': 0.5, 'B': 0.5}

        state = SimulationState(
            graph=graph,
            health=health,
            complexity=complexity,
            demand=demand
        )

        state.update_derived_fields()
        state.update_energies()

        # H = T + V should be computed
        assert state.H >= 0
        assert state.T >= 0
        assert state.V >= 0
        assert np.abs(state.H - (state.T + state.V)) < 1e-10

    def test_step_forward(self):
        """Test time step advancement."""
        nodes = ['A']
        edges = []
        graph = TensegrityGraph(nodes, edges)

        state = SimulationState(
            graph=graph,
            health={'A': 1.0},
            complexity={'A': 0.5},
            demand={'A': 0.5}
        )

        state.update_derived_fields()
        initial_bad = state.bad.copy()

        state.step_forward()

        assert state.time_step == 1
        assert state.bad_prev == initial_bad

    def test_incident_recording(self):
        """Test incident tracking."""
        nodes = ['A']
        edges = []
        graph = TensegrityGraph(nodes, edges)

        state = SimulationState(
            graph=graph,
            health={'A': 1.0},
            complexity={'A': 0.5},
            demand={'A': 0.5}
        )

        state.update_derived_fields()
        state.update_energies()

        assert len(state.incidents) == 0

        state.record_incident('A', 'bug', severity=0.8)
        assert len(state.incidents) == 1
        assert state.incidents[0]['node'] == 'A'
        assert state.incidents[0]['type'] == 'bug'

    def test_high_risk_nodes(self):
        """Test high risk node identification."""
        nodes = ['A', 'B', 'C']
        edges = []
        graph = TensegrityGraph(nodes, edges)

        health = {'A': 1.0, 'B': 0.5, 'C': 0.1}
        complexity = {'A': 0.1, 'B': 0.5, 'C': 0.9}
        demand = {'A': 0.5, 'B': 0.5, 'C': 0.5}

        state = SimulationState(
            graph=graph,
            health=health,
            complexity=complexity,
            demand=demand
        )

        state.update_derived_fields()

        # C should have high badness (unhealthy + complex)
        high_risk = state.get_high_risk_nodes(threshold=0.5)
        assert 'C' in high_risk


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

#!/usr/bin/env python3
"""
Generate diagrams for mathematical concepts in Tensegrity foundations.

Visualizes:
- Coordination complexity (n² growth)
- Knowledge divergence over time
- LP feasible region and simplex navigation
- Lyapunov stability (energy function)
- Multi-layer verification security
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
import matplotlib.patches as mpatches

plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'primary': '#2196F3',
    'secondary': '#7B1FA2',
    'accent': '#F57C00',
    'success': '#388E3C',
    'danger': '#D32F2F',
    'neutral': '#757575'
}


def generate_coordination_complexity():
    """
    Visualize O(n²) coordination complexity vs O(n) with infrastructure.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    n_values = np.arange(1, 21)
    coord_without = n_values ** 2  # O(n²)
    coord_with = 2 * n_values      # O(n)

    # Left: Comparison
    ax1.plot(n_values, coord_without, 'o-', linewidth=2.5, markersize=8,
             color=colors['danger'], label='Without infrastructure: Θ(n²)')
    ax1.plot(n_values, coord_with, 's-', linewidth=2.5, markersize=8,
             color=colors['success'], label='With infrastructure: O(n)')

    ax1.fill_between(n_values, coord_with, coord_without, alpha=0.2, color=colors['danger'])

    ax1.set_xlabel('Number of Agents (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Coordination Messages', fontsize=12, fontweight='bold')
    ax1.set_title('Coordination Complexity', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Annotate gap
    n_highlight = 15
    gap = coord_without[n_highlight-1] - coord_with[n_highlight-1]
    ax1.annotate(f'Gap: {gap} messages\nat n={n_highlight}',
                xy=(n_highlight, coord_without[n_highlight-1]),
                xytext=(n_highlight-3, coord_without[n_highlight-1]-50),
                fontsize=10,
                arrowprops=dict(arrowstyle='->', lw=1.5, color=colors['danger']))

    # Right: Asymptotic comparison
    n_large = np.arange(1, 101)
    ratio = n_large  # n²/n = n

    ax2.plot(n_large, ratio, linewidth=3, color=colors['primary'])
    ax2.fill_between(n_large, 0, ratio, alpha=0.2, color=colors['primary'])

    ax2.set_xlabel('Number of Agents (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Speedup Factor (Θ(n²)/O(n))', fontsize=12, fontweight='bold')
    ax2.set_title('Infrastructure Benefit Grows Linearly', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    ax2.text(50, 50, 'Benefit = Θ(n)', fontsize=12, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5))

    plt.tight_layout()
    plt.savefig('coordination_complexity_math.png', dpi=300, bbox_inches='tight')
    plt.savefig('coordination_complexity_math.svg', bbox_inches='tight')
    print("✓ Generated: coordination_complexity_math.{png,svg}")
    plt.close()


def generate_knowledge_divergence():
    """
    Visualize unbounded knowledge divergence without active learning.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    t = np.linspace(0, 24, 200)  # 24 months

    # Agent velocity (exponential growth, 7-month doubling)
    alpha = np.log(2) / 7  # doubling constant
    lambda_agent = 10 * np.exp(alpha * t)

    # Knowledge required (integral of agent velocity)
    K_t = (10 / alpha) * (np.exp(alpha * t) - 1)

    # Human knowledge without active learning (linear growth)
    lambda_human_passive = 15
    H_passive = lambda_human_passive * t

    # Human knowledge with active learning (amplified by β=3)
    beta = 3
    lambda_human_active = beta * lambda_human_passive
    H_active = lambda_human_active * t

    # Knowledge gap
    G_passive = K_t - H_passive
    G_active = K_t - H_active

    # Plot
    ax.plot(t, K_t, linewidth=3, color=colors['primary'], label='Knowledge Required: K(t)')
    ax.plot(t, H_passive, '--', linewidth=2.5, color=colors['danger'],
            label='Human Knowledge (passive): H_passive(t)')
    ax.plot(t, H_active, '--', linewidth=2.5, color=colors['success'],
            label='Human Knowledge (active learning): H_active(t)')

    # Shade gaps
    ax.fill_between(t, H_passive, K_t, alpha=0.2, color=colors['danger'],
                    label='Gap (passive) → ∞')
    ax.fill_between(t, H_active, K_t, alpha=0.15, color=colors['accent'],
                    where=(K_t > H_active), label='Gap (active) → bounded')

    ax.set_xlabel('Time (months)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Knowledge (arbitrary units)', fontsize=12, fontweight='bold')
    ax.set_title('Knowledge Divergence: Theorem 3.1', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 24)

    # Annotate divergence
    ax.annotate('Without active learning:\nG(t) → ∞',
                xy=(18, G_passive[180]), xytext=(12, 1500),
                fontsize=11, color=colors['danger'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['danger']))

    ax.annotate('With active learning:\nG(t) bounded',
                xy=(18, G_active[180]), xytext=(15, 200),
                fontsize=11, color=colors['success'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['success']))

    plt.tight_layout()
    plt.savefig('knowledge_divergence_math.png', dpi=300, bbox_inches='tight')
    plt.savefig('knowledge_divergence_math.svg', bbox_inches='tight')
    print("✓ Generated: knowledge_divergence_math.{png,svg}")
    plt.close()


def generate_lp_feasible_region():
    """
    Visualize LP feasible region and simplex navigation.
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Feasible region (2D: velocity and quality forces)
    vertices = np.array([[0, 0], [8, 0], [7, 4], [5, 7], [0, 9]])
    poly = Polygon(vertices, alpha=0.2, facecolor=colors['primary'],
                   edgecolor=colors['primary'], linewidth=3)
    ax.add_patch(poly)

    # Draw vertices
    for v in vertices:
        ax.plot(v[0], v[1], 'o', markersize=12, color=colors['primary'],
                markeredgecolor='black', markeredgewidth=2, zorder=5)

    # Simplex path
    simplex_path = np.array([[0, 0], [8, 0], [7, 4], [5, 7]])
    ax.plot(simplex_path[:, 0], simplex_path[:, 1], 'r->', linewidth=3, markersize=10,
            label='Simplex path', zorder=4)

    # Optimal point
    f_star = simplex_path[-1]
    ax.plot(f_star[0], f_star[1], '*', markersize=25, color='gold',
            markeredgecolor='red', markeredgewidth=2, zorder=6,
            label='f* (optimal)')

    # Draw constraint lines
    x = np.linspace(0, 10, 100)

    # Constraint 1: f_v + f_q ≤ 12
    c1 = 12 - x
    ax.plot(x, c1, '--', linewidth=2, color=colors['secondary'], alpha=0.7,
            label='Constraint: f_v + f_q ≤ 12')

    # Constraint 2: Resource constraint
    c2 = 9 - 0.5*x
    ax.plot(x, c2, '--', linewidth=2, color=colors['accent'], alpha=0.7,
            label='Resource constraint')

    # Objective function gradients
    for c in [20, 30, 40]:
        obj = c - 2*x
        ax.plot(x, obj, ':', linewidth=1, color='gray', alpha=0.5)

    ax.text(9, 40-2*9, 'value = 2f_v + f_q', fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    # Labels
    ax.set_xlabel('Velocity Force (f_v)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Quality Force (f_q)', fontsize=13, fontweight='bold')
    ax.set_title('LP Feasible Region and Simplex Navigation: Theorem 5.1',
                fontsize=14, fontweight='bold')
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-0.5, 10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    # Annotate vertices
    vertex_labels = ['Origin', 'Max velocity', 'Iteration 2', 'f* (optimal)', 'Max quality']
    for i, (v, label) in enumerate(zip(vertices, vertex_labels)):
        if i < 4:
            ax.annotate(f'{i}: {label}', xy=v, xytext=(v[0]+0.3, v[1]+0.5),
                       fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6))

    plt.tight_layout()
    plt.savefig('lp_feasible_region.png', dpi=300, bbox_inches='tight')
    plt.savefig('lp_feasible_region.svg', bbox_inches='tight')
    print("✓ Generated: lp_feasible_region.{png,svg}")
    plt.close()


def generate_lyapunov_stability():
    """
    Visualize Lyapunov energy function.
    """
    fig = plt.figure(figsize=(12, 5))

    # Left: 2D contour plot
    ax1 = fig.add_subplot(121)

    f1 = np.linspace(-3, 3, 100)
    f2 = np.linspace(-3, 3, 100)
    F1, F2 = np.meshgrid(f1, f2)

    # Lyapunov function: V(f) = ½||f - f*||²
    f_star = np.array([1, 1])
    V = 0.5 * ((F1 - f_star[0])**2 + (F2 - f_star[1])**2)

    contour = ax1.contour(F1, F2, V, levels=15, cmap='viridis')
    ax1.clabel(contour, inline=True, fontsize=8)
    ax1.plot(f_star[0], f_star[1], '*', markersize=20, color='red',
            markeredgecolor='darkred', markeredgewidth=2,
            label='f* (equilibrium)', zorder=5)

    # Draw trajectory converging to equilibrium
    t = np.linspace(0, 5, 50)
    traj_f1 = f_star[0] + 2*np.exp(-0.5*t)*np.cos(t)
    traj_f2 = f_star[1] + 2*np.exp(-0.5*t)*np.sin(t)
    ax1.plot(traj_f1, traj_f2, 'r-', linewidth=2, alpha=0.7, label='Trajectory')
    ax1.arrow(traj_f1[10], traj_f2[10],
             traj_f1[11]-traj_f1[10], traj_f2[11]-traj_f2[10],
             head_width=0.1, head_length=0.15, fc='red', ec='red')

    ax1.set_xlabel('Force f₁', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Force f₂', fontsize=12, fontweight='bold')
    ax1.set_title('Lyapunov Function: V(f) = ½||f - f*||²', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')

    # Right: Energy over time
    ax2 = fig.add_subplot(122)

    V_t = 2 * np.exp(-t)  # V decreases exponentially
    ax2.plot(t, V_t, linewidth=3, color=colors['primary'])
    ax2.fill_between(t, 0, V_t, alpha=0.2, color=colors['primary'])

    ax2.axhline(0, color='red', linestyle='--', linewidth=2,
               label='V(f*) = 0 (equilibrium)')

    ax2.set_xlabel('Time t', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Lyapunov Function V(t)', fontsize=12, fontweight='bold')
    ax2.set_title('Energy Decreases → Stability: dV/dt < 0', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Annotate dV/dt < 0
    ax2.text(2.5, 0.5, 'dV/dt < 0\n(Theorem 6.1)', fontsize=12, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.6),
            fontweight='bold')

    plt.tight_layout()
    plt.savefig('lyapunov_stability.png', dpi=300, bbox_inches='tight')
    plt.savefig('lyapunov_stability.svg', bbox_inches='tight')
    print("✓ Generated: lyapunov_stability.{png,svg}")
    plt.close()


def generate_multilayer_verification():
    """
    Visualize exponential security in multi-layer verification.
    """
    fig, ax = plt.subplots(figsize=(11, 7))

    layers = np.arange(1, 11)
    epsilon = 0.3  # False negative rate per layer

    success_prob = epsilon ** layers

    ax.semilogy(layers, success_prob, 'o-', linewidth=3, markersize=10,
               color=colors['danger'], label='P(exploit succeeds)')
    ax.axhline(0.01, color='green', linestyle='--', linewidth=2,
              label='1% threshold', alpha=0.7)
    ax.axhline(0.001, color='darkgreen', linestyle='--', linewidth=2,
              label='0.1% threshold', alpha=0.7)

    # Shade safe region
    ax.fill_between(layers, 0.0001, 0.01, alpha=0.1, color='green',
                    label='Safe region')

    ax.set_xlabel('Number of Verification Layers (k)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability of Successful Exploit', fontsize=12, fontweight='bold')
    ax.set_title('Multi-Layer Verification Security: P(exploit) = ε^k (Proposition 4.2)',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_ylim(1e-6, 1)

    # Annotate exponential drop
    ax.annotate('Exponential\nsecurity in k',
                xy=(5, epsilon**5), xytext=(7, 0.1),
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.6),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    # Add formula
    ax.text(5, 1e-5, 'P(all layers pass | defect) = ε^k\nFor ε = 0.3, k = 5 → P ≈ 0.2%',
           fontsize=11, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor='black', linewidth=2))

    plt.tight_layout()
    plt.savefig('multilayer_verification.png', dpi=300, bbox_inches='tight')
    plt.savefig('multilayer_verification.svg', bbox_inches='tight')
    print("✓ Generated: multilayer_verification.{png,svg}")
    plt.close()


if __name__ == '__main__':
    print("Generating mathematical concept diagrams...\n")

    generate_coordination_complexity()
    generate_knowledge_divergence()
    generate_lp_feasible_region()
    generate_lyapunov_stability()
    generate_multilayer_verification()

    print("\n✓ All diagrams generated successfully!")
    print("  Location: docs/assets/images/math/")
    print("  Formats: PNG (300 DPI) and SVG (vector)")

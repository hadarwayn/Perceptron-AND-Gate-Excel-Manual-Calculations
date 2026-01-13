#!/usr/bin/env python3
"""
Create FUN, colorful visualizations for Perceptron Learning!
Generates 4 educational graphs that show how the perceptron works.

Usage: python create_visualizations.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path


# Color scheme matching Excel
COLORS = {
    'blue': '#4472C4',
    'yellow': '#FFF2CC',
    'purple': '#E2D0F8',
    'green': '#C6EFCE',
    'red': '#FFC7CE',
    'orange': '#FCE4D6',
}


def run_perceptron_training(initial_weights=(3, 3, 3), iterations=20):
    """
    Run the perceptron learning algorithm on AND gate data.
    Returns the history of weights and predictions for visualization.
    """
    # AND gate truth table: [x0(bias), x1, x2, output]
    truth_table = np.array([
        [1, 0, 0, 0],  # OFF + OFF = OFF
        [1, 0, 1, 0],  # OFF + ON = OFF
        [1, 1, 0, 0],  # ON + OFF = OFF
        [1, 1, 1, 1],  # ON + ON = ON!
    ])

    weights = np.array(initial_weights, dtype=float)
    history = {'weights': [weights.copy()], 'errors': [], 'correct': []}

    for i in range(iterations):
        sample_idx = i % 4
        x = truth_table[sample_idx, :3]  # x0, x1, x2
        actual = truth_table[sample_idx, 3]

        z = np.dot(weights, x)  # Dot product
        predicted = 1 if z > 0 else 0
        error = actual - predicted

        history['errors'].append(error)
        history['correct'].append(error == 0)

        # Update weights: W_new = W_old + error * x
        weights = weights + error * x
        history['weights'].append(weights.copy())

    return history


def create_perceptron_diagram(output_path):
    """Create a beautiful diagram showing perceptron architecture."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('The Perceptron - A Simple "Brain"', fontsize=18, fontweight='bold', pad=20)

    # Input nodes
    inputs = [('x0=1\n(Bias)', 6), ('x1', 4), ('x2', 2)]
    for label, y in inputs:
        circle = plt.Circle((1.5, y), 0.5, color=COLORS['purple'], ec='black', lw=2)
        ax.add_patch(circle)
        ax.text(1.5, y, label, ha='center', va='center', fontsize=11, fontweight='bold')

    # Weights on arrows
    weights = ['W0', 'W1', 'W2']
    for i, (w, (_, y)) in enumerate(zip(weights, inputs)):
        ax.annotate('', xy=(4, 4), xytext=(2, y),
                    arrowprops=dict(arrowstyle='->', color=COLORS['blue'], lw=2))
        ax.text(2.8, y + 0.3 + (i - 1) * 0.2, w, fontsize=12, fontweight='bold',
                color=COLORS['blue'], bbox=dict(boxstyle='round', facecolor=COLORS['yellow']))

    # Summation node
    circle = plt.Circle((4.5, 4), 0.6, color=COLORS['orange'], ec='black', lw=2)
    ax.add_patch(circle)
    ax.text(4.5, 4, 'Sum', ha='center', va='center', fontsize=12, fontweight='bold')

    # Arrow to activation
    ax.annotate('', xy=(6.5, 4), xytext=(5.1, 4),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(5.8, 4.4, 'Z = W*X', fontsize=10, ha='center')

    # Activation (step function)
    rect = mpatches.FancyBboxPatch((6.5, 3.3), 1.5, 1.4, boxstyle="round,pad=0.1",
                                    facecolor=COLORS['blue'], edgecolor='black', lw=2)
    ax.add_patch(rect)
    ax.text(7.25, 4, 'Step\nFunction', ha='center', va='center', fontsize=10,
            fontweight='bold', color='white')

    # Arrow to output
    ax.annotate('', xy=(9, 4), xytext=(8, 4),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Output node
    circle = plt.Circle((9.3, 4), 0.5, color=COLORS['green'], ec='black', lw=2)
    ax.add_patch(circle)
    ax.text(9.3, 4, 'Out', ha='center', va='center', fontsize=11, fontweight='bold')

    # Explanation box
    explanation = ("How it works:\n"
                   "1. Multiply each input by its weight\n"
                   "2. Add them all up (Z = W0*x0 + W1*x1 + W2*x2)\n"
                   "3. If Z > 0, output 1 (YES!)\n"
                   "   If Z <= 0, output 0 (NO!)")
    ax.text(5, 1.2, explanation, fontsize=11, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_path}")


def create_decision_boundary(output_path):
    """Create 2D plot showing AND gate points and decision boundary."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # AND gate points
    points_0 = [(0, 0), (0, 1), (1, 0)]  # Output = 0
    points_1 = [(1, 1)]  # Output = 1

    # Plot points
    for x1, x2 in points_0:
        ax.scatter(x1, x2, c='red', s=300, marker='o', edgecolors='black', linewidth=2, zorder=5)
        ax.annotate(f'({x1},{x2})=0', (x1 + 0.05, x2 + 0.1), fontsize=12)

    for x1, x2 in points_1:
        ax.scatter(x1, x2, c='green', s=300, marker='s', edgecolors='black', linewidth=2, zorder=5)
        ax.annotate(f'({x1},{x2})=1', (x1 + 0.05, x2 + 0.1), fontsize=12, fontweight='bold')

    # Decision boundary: W0 + W1*x1 + W2*x2 = 0
    # After learning, typical weights might be W0=-1, W1=1, W2=1
    # So: -1 + x1 + x2 = 0 => x2 = 1 - x1
    x1_line = np.linspace(-0.2, 1.5, 100)
    x2_line = 1 - x1_line  # This is the decision line

    ax.plot(x1_line, x2_line, 'b--', linewidth=2, label='Decision Boundary')
    ax.fill_between(x1_line, x2_line, 1.5, alpha=0.2, color='green', label='Output = 1 region')
    ax.fill_between(x1_line, -0.5, x2_line, alpha=0.2, color='red', label='Output = 0 region')

    ax.set_xlim(-0.3, 1.5)
    ax.set_ylim(-0.3, 1.5)
    ax.set_xlabel('x1 (Input 1)', fontsize=14)
    ax.set_ylabel('x2 (Input 2)', fontsize=14)
    ax.set_title('AND Gate: Decision Boundary\nOnly (1,1) is in the "YES" region!', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_path}")


def create_weight_evolution(history, output_path):
    """Create line chart showing how weights change over iterations."""
    weights = np.array(history['weights'])
    iterations = range(len(weights))

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(iterations, weights[:, 0], 'b-o', linewidth=2, markersize=6, label='W0 (Bias Weight)')
    ax.plot(iterations, weights[:, 1], 'g-s', linewidth=2, markersize=6, label='W1 (x1 Weight)')
    ax.plot(iterations, weights[:, 2], 'r-^', linewidth=2, markersize=6, label='W2 (x2 Weight)')

    ax.set_xlabel('Iteration', fontsize=14)
    ax.set_ylabel('Weight Value', fontsize=14)
    ax.set_title('Weight Evolution: Watch the Brain Learn!\nWeights adjust with each mistake', fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Add annotations
    ax.annotate('Starting\nweights', xy=(0, weights[0, 0]), xytext=(1, weights[0, 0] + 0.5),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)
    ax.annotate('Final\nweights', xy=(len(weights) - 1, weights[-1, 0]),
                xytext=(len(weights) - 3, weights[-1, 0] + 0.5),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_path}")


def create_learning_progress(history, output_path):
    """Create bar chart showing errors per epoch (4 samples = 1 epoch)."""
    errors = history['errors']
    epochs = len(errors) // 4  # 4 samples per epoch

    errors_per_epoch = []
    for i in range(epochs):
        epoch_errors = sum(1 for e in errors[i * 4:(i + 1) * 4] if e != 0)
        errors_per_epoch.append(epoch_errors)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['red' if e > 0 else 'green' for e in errors_per_epoch]
    bars = ax.bar(range(1, epochs + 1), errors_per_epoch, color=colors, edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Epoch (1 epoch = 4 samples)', fontsize=14)
    ax.set_ylabel('Number of Errors', fontsize=14)
    ax.set_title('Learning Progress: Errors Decrease Over Time!\nGreen = No errors in that epoch', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 5)
    ax.set_xticks(range(1, epochs + 1))
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, val in zip(bars, errors_per_epoch):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(val), ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Created: {output_path}")


def main():
    """Generate all visualizations."""
    print("Generating Perceptron visualizations...\n")

    output_dir = Path(__file__).parent / "results" / "graphs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run perceptron training to get data
    history = run_perceptron_training(initial_weights=(3, 3, 3), iterations=20)

    # Create all graphs
    create_perceptron_diagram(output_dir / "perceptron_diagram.png")
    create_decision_boundary(output_dir / "decision_boundary.png")
    create_weight_evolution(history, output_dir / "weight_evolution.png")
    create_learning_progress(history, output_dir / "learning_progress.png")

    print(f"\nAll visualizations saved to: {output_dir}")


if __name__ == "__main__":
    main()

# Import native simulation backends
from qiskit_aer import AerSimulator
from qiskit import transpile

# Import your custom project modules
from components.signal_generator import (
    generate_eeg_signal_8,
    generate_eeg_signal_32,
    generate_eeg_signal_128,
)
from components.quantum_circuits import (
    build_qft_circuit_3qb,
    build_qft_circuit_5qb,
    build_qft_circuit_7qb,
)
from components.metrics_analyzer import evaluate_and_plot

import os
import matplotlib.pyplot as plt
import re

os.makedirs("figures", exist_ok=True)

def run_experiment(title, signal_generator, circuit_builder):
    print(f"\n{'=' * 60}")
    print(title)
    print(f"{'=' * 60}")

    # Generate biological signal
    time, raw_signal, normalized_amplitudes,  wave_7hz, wave_15hz = signal_generator()

    # Build circuits
    circuit_standard = circuit_builder(normalized_amplitudes, truncate=False)
    circuit_truncated = circuit_builder(normalized_amplitudes, truncate=True)

    # Print Circuits
    print("\nStandard QFT Circuit:")

    # Print the exact gate breakdown for your Standard QFT
    print("Standard QFT Gates:", circuit_standard.count_ops())
    print(circuit_standard)

    print("\nTruncated QFT Circuit:")

    # Print the exact gate breakdown for your Truncated QFT
    print("Truncated QFT Gates:", circuit_truncated.count_ops())
    print(circuit_truncated)

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", title)

    fig = circuit_standard.draw(output="mpl", fold=-1)
    fig.savefig(
        f"figures/{safe_name}_standard_qft_circuit.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    fig = circuit_truncated.draw(output="mpl", fold=-1)
    fig.savefig(
        f"figures/{safe_name}_truncated_qft_circuit.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    # Simulator
    backend = AerSimulator()

    # Run Standard QFT
    compiled_std = transpile(circuit_standard, backend)
    result_std = backend.run(compiled_std, shots=1024).result()

    # Run Truncated QFT
    compiled_trunc = transpile(circuit_truncated, backend)
    result_trunc = backend.run(compiled_trunc, shots=1024).result()

    # Analyze results
    evaluate_and_plot(
        time,
        raw_signal,
        circuit_standard,
        circuit_truncated,
        result_std,
        result_trunc,
        title,
        wave_7hz,
        wave_15hz
    )


def main():

    # Experiment 1: 8-point EEG using 3 qubits
    run_experiment(
        "8-Sample EEG (3-Qubit QFT)",
        generate_eeg_signal_8,
        build_qft_circuit_3qb,
    )

    # Experiment 2: 32-point EEG using 5 qubits
    run_experiment(
        "32-Sample EEG (5-Qubit QFT)",
        generate_eeg_signal_32,
        build_qft_circuit_5qb,
    )

    # Experiment 3: 128-point EEG using 5 qubits
    run_experiment(
        "128-Sample EEG (7-Qubit QFT)",
        generate_eeg_signal_128,
        build_qft_circuit_7qb,
    )

if __name__ == "__main__":
    main()
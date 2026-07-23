import matplotlib.pyplot as plt
import numpy as np
from qiskit.visualization import plot_histogram
from qiskit import transpile 
from qiskit import QuantumCircuit
import os
import re
from scipy.fft import fft, fftfreq

os.makedirs("figures", exist_ok=True)
# Update import for Hellinger distance to compatible locations or custom computing 
# from scipy.spatial.distance import total_variation_distance 
 

def evaluate_and_plot(time, raw_signal, qc_standard, qc_truncated, result_std, result_trunc, experiment_name, wave_7hz, wave_15hz): 
    """ 
    Computes presentation-ready metrics and plots the experimental results. 
    """ 
    # --- Print Engineering Metrics --- 
    print("==================================================") 
    print("        QUANTUM ARCHITECTURE OPTIMIZATION METRICS ") 
    print("==================================================") 
    print(f"Standard Circuit Depth:  {qc_standard.depth()}") 
    print(f"Truncated Circuit Depth: {qc_truncated.depth()}") 
    depth_saved = ((qc_standard.depth() - qc_truncated.depth()) / qc_standard.depth()) * 100 
    print(f"Circuit Depth Reduction: {depth_saved:.1f}%") 
     
    # Total Gate Count (Operations) 
    print(f"Standard Gate Counts:  {dict(qc_standard.count_ops())}") 
    print(f"Truncated Gate Counts: {dict(qc_truncated.count_ops())}") 
    print("==================================================\n") 
 
    # --- Text-based prinout of circuit diagrams. Need to work on qc_standard.draw (output="mpl") etc working (7/2/2026)
    print(qc_standard)
    print(qc_truncated)


# --- Plot 1: Neural Signal Input --- 
#Generate the side-by-side histogram figure
    plt.figure(figsize=(8, 3)) 
    plt.plot(time, raw_signal, '-o', color='purple', label='Continuous EEG Signal') 
    plt.title(f"{experiment_name} - Time-Domain Synthetic Brainwave Data")
    plt.xlabel("Time (seconds)") 
    plt.ylabel("Amplitude (arbitrary units)") 
    plt.grid(True) 
    plt.legend() 
    plt.tight_layout()

    safe_name = experiment_name.lower().replace(" ", "_").replace("(", "").replace(")", "")

    plt.savefig(f"figures/{safe_name}_neural_signal.png")

# --- Plot: Frequency Components of EEG Signal ---

    num_samples = len(raw_signal)

    # Compute FFT
    fft_values = fft(raw_signal)

    # Frequency axis
    freqs = fftfreq(
        num_samples,
        d=(time[1] - time[0])
    )

    # Only keep positive frequencies
    positive_freqs = freqs[:num_samples // 2]
    positive_fft = np.abs(fft_values[:num_samples // 2])

    plt.figure(figsize=(8, 4))

    plt.plot(
        positive_freqs,
        positive_fft,
        color="purple",
        linewidth=2
    )

    plt.title(f"{experiment_name} - EEG Frequency Components")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(alpha=0.3)

    # Highlight expected frequency components
    plt.axvline(
        7,
        color="orange",
        linestyle="--",
        label="7 Hz Component"
    )

    plt.axvline(
        15,
        color="green",
        linestyle="--",
        label="15 Hz Component"
    )

    plt.legend()
    plt.tight_layout()

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", experiment_name)

    plt.savefig(
        f"figures/{safe_name}_frequency_components.png",
        dpi=300,
        bbox_inches="tight"
    )

# --- Plot: EEG Signal Components ---

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(10, 8),
        sharex=True
    )

    # 7 Hz component
    axes[0].plot(
        time,
        wave_7hz,
        color="#F07021",
        linewidth=2
    )

    axes[0].set_title("7 Hz EEG Component")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(alpha=0.3)


    # 15 Hz component
    axes[1].plot(
        time,
        wave_15hz,
        color="#00806B",
        linewidth=2
    )

    axes[1].set_title("15 Hz EEG Component")
    axes[1].set_ylabel("Amplitude")
    axes[1].grid(alpha=0.3)


    # Combined EEG signal
    axes[2].plot(
        time,
        raw_signal,
        color="purple",
        linewidth=2
    )

    axes[2].set_title("Combined Synthetic EEG Signal")
    axes[2].set_xlabel("Time (seconds)")
    axes[2].set_ylabel("Amplitude")
    axes[2].grid(alpha=0.3)


    fig.suptitle(
        f"{experiment_name} - EEG Signal Components",
        fontsize=14
    )

    plt.tight_layout()

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", experiment_name)

    plt.savefig(
        f"figures/{safe_name}_eeg_components.png",
        dpi=300,
        bbox_inches="tight"
    )

# --- Plot 2: Quantum Output Histograms --- 
    # Convert counts to probability distributions for distance calculation 
    # Express comparison as total variation distance 
    counts_std = result_std.get_counts() 
    counts_trunc = result_trunc.get_counts()
    # print(counts_std, counts_trunc)
     
    all_states = [format(i, '03b') for i in range(8)] 
    prob_std = [counts_std.get(s, 0) / 1024 for s in all_states] 
    prob_trunc = [counts_trunc.get(s, 0) / 1024 for s in all_states]
    tvd = 0.5 * np.sum(np.abs(np.array(prob_std) - np.array(prob_trunc))) 
    # tvd = total_variation_distance(prob_std, prob_trunc) 
     
    print(f"Statistical Distance (Total Variation Distance): {tvd:.4f}") 
    print("A value close to 0 proves the optimized circuit did not compromise frequency integrity!")

    # Generate the side-by-side histogram figure
    hist = plot_histogram(
        [counts_std, counts_trunc],
          legend=['Standard QFT (Control)', 'Truncated QFT (Optimized)'],
          color=["#F07021", "#00806B"]
    )

    # --- Add your labels and title here ---
    ax = hist.axes[0]
    ax.set_xlabel("Computational Basis States")
    ax.set_ylabel("Count")
    ax.set_title(f"{experiment_name} - Quantum Fourier Transform Output Comparison")
    # --------------------------------------

    # Save the histogram directly to your current project folder
    hist.savefig(f"figures/{safe_name}_quantum_histogram.png")
    print("Histogram saved successfully as 'quantum_histogram.png' to 'figures' folder.")

    # --- Plot 3: Connected Scatter Trend Comparison ---

    # Order computational states
    all_states = sorted(set(counts_std.keys()) | set(counts_trunc.keys()))

    # Convert counts to probabilities
    prob_std = [
        counts_std.get(state, 0) / 1024
        for state in all_states
    ]

    prob_trunc = [
        counts_trunc.get(state, 0) / 1024
        for state in all_states
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        all_states,
        prob_std,
        marker="o",
        linewidth=2.5,
        color="#F07021",
        label="Standard QFT (Control)"
    )

    plt.plot(
        all_states,
        prob_trunc,
        marker="s",
        linestyle="--",
        linewidth=2.5,
        color="#00806B",
        label="Truncated QFT (Optimized)"
    )

    plt.fill_between(
        all_states,
        prob_std,
        prob_trunc,
        color="gray",
        alpha=0.15
    )

    plt.title(f"{experiment_name} - QFT Output Probability Comparison")
    plt.xlabel("Computational Basis State")
    plt.ylabel("Measurement Probability")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", experiment_name)

    plt.savefig(
        f"figures/{safe_name}_quantum_trend.png",
        dpi=300,
        bbox_inches="tight"
    )

    # --- Show both plots after they are saved to figures folder ---
    hist.show()
    print("hist.show ran")
    plt.show()
    print("plt.show ran")
 

# # Display side-by-side quantum histogram histograms 
#     display(plot_histogram([counts_std, counts_trunc],  
#                            legend=['Standard QFT (Control)', 'Truncated QFT (Optimized)'], 
#                            color=['#808080', '#008080'])) 

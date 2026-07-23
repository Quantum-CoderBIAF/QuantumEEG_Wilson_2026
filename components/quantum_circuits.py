import numpy as np
from qiskit import QuantumCircuit 
 

def build_qft_circuit_3qb(amplitudes, truncate=False): 
    """ 
    Creates a 3-qubit quantum circuit initialized with the EEG data. 
    Applies either a full standard QFT or a depth-optimized truncated QFT. 
    """ 
    # 3 qubits represent 8 data points; 3 classical bits for measurement 
    qc = QuantumCircuit(3, 3) 
     
    # Step 1: Load the classical EEG data amplitudes into the quantum state 
    # qc.initialize(amplitudes,)
    qc.initialize(amplitudes, [0, 1, 2])
    qc.barrier() # Visual separator in the circuit diagram 
     
    # Step 2: Custom 3-Qubit QFT Routine 
    # Qubit 2 
    qc.h(2) 
    qc.cp(np.pi / 2, 1, 2) 
     
    # The smallest gate: CP(pi/4) between Qubit 0 and 2 
    if not truncate: 
        qc.cp(np.pi / 4, 0, 2)  # Kept in the Control Group 
    else: 
        pass                    # Removed in the Experimental Group (Optimized) 
         
    # Qubit 1 
    qc.barrier() 
    qc.h(1) 
    qc.cp(np.pi / 2, 0, 1) 
     
    # Qubit 0 
    qc.barrier() 
    qc.h(0) 
     
    # Step 3: Swap gates to correct frequency ordering 
    qc.swap(0, 2) 
    qc.barrier() 
     
    # Step 4: Add measurements 
    # qc.measure(,) 
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc

def build_qft_circuit_5qb(amplitudes, truncate=False): 
    """ 
    Creates a 5-qubit quantum circuit initialized with the EEG data. 
    Applies either a full standard QFT or a depth-optimized truncated QFT. 
    """ 
    # 5 qubits represent 32 data points; 5 classical bits for measurement 
    qc = QuantumCircuit(5, 5) 
     
    # Step 1: Load the classical EEG data amplitudes into the quantum state 
    qc.initialize(amplitudes, [0, 1, 2, 3, 4])
    qc.barrier() # Visual separator in the circuit diagram 
     
    # Step 2: Custom 5-Qubit QFT Routine 
    
    # --- Qubit 4 ---
    qc.h(4) 
    qc.cp(np.pi / 2, 3, 4) 
    qc.cp(np.pi / 4, 2, 4) 
    if not truncate: 
        qc.cp(np.pi / 8, 1, 4)   # Removed if truncate=True
        qc.cp(np.pi / 16, 0, 4)  # Removed if truncate=True
    qc.barrier() 
     
    # --- Qubit 3 ---
    qc.h(3) 
    qc.cp(np.pi / 2, 2, 3) 
    qc.cp(np.pi / 4, 1, 3) 
    if not truncate: 
        qc.cp(np.pi / 8, 0, 3)   # Removed if truncate=True
    qc.barrier() 
     
    # --- Qubit 2 ---
    qc.h(2) 
    qc.cp(np.pi / 2, 1, 2) 
    qc.cp(np.pi / 4, 0, 2) 
    qc.barrier() 
     
    # --- Qubit 1 ---
    qc.h(1) 
    qc.cp(np.pi / 2, 0, 1) 
    qc.barrier() 
     
    # --- Qubit 0 ---
    qc.h(0) 
    qc.barrier() 
     
    # Step 3: Swap gates to correct frequency ordering (Mirror inversion)
    qc.swap(0, 4) 
    qc.swap(1, 3) 
    qc.barrier() 
     
    # Step 4: Add measurements 
    qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

    return qc

def build_qft_circuit_7qb(amplitudes, truncate=False):
    """
    Creates a 7-qubit quantum circuit initialized with the EEG data.
    Applies either a full standard QFT or a depth-optimized truncated QFT.
    """

    qc = QuantumCircuit(7, 7)

    # Step 1: Load the classical EEG data amplitudes
    qc.initialize(amplitudes, list(range(7)))
    qc.barrier()

    # ---------- Qubit 6 ----------
    qc.h(6)
    qc.cp(np.pi/2, 5, 6)
    qc.cp(np.pi/4, 4, 6)

    if not truncate:
        qc.cp(np.pi/8, 3, 6)
        qc.cp(np.pi/16, 2, 6)
        qc.cp(np.pi/32, 1, 6)
        qc.cp(np.pi/64, 0, 6)

    qc.barrier()

    # ---------- Qubit 5 ----------
    qc.h(5)
    qc.cp(np.pi/2, 4, 5)
    qc.cp(np.pi/4, 3, 5)

    if not truncate:
        qc.cp(np.pi/8, 2, 5)
        qc.cp(np.pi/16, 1, 5)
        qc.cp(np.pi/32, 0, 5)

    qc.barrier()

    # ---------- Qubit 4 ----------
    qc.h(4)
    qc.cp(np.pi/2, 3, 4)
    qc.cp(np.pi/4, 2, 4)

    if not truncate:
        qc.cp(np.pi/8, 1, 4)
        qc.cp(np.pi/16, 0, 4)

    qc.barrier()

    # ---------- Qubit 3 ----------
    qc.h(3)
    qc.cp(np.pi/2, 2, 3)
    qc.cp(np.pi/4, 1, 3)

    if not truncate:
        qc.cp(np.pi/8, 0, 3)

    qc.barrier()

    # ---------- Qubit 2 ----------
    qc.h(2)
    qc.cp(np.pi/2, 1, 2)
    qc.cp(np.pi/4, 0, 2)
    qc.barrier()

    # ---------- Qubit 1 ----------
    qc.h(1)
    qc.cp(np.pi/2, 0, 1)
    qc.barrier()

    # ---------- Qubit 0 ----------
    qc.h(0)
    qc.barrier()

    # Swap qubits
    qc.swap(0, 6)
    qc.swap(1, 5)
    qc.swap(2, 4)
    qc.barrier()

    # Measurements
    qc.measure(range(7), range(7))

    return qc
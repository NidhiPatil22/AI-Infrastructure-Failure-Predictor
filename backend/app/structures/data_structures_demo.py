"""
Data Structures in AIML Urban Infrastructure Failure Predictor
Demonstrates and benchmarks the 6 core data structures used throughout the system:
1. NumPy Vectors and Matrices (Dense numerical feature computing)
2. SciPy Sparse Matrices (Memory-efficient categorical feature encoding)
3. Decision Trees (Hierarchical non-linear decision partitioning)
4. Graphs (Infrastructure topological connectivity and cascading risk propagation)
5. Priority Queues (Heap-based emergency triage and asset prioritization)
6. Hash Dictionaries (O(1) asset ID-to-prediction indexing and caching)
"""
from __future__ import annotations

import heapq
import time
from typing import Any, Dict, List, Tuple

import networkx as nx
import numpy as np
import scipy.sparse as sp
from sklearn.tree import DecisionTreeClassifier, export_text


# -------------------------------------------------------------------------
# 1. NUMPY VECTORS AND MATRICES
# -------------------------------------------------------------------------
def demonstrate_numpy_structures() -> Dict[str, Any]:
    """
    Demonstrates NumPy 1D vectors (feature instances, weights) and 2D matrices (batch design matrix).
    Why appropriate:
    - Contiguous C-order memory layout enabling SIMD vectorization.
    - O(1) vectorized dot products for linear decision boundaries and Euclidean distance in K-Means.
    """
    # Sample asset feature vectors: [age, traffic_density, load, rainfall, corrosion]
    asset_features_matrix = np.array([
        [22.5, 78.4, 110.2, 1850.0, 45.2],
        [8.2, 34.1, 45.0, 920.0, 12.0],
        [18.9, 92.0, 135.5, 2100.0, 58.6],
        [4.5, 25.0, 30.0, 600.0, 5.0],
        [29.1, 85.0, 120.0, 1950.0, 62.1],
    ], dtype=np.float64)

    # Risk factor sensitivity weight vector
    weights_vector = np.array([0.25, 0.20, 0.20, 0.15, 0.20], dtype=np.float64)

    # Vectorized normalization: Z-score scaling across columns
    mean = np.mean(asset_features_matrix, axis=0)
    std = np.std(asset_features_matrix, axis=0) + 1e-8
    normalized_matrix = (asset_features_matrix - mean) / std

    # Matrix-vector multiplication for synthetic risk projection
    composite_risk_scores = np.dot(normalized_matrix, weights_vector)

    return {
        "structure": "NumPy 1D Vectors & 2D Matrices (ndarray)",
        "why_appropriate": "Enables cache-friendly SIMD vectorized linear algebra, feature standardization, and batch matrix operations with zero Python interpreter loop overhead.",
        "matrix_shape": list(asset_features_matrix.shape),
        "vector_shape": list(weights_vector.shape),
        "sample_matrix": asset_features_matrix.tolist(),
        "weights_vector": weights_vector.tolist(),
        "computed_scores": np.round(composite_risk_scores, 4).tolist(),
    }


# -------------------------------------------------------------------------
# 2. SCIPY SPARSE MATRICES
# -------------------------------------------------------------------------
def demonstrate_sparse_matrices(num_assets: int = 1000) -> Dict[str, Any]:
    """
    Demonstrates SciPy Compressed Sparse Row (CSR) matrices for high-cardinality categorical one-hot encoding.
    Why appropriate:
    - In urban infrastructure, one-hot encoding across multiple categorical attributes
      (asset_type x zone x material x subdistrict) produces high-dimensional binary vectors with >95% zero elements.
    - CSR matrices store only non-zero values, column indices, and row pointers, saving >90% memory.
    """
    np.random.seed(42)
    num_zones = 50
    # Simulate one-hot row where exactly 1 zone out of 50 is active per asset
    active_indices = np.random.randint(0, num_zones, size=num_assets)
    indptr = np.arange(num_assets + 1)
    indices = active_indices
    data = np.ones(num_assets, dtype=np.float32)

    # Create Compressed Sparse Row matrix
    csr_matrix = sp.csr_matrix((data, indices, indptr), shape=(num_assets, num_zones))
    dense_equivalent = csr_matrix.toarray()

    csr_memory_bytes = csr_matrix.data.nbytes + csr_matrix.indices.nbytes + csr_matrix.indptr.nbytes
    dense_memory_bytes = dense_equivalent.nbytes
    memory_savings_pct = round(((dense_memory_bytes - csr_memory_bytes) / dense_memory_bytes) * 100, 2)

    return {
        "structure": "SciPy CSR Sparse Matrix (scipy.sparse.csr_matrix)",
        "why_appropriate": "Compresses high-cardinality categorical one-hot encoded infrastructure matrices by storing only non-zero entries (values, column indices, row pointers), avoiding gigabytes of empty memory allocation.",
        "shape": list(csr_matrix.shape),
        "non_zero_elements": int(csr_matrix.nnz),
        "sparsity_percentage": round((1.0 - (csr_matrix.nnz / (num_assets * num_zones))) * 100, 2),
        "dense_memory_bytes": int(dense_memory_bytes),
        "sparse_memory_bytes": int(csr_memory_bytes),
        "memory_savings_pct": memory_savings_pct,
    }


# -------------------------------------------------------------------------
# 3. DECISION TREES
# -------------------------------------------------------------------------
def demonstrate_decision_trees() -> Dict[str, Any]:
    """
    Demonstrates supervised decision trees with explicit threshold splits.
    Why appropriate:
    - Provides human-interpretable orthogonal axis partitions:
      if (corrosion > 45.0 and age > 15.0) -> High Failure Risk.
    - Enables root-cause explanations directly mapped to engineering guidelines.
    """
    X = np.array([
        [5.0, 10.0],   # Young, Low Corrosion -> No Failure (0)
        [8.0, 25.0],   # Young, Medium Corrosion -> No Failure (0)
        [22.0, 65.0],  # Old, High Corrosion -> Failure (1)
        [28.0, 75.0],  # Old, Very High Corrosion -> Failure (1)
        [15.0, 42.0],  # Mid, Medium Corrosion -> Failure (1)
        [12.0, 15.0],  # Mid, Low Corrosion -> No Failure (0)
        [25.0, 30.0],  # Old, Low Corrosion -> No Failure (0)
        [19.0, 58.0],  # Mid-Old, High Corrosion -> Failure (1)
    ])
    y = np.array([0, 0, 1, 1, 1, 0, 0, 1])
    feature_names = ["age_years", "corrosion_level"]

    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X, y)
    tree_rules = export_text(clf, feature_names=feature_names)

    return {
        "structure": "Binary Decision Tree (sklearn.tree.DecisionTreeClassifier)",
        "why_appropriate": "Constructs a transparent hierarchical directed acyclic graph of orthogonal threshold rules, giving interpretable failure attribution and feature importance without black-box opacity.",
        "tree_depth": int(clf.get_depth()),
        "number_of_leaves": int(clf.get_n_leaves()),
        "tree_rules_text": tree_rules,
        "feature_importances": {
            feature_names[i]: round(float(clf.feature_importances_[i]), 4)
            for i in range(len(feature_names))
        },
    }


# -------------------------------------------------------------------------
# 4. INFRASTRUCTURE CONNECTIVITY GRAPH
# -------------------------------------------------------------------------
def demonstrate_infrastructure_graph() -> Dict[str, Any]:
    """
    Demonstrates NetworkX Directed Graph representing urban infrastructure topology.
    Why appropriate:
    - Infrastructure assets are not isolated: water mains feed branch pipelines,
      electrical substations supply power poles, arterial roads connect to feeder corridors.
    - Graph modeling reveals cascading vulnerability: if node A fails, which downstream nodes lose supply?
    """
    G = nx.DiGraph()

    # Define urban infrastructure nodes with baseline failure probabilities
    nodes = {
        "SUBSTATION-01": {"type": "Substation", "risk": 0.35, "zone": "Central"},
        "FEEDER-A": {"type": "Power Feeder", "risk": 0.40, "zone": "North"},
        "FEEDER-B": {"type": "Power Feeder", "risk": 0.25, "zone": "South"},
        "PUMP-STATION-01": {"type": "Water Pumping Station", "risk": 0.50, "zone": "North"},
        "PIPELINE-MAIN": {"type": "Water Main", "risk": 0.65, "zone": "North"},
        "DIST-VALVE-01": {"type": "Distribution Valve", "risk": 0.20, "zone": "North"},
        "HOSPITAL-GRID": {"type": "Critical Hospital Service", "risk": 0.10, "zone": "North"},
    }

    for n, data in nodes.items():
        G.add_node(n, **data)

    # Directed dependency edges: failure in predecessor cascades risk downstream
    edges = [
        ("SUBSTATION-01", "FEEDER-A", 0.90),
        ("SUBSTATION-01", "FEEDER-B", 0.85),
        ("FEEDER-A", "PUMP-STATION-01", 0.95),  # Pump needs power
        ("PUMP-STATION-01", "PIPELINE-MAIN", 0.80),
        ("PIPELINE-MAIN", "DIST-VALVE-01", 0.85),
        ("FEEDER-A", "HOSPITAL-GRID", 0.99),
    ]
    for u, v, weight in edges:
        G.add_edge(u, v, cascade_weight=weight)

    # Cascading risk calculation: if SUBSTATION-01 fails, compute impacted downstream reachable nodes
    downstream_impact = list(nx.descendants(G, "SUBSTATION-01"))
    betweenness = nx.betweenness_centrality(G)
    top_critical_bottleneck = max(betweenness, key=betweenness.get)

    return {
        "structure": "Directed Connectivity Graph (networkx.DiGraph)",
        "why_appropriate": "Captures spatial & functional interdependencies across utility networks (power, water, transportation). Enables betweenness centrality bottleneck detection and cascading failure analysis.",
        "nodes_count": G.number_of_nodes(),
        "edges_count": G.number_of_edges(),
        "nodes": list(G.nodes()),
        "critical_bottleneck_node": top_critical_bottleneck,
        "betweenness_centrality": {k: round(v, 3) for k, v in betweenness.items()},
        "cascading_impact_from_substation": downstream_impact,
    }


# -------------------------------------------------------------------------
# 5. PRIORITY QUEUE (MAX-HEAP)
# -------------------------------------------------------------------------
def demonstrate_priority_queue() -> Dict[str, Any]:
    """
    Demonstrates Heap-based Priority Queue for emergency triage and maintenance dispatch.
    Why appropriate:
    - O(log N) insertion and O(1) peek / O(log N) extraction of highest-risk asset.
    - Far superior to re-sorting the entire asset catalog (O(N log N)) when real-time sensor updates arrive.
    """
    # Python heapq implements a min-heap by default; we store negative risk to implement max-heap
    assets_stream = [
        ("ASSET-101", 0.42, "Road"),
        ("ASSET-102", 0.89, "Bridge"),
        ("ASSET-103", 0.15, "Pole"),
        ("ASSET-104", 0.94, "Pipeline"),
        ("ASSET-105", 0.63, "Drainage"),
        ("ASSET-106", 0.77, "Bridge"),
    ]

    pq: List[Tuple[float, str, str]] = []
    for aid, risk, atype in assets_stream:
        # Push (-risk, aid, atype)
        heapq.heappush(pq, (-risk, aid, atype))

    # Extract top 3 emergency dispatch assets
    dispatched: List[Dict[str, Any]] = []
    for rank in range(1, 4):
        neg_risk, aid, atype = heapq.heappop(pq)
        dispatched.append({
            "dispatch_rank": rank,
            "asset_id": aid,
            "risk_score": round(-neg_risk, 3),
            "asset_type": atype,
        })

    return {
        "structure": "Binary Heap Priority Queue (heapq / max-heap)",
        "why_appropriate": "Provides O(log N) insertion of incoming sensor telemetry updates and O(log N) immediate extraction of highest-priority emergency repairs, avoiding full O(N log N) database scans.",
        "top_emergency_dispatches": dispatched,
        "remaining_queued_assets": len(pq),
    }


# -------------------------------------------------------------------------
# 6. HASH DICTIONARIES
# -------------------------------------------------------------------------
def demonstrate_hash_dictionaries() -> Dict[str, Any]:
    """
    Demonstrates Hash Map / Dictionary for O(1) asset ID lookup and cached predictions.
    Why appropriate:
    - Rapid retrieval of asset telemetry, inspection history, and real-time inference scores by unique asset UUID.
    """
    asset_registry: Dict[str, Dict[str, Any]] = {
        "ASSET-0001": {"type": "Bridge", "zone": "Central", "risk": 0.88, "status": "INSPECTED"},
        "ASSET-0002": {"type": "Pipeline", "zone": "North", "risk": 0.45, "status": "OPERATIONAL"},
        "ASSET-0003": {"type": "Road", "zone": "South", "risk": 0.72, "status": "FLAGGED"},
    }

    # O(1) lookup
    target_id = "ASSET-0001"
    retrieved = asset_registry.get(target_id)

    return {
        "structure": "Hash Table / Dictionary (dict)",
        "why_appropriate": "Provides average O(1) time complexity for key-value retrieval of asset attributes, cached model inference results, and real-time status indexing by asset identifier.",
        "sample_lookup_key": target_id,
        "retrieved_record": retrieved,
        "total_indexed_assets": len(asset_registry),
    }


def demonstrate_all_data_structures() -> Dict[str, Any]:
    """Runs demonstrations of all 6 data structures and returns consolidated summaries."""
    return {
        "numpy": demonstrate_numpy_structures(),
        "sparse_matrices": demonstrate_sparse_matrices(),
        "decision_trees": demonstrate_decision_trees(),
        "infrastructure_graph": demonstrate_infrastructure_graph(),
        "priority_queue": demonstrate_priority_queue(),
        "dictionaries": demonstrate_hash_dictionaries(),
    }

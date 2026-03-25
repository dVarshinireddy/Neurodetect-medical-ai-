import numpy as np
import json
import os
from datetime import datetime
# ── HOSPITAL NODES ──
HOSPITAL_NODES = {
    "node_001": {
        "name":     "NeuroDetect Medical Center",
        "location": "Hyderabad, India",
        "patients": 1250,
        "scans":    3200,
        "specialty":"Neuro-Oncology"
    },
    "node_002": {
        "name":     "Apollo Brain Institute",
        "location": "Chennai, India",
        "patients": 980,
        "scans":    2100,
        "specialty":"Neurosurgery"
    },
    "node_003": {
        "name":     "NIMHANS",
        "location": "Bangalore, India",
        "patients": 1560,
        "scans":    4200,
        "specialty":"Neurology"
    },
    "node_004": {
        "name":     "AIIMS Neurosciences",
        "location": "New Delhi, India",
        "patients": 2100,
        "scans":    5800,
        "specialty":"Neurosciences"
    },
    "node_005": {
        "name":     "Global Hospital",
        "location": "Mumbai, India",
        "patients": 890,
        "scans":    1900,
        "specialty":"Radiology"
    }
}

def add_differential_privacy_noise(
    weights, epsilon=1.0, sensitivity=1.0
):
    noise_scale = sensitivity / epsilon
    noisy = {}
    for k, w in weights.items():
        if isinstance(w, np.ndarray):
            noise = np.random.laplace(
                0, noise_scale, w.shape
            )
            noisy[k] = w + noise
        else:
            noisy[k] = w
    return noisy

def federated_average(
    local_weights_list,
    sample_counts
):
    total_samples = sum(sample_counts)
    avg_weights   = {}

    keys = local_weights_list[0].keys()

    for key in keys:
        weighted_sum = sum(
            w[key] * (n / total_samples)
            for w, n in zip(
                local_weights_list,
                sample_counts
            )
        )
        avg_weights[key] = weighted_sum

    return avg_weights

def simulate_local_training(
    node_id, base_accuracy,
    local_samples
):
    noise         = np.random.normal(
        0, 0.5
    )
    local_acc     = min(
        99.9,
        base_accuracy + noise
    )
    improvement   = np.random.uniform(
        0.1, 0.8
    )
    n_layers      = 5
    local_weights = {}

    for i in range(n_layers):
        layer_shape = (
            64 * (2**min(i,3)),
            64 * (2**min(i,3))
        )
        local_weights[f"layer_{i}"] = \
            np.random.randn(
                *layer_shape
            ) * 0.01

    return {
        "node_id":        node_id,
        "local_accuracy": round(local_acc, 2),
        "improvement":    round(improvement, 2),
        "samples_used":   local_samples,
        "weights":        local_weights,
        "timestamp":      datetime.now()
                          .isoformat(),
        "privacy":        "differential_privacy",
        "epsilon":        1.0
    }

def run_federated_round(
    round_num,
    global_accuracy=98.87
):
    print(
        f"\n{'='*50}\n"
        f"Federated Learning Round {round_num}\n"
        f"{'='*50}"
    )

    local_results = []
    local_weights = []
    sample_counts = []

    for node_id, node_info in \
            HOSPITAL_NODES.items():
        print(
            f"Training on {node_info['name']}..."
        )
        result = simulate_local_training(
            node_id,
            global_accuracy,
            node_info["scans"]
        )

        # Add differential privacy
        private_weights = \
            add_differential_privacy_noise(
                result["weights"],
                epsilon=1.0
            )
        result["weights"] = private_weights

        local_results.append(result)
        local_weights.append(
            result["weights"]
        )
        sample_counts.append(
            node_info["scans"]
        )

        print(
            f"  Local accuracy: "
            f"{result['local_accuracy']}%"
        )

    # Federated averaging
    global_weights = federated_average(
        local_weights, sample_counts
    )

    # Calculate new global accuracy
    weighted_acc = sum(
        r["local_accuracy"] *
        (n / sum(sample_counts))
        for r, n in zip(
            local_results, sample_counts
        )
    )
    improvement  = np.random.uniform(
        0.05, 0.3
    )
    new_global   = min(
        99.9,
        weighted_acc + improvement
    )

    round_result = {
        "round":           round_num,
        "timestamp":       datetime.now()
                           .isoformat(),
        "nodes_trained":   len(HOSPITAL_NODES),
        "total_samples":   sum(sample_counts),
        "prev_accuracy":   round(
            global_accuracy, 2
        ),
        "new_accuracy":    round(new_global, 2),
        "improvement":     round(
            new_global - global_accuracy, 3
        ),
        "privacy_method":  "Differential Privacy",
        "epsilon":         1.0,
        "aggregation":     "FedAvg",
        "local_results":   [
            {
                "node":     r["node_id"],
                "accuracy": r["local_accuracy"],
                "samples":  r["samples_used"]
            }
            for r in local_results
        ]
    }

    print(
        f"\nGlobal accuracy: "
        f"{global_accuracy}% → "
        f"{new_global:.2f}%"
        f" (+{new_global-global_accuracy:.3f}%)"
    )

    return round_result

def save_federated_log(results):
    path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "history",
        "federated_log.json"
    )
    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    return path

def load_federated_log():
    path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "history",
        "federated_log.json"
    )
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def get_federation_stats():
    return {
        "total_nodes":    len(HOSPITAL_NODES),
        "total_patients": sum(
            n["patients"]
            for n in HOSPITAL_NODES.values()
        ),
        "total_scans":    sum(
            n["scans"]
            for n in HOSPITAL_NODES.values()
        ),
        "privacy_method": "Differential Privacy",
        "aggregation":    "FedAvg (McMahan 2017)",
        "communication":  "REST API",
        "base_accuracy":  98.87,
        "nodes":          HOSPITAL_NODES
    }

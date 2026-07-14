import numpy as np
from schemas import Flow

def extract_features(flow: FLowData) -> np.ndarray:
    return np.array([
        flow.src_port,
        flow.dst_port,
        flow.packet_size,
        flow.packet_count,
        flow.byte_count,
        1 if flow.protocol == "TCP" else 0,
        1 if flow.protocol == "UDP" else 0,
        1 if flow.protocol == "ICMP" else 0,
        len(flow.flags) if flow.flags else 0,
        flow.byte_count / max(flow.packet_count, 1), #bytes per packet averaging
        flow.packet_count / max(flow.duration, 0.001), # packet rate
    ])
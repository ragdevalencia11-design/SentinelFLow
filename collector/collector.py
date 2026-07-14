from scapy.all import sniff, IP
from utils import parse_packet, aggregate_flows
from shared.schemas import FlowData
import requests
from collections import defaultdict
from threading import Lock
import time

# Buffer: src_ip:dst_ip:proto:dport -> list of packet dicts
flow_buffer = defaultdict(list)
buffer_lock = Lock()

API_URL = "http://api:8000/predict"

def process_packet(packet):
    if IP not in packet:
        return
    
    parsed = parse_packet(packet)
    
    # Group key: src_ip + dst_ip + protocol + dst_port
    key = f"{parsed['src_ip']}:{parsed['dst_ip']}:{parsed['protocol']}:{parsed['dst_port']}"
    
    with buffer_lock:
        flow_buffer[key].append(parsed)
        
        # Flush to API when we have 10 packets or 5 seconds elapsed
        if len(flow_buffer[key]) >= 10:
            flush_flow(key)

def flush_flow(key):
    with buffer_lock:
        packets = flow_buffer[key]
        if not packets:
            return
        
        flow_data = aggregate_flows(packets)
        flow_buffer[key] = []
    
    try:
        response = requests.post(API_URL, json=flow_data.model_dump(), timeout=2)
        print(f"Sent flow {key}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send {key}: {e}")

def timeout_flush():
    """Flush stale flows every 5 seconds."""
    while True:
        time.sleep(5)
        keys = list(flow_buffer.keys())
        for key in keys:
            with buffer_lock:
                if flow_buffer[key] and (time.time() - flow_buffer[key][-1]['timestamp'] > 5):
                    flush_flow(key)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=timeout_flush, daemon=True).start()
    sniff(iface="eth0", prn=process_packet, store=0)

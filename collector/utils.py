from scapy.all import IP, TCP, UDP, ICMP
from shared.schemas import FlowData
from datetime import datetime
import time
import time

def parse_packet(packet) -> dict:
    """Extract basic info from a scapy packet."""
    flow = {
        "src_ip": packet[IP].src if IP in packet else None,
        "dst_ip": packet[IP].dst if IP in packet else None,
        "protocol": "TCP" if TCP in packet else "UDP" if UDP in packet else "ICMP" if ICMP in packet else "OTHER",
        "src_port": packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else 0),
        "dst_port": packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else 0),
        "packet_size": len(packet),
        "timestamp": time.time(),
    }
    return flow

def aggregate_flows(packets: list) -> FlowData:
    """Turn a list of packets into one FlowData record."""
    if not packets:
        return None
    
    first = packets[0]
    duration = (packets[-1].time - first.time) if len(packets) > 1 else 0.001
    
    return FlowData(
        src_ip=first["src_ip"],
        dst_ip=first["dst_ip"],
        src_port=first["src_port"],
        dst_port=first["dst_port"],
        protocol=first["protocol"],
        packet_size=sum(p["packet_size"] for p in packets) / len(packets),
        duration=duration,
        packet_count=len(packets),
        byte_count=sum(p["packet_size"] for p in packets),
        flags=None
    )

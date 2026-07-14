Here
it is:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def anomaly_score_chart(scores: list, timestamps: list) -> go.Figure:
    """Line chart of anomaly scores over time."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=scores,
        mode='lines+markers',
        name='Anomaly Score',
        line=dict(color='red' if any(s > 0.6 for s in scores) else 'green')
    ))
    fig.update_layout(
        title="Anomaly Score Timeline",
        xaxis_title="Time",
        yaxis_title="Score",
        template="plotly_dark"
    )
    return fig


def alert_severity_pie(alerts: list) -> go.Figure:
    """Pie chart of alert severity distribution."""
    severities = [a.severity for a in alerts]
    counts = {s: severities.count(s) for s in set(severities)}

    fig = go.Figure(data=[go.Pie(
        labels=list(counts.keys()),
        values=list(counts.values()),
        hole=.3
    )])
    fig.update_layout(title="Alert Severity Distribution", template="plotly_dark")
    return fig


def traffic_volume_chart(flows: list) -> go.Figure:
    """Bar chart of packet counts per flow."""
    fig = go.Figure(data=[
        go.Bar(
            x=[f"{f.src_ip}:{f.src_port}" for f in flows],
            y=[f.packet_count for f in flows],
            marker_color='cyan'
        )
    ])
    fig.update_layout(
        title="Traffic Volume by Source",
        xaxis_title="Source",
        yaxis_title="Packet Count",
        template="plotly_dark"
    )
    return fig


```
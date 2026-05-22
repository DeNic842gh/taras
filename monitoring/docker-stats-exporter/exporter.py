"""[docker] Container metrics via Docker API (works on Docker Desktop for Windows)."""

from __future__ import annotations

import time

import docker
from prometheus_client import Gauge, start_http_server

CONTAINER_CPU = Gauge(
    "docker_container_cpu_usage_percent",
    "[docker] CPU usage percent per container",
    ["container_name"],
)
CONTAINER_MEM = Gauge(
    "docker_container_memory_usage_bytes",
    "[docker] Memory working set bytes per container",
    ["container_name"],
)
CONTAINER_NET_RX = Gauge(
    "docker_container_network_receive_bytes_total",
    "[docker] Network bytes received",
    ["container_name"],
)
CONTAINER_NET_TX = Gauge(
    "docker_container_network_transmit_bytes_total",
    "[docker] Network bytes transmitted",
    ["container_name"],
)


def collect() -> None:
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        name = (container.name or "unknown").lstrip("/")
        try:
            stats = container.stats(stream=False)
        except docker.errors.APIError:
            continue

        cpu_delta = (
            stats["cpu_stats"]["cpu_usage"]["total_usage"]
            - stats["precpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_delta = (
            stats["cpu_stats"].get("system_cpu_usage", 0)
            - stats["precpu_stats"].get("system_cpu_usage", 0)
        )
        online_cpus = stats["cpu_stats"].get("online_cpus") or len(
            stats["cpu_stats"]["cpu_usage"].get("percpu_usage", []) or [1]
        )
        cpu_pct = 0.0
        if system_delta > 0 and online_cpus:
            cpu_pct = (cpu_delta / system_delta) * online_cpus * 100.0

        mem = stats.get("memory_stats", {}).get("usage", 0) or 0
        nets = stats.get("networks") or {}
        rx = sum(n.get("rx_bytes", 0) for n in nets.values())
        tx = sum(n.get("tx_bytes", 0) for n in nets.values())

        CONTAINER_CPU.labels(container_name=name).set(cpu_pct)
        CONTAINER_MEM.labels(container_name=name).set(float(mem))
        CONTAINER_NET_RX.labels(container_name=name).set(float(rx))
        CONTAINER_NET_TX.labels(container_name=name).set(float(tx))


def main() -> None:
    start_http_server(9417)
    while True:
        collect()
        time.sleep(15)


if __name__ == "__main__":
    main()

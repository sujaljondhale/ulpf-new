import time
import psutil
import gc
from typing import List
from app.pipeline import UlpfPipeline

# Sample diverse log messages for benchmarking
SAMPLE_LOG_POOL = [
    "CEF:0|CheckPoint|VPN-1 & FireWall-1|R80.10|1000|Accept Connection|Low|src=10.10.1.5 dst=8.8.8.8 spt=51522 dpt=443 proto=tcp act=allow shost=fw-edge-01",
    "src=192.168.1.100 dst=1.1.1.1 spt=54321 dpt=53 action=deny proto=udp rule=\"Block-DNS-External\" vendor=\"Fortinet\" product=\"FortiGate\"",
    "<134>Jan 10 14:32:01 edge-router-01 firewall[1234]: src=172.16.0.50 dst=10.0.0.1 spt=80 dpt=12345 action=drop proto=tcp",
    "LEEF:2.0|Imperva|SecureSphere|13.5|HTTP_Violation|^|src=10.2.3.4\tdst=192.168.100.5\tspt=49152\tdpt=80\tproto=tcp\tusr=admin\tact=block",
    '{"timestamp": "2026-09-02T12:00:00Z", "source_ip": "10.0.0.55", "source_port": 60000, "dest_ip": "8.8.4.4", "dest_port": 53, "protocol": "udp", "action": "allow", "vendor": "AWS WAF"}',
]


def run_benchmark_target(pipeline: UlpfPipeline, count: int, batch_size: int = 10000):
    print(f"\n" + "=" * 60, flush=True)
    print(f"Running ULPF Benchmark for {count:,} Events...", flush=True)
    print("=" * 60, flush=True)

    process = psutil.Process()
    gc.collect()
    mem_before = process.memory_info().rss / (1024 * 1024)

    start_time = time.perf_counter()
    processed_count = 0
    pool_len = len(SAMPLE_LOG_POOL)

    # Process in batches to ensure low memory footprint (16GB RAM constraint)
    for i in range(0, count, batch_size):
        current_batch_size = min(batch_size, count - i)
        for j in range(current_batch_size):
            log_idx = (i + j) % pool_len
            raw_msg = SAMPLE_LOG_POOL[log_idx]
            _ = pipeline.process(raw_msg)
        processed_count += current_batch_size

    total_time = time.perf_counter() - start_time
    mem_after = process.memory_info().rss / (1024 * 1024)
    cpu_percent = psutil.cpu_percent(interval=0.1)

    events_per_sec = count / total_time if total_time > 0 else 0
    avg_latency_us = (total_time / count) * 1_000_000 if count > 0 else 0
    avg_latency_ms = (total_time / count) * 1_000 if count > 0 else 0

    print(f"Processed Events:        {processed_count:,}", flush=True)
    print(f"Total Processing Time:   {total_time:.4f} seconds", flush=True)
    print(f"Throughput:              {events_per_sec:,.2f} events/sec", flush=True)
    print(f"Average Latency:         {avg_latency_us:.2f} \u00b5s ({avg_latency_ms:.4f} ms)", flush=True)
    print(f"Memory Usage (RSS):      {mem_after:.2f} MB (Delta: {mem_after - mem_before:+.2f} MB)", flush=True)
    print(f"CPU Utilization:         {cpu_percent:.1f}%", flush=True)

    return {
        "count": count,
        "total_time_sec": total_time,
        "events_per_sec": events_per_sec,
        "avg_latency_us": avg_latency_us,
        "memory_mb": mem_after,
        "cpu_percent": cpu_percent,
    }


def main():
    print("ULPF (Universal Log Pre-processing Framework) Phase 1 Benchmark", flush=True)
    print("System hardware targets: 16 GB RAM, Offline Deterministic Core", flush=True)

    pipeline = UlpfPipeline()

    # Warmup
    print("\nWarming up JIT/cache with 1,000 events...", flush=True)
    for i in range(1000):
        pipeline.process(SAMPLE_LOG_POOL[i % len(SAMPLE_LOG_POOL)])

    targets = [10_000, 100_000, 1_000_000]
    results = []

    for t in targets:
        res = run_benchmark_target(pipeline, count=t)
        results.append(res)

    print("\n" + "=" * 60, flush=True)
    print("FINAL BENCHMARK SUMMARY TABLE", flush=True)
    print("=" * 60, flush=True)
    print(f"{'Events':<12} | {'Time (s)':<10} | {'Events/sec':<14} | {'Avg Latency (µs)':<18} | {'RAM (MB)':<10}", flush=True)
    print("-" * 75, flush=True)
    for r in results:
        print(f"{r['count']:<12,} | {r['total_time_sec']:<10.3f} | {r['events_per_sec']:<14,.2f} | {r['avg_latency_us']:<18.2f} | {r['memory_mb']:<10.2f}", flush=True)
    print("=" * 75, flush=True)



if __name__ == "__main__":
    main()

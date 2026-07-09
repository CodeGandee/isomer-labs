# Hypothesis Model Contract

Before an idea becomes a model direction, state whether it aims to predict runtime, throughput, counter trends, saturated component, blocking execution path, or a narrower subset.

Require a hardware component graph for the relevant internals: schedulers, issue slots, tensor or vector pipes, special-function units, shared memory, caches, memory fabric, HBM, synchronization paths, launch overhead, or other named components. For every coefficient, efficiency, latency, bandwidth, probability, threshold, or factor, state its physical meaning, units or dimensionless status, source or calibration role, allowed range, and affected component or path.

Map workload inputs through ordered stages and component visits. State whether stages sum, overlap, serialize, queue, recur, or form a critical path. For data movement claims, name what moves, how it is sliced or batched, which components each slice traverses, and which hops can overlap or serialize.

Name the source family for each hard fact. Simulator structure can suggest the shape of the idea; target-hardware parameters need vendor sources, hardware queries, measurements, counters, or explicit assumptions.

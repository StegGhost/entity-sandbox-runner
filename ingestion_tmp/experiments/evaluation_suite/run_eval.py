from install.eval_orchestrator import run_cycle

workers = {"w1":{"score":1.0},"w2":{"score":0.9}}
queue = ["shard1","shard2"]

for _ in range(2):
    print(run_cycle(workers, queue))

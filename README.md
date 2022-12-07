# HPCC simulation
[Project page of HPCC](https://hpcc-group.github.io/) includes latest news of HPCC and extensive evaluation results using this simulator.

This is the simulator for [HPCC: High Precision Congestion Control (SIGCOMM' 2019)](https://rmiao.github.io/publications/hpcc-li.pdf). It also includes the implementation of DCQCN, TIMELY, DCTCP, PFC, ECN and Broadcom shared buffer switch.

We have update this simulator to support HPCC-PINT, which reduces the INT header overhead to 1 to 2 byte. This improves the long flow completion time. See [PINT: Probabilistic In-band Network Telemetry (SIGCOMM' 2020)](https://liyuliang001.github.io/publications/pint.pdf).

## How to run

### Prepare environment 

```
sudo ./prepare.sh
```

### Change the simulation config

* simulation/mix/config.txt         the main simulation configuration options
* simulation/mix/topology.txt       the topology in the simulation
* simulation/mix/flow.txt           the flow settings
* run.sh                            change `NODE_IDS` to select the nodes you want to plot

### Run simulation

```
./run.sh
```

### Get results

The results are put in directory `analysis/data/<time_str>`, where `<time_str>` is the time when the simulation starts. After simulation, there should be `node_<id>_bw.png` in the directory.

### Using Docker

```
docker build . -t ns3env
docker run --rm -v <host_path_to_project>:/workspace -v <host_path_to_project>/analysis/data:/workspace/analysis/data ns3env run.sh
```

## NS-3 simulation
The ns-3 simulation is under `simulation/`. Refer to the README.md under it for more details.

## Traffic generator
The traffic generator is under `traffic_gen/`. Refer to the README.md under it for more details.

## Analysis
We provide a few analysis scripts under `analysis/` to view the packet-level events, and analyzing the fct in the same way as [HPCC](https://liyuliang001.github.io/publications/hpcc.pdf) Figure 11.
Refer to the README.md under it for more details.

## Questions
For technical questions, please create an issue in this repo, so other people can benefit from your questions. 
You may also check the issue list first to see if people have already asked the questions you have :)

For other questions, please contact Rui Miao (miao.rui@alibaba-inc.com).

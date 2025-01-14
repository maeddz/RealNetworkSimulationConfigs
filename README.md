# RealNetworkSimulationConfigs

This repository contains configurations and scripts designed for real network simulations using OMNeT++, INET, and IXIA. The files are structured to facilitate network modeling, traffic generation, and analysis in research and experimentation settings.  

## Features  
- **OMNeT++/INET Configurations:**  
  Includes `.ned` and `.ini` files for defining network topologies and simulation parameters.  

- **Custom Queue Model:**  
  Implements a queue model to simulate FIFO policies with fairness across flows.  

- **Traffic and Routing Configurations:**  
  Contains detailed traffic patterns (`Traffic.json`) and routing configurations (`graph.txt` and `traffic.txt`) for seamless integration with real-world network setups.  

- **Execution Scripts:**  
  Automates the generation of simulation inputs and analysis of results for reproducibility and ease of use.  

## Prerequisites
- **OMNeT++** (version 6.0.2 or higher):  
  - [Installation guide](https://omnetpp.org/documentation/)  
- **INET Framework** (version 4.3)
- **IXIA Traffic Generator** ((https://support.ixiacom.com/version/ixnetwork-930))
- **BNNetSimulator** (https://github.com/BNN-UPC/BNNetSimulator)
- **RouteNetFermi** (https://github.com/BNN-UPC/RouteNet-Fermi)

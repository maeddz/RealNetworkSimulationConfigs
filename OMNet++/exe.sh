#!/bin/bash

# python randomNumbers.py

repeats=1
i=0
for (( j=0; j<repeats; j++ ))
do
     python script.py $j

     ./TopoSimulation.exe -u Cmdenv -c General -r $i -m -n "../simulations;.;../../../inet4.3/src;../../../inet4.3/examples;../../../inet4.3/tutorials;../../../inet4.3/showcases" -x "inet.emulation;inet.showcases.visualizer.osg;inet.showcases.emulation;inet.clock.common;inet.clock.model;inet.visualizer.osg;inet.examples.voipstream;inet.clock.oscillator;inet.examples.emulation;inet.transportlayer.tcp_lwip;inet.applications.voipstream;inet.clock.base;inet.examples.clock;inet.transportlayer.tcp_nsc" --image-path="../../../inet4.3/images" -l "../../../inet4.3/src/INET" omnetpp.ini
     opp_scavetool x results/*.sca -o result_sca.json
     python resultAnalysis.py $j
done


package toposimulation;

import inet.common.misc.ThruputMeteringChannel;
import inet.common.scenario.ScenarioManager;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import inet.node.ospfv2.OspfRouter;
import inet.visualizer.common.IntegratedVisualizer;
import inet.node.ethernet.Eth1G;
import inet.node.ethernet.Eth100M;
import ned.DatarateChannel;
import inet.queueing.queue.DropTailQueue;
import inet.queueing.contract.IPacketQueue;
import inet.queueing.scheduler.WrrScheduler;


network Network
{
    parameters:
        @display("p=10,10;b=712,152");
        @statistic[endToEndDelay](record=vector);
	types:
	    channel C extends ThruputMeteringChannel {
			datarate = 100Mbps;	    
		}
    submodules:
        H11: StandardHost {
            parameters:
                @display("p=250,200");
            gates:
                ethg[1];
        }
        R11: OspfRouter {
            parameters:
                @display("p=400,200");
            gates:
                ethg[2];
        }
        H13: StandardHost {
            parameters:
                @display("p=550,50");
            gates:
                ethg[1];
        }
        H14: StandardHost {
            parameters:
                @display("p=821,23");
            gates:
                ethg[1];
        }
        R13: OspfRouter {
            parameters:
                @display("p=550,100");
            gates:
                ethg[4];
        }
        R14: OspfRouter {
            parameters:
                @display("p=723,73");
            gates:
                ethg[2];
        }
        R12: OspfRouter {
            parameters:
                @display("p=700,200");
            gates:
                ethg[2];
        }
      
        H12: StandardHost {
            parameters:
                @display("p=850,200");
            gates:
                ethg[1];
        }
        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=100,100;is=s");
                config = xml("<config>"
                        + "<interface among='H11 R11' address='192.168.1.x' netmask='255.255.255.x' />"
                        + "<interface among='H12 R12' address='192.168.2.x' netmask='255.255.255.x' />"
                        + "<interface among='H13 R13' address='192.168.3.x' netmask='255.255.255.x' />"
                        + "<interface among='H14 R14' address='192.168.4.x' netmask='255.255.255.x' />"
                        + "<interface among='R*' address='10.0.0.x' netmask='255.255.255.x' />"
                        + "<multicast-group hosts='R*' address='224.0.0.5 224.0.0.6' />"
                        + "<route hosts='H11' destination='*' gateway='R11'/>"
                        + "<route hosts='H12' destination='*' gateway='R12'/>"
                        + "<route hosts='H13' destination='*' gateway='R13'/>"
                        + "<route hosts='H14' destination='*' gateway='R14'/>"
                        + "<route hosts='R*' destination='224.0.0.0' netmask='240.0.0.0' interface='eth0'/>"
                        + "<route hosts='R*' destination='224.0.0.0' netmask='240.0.0.0' interface='eth1'/>"
                        + "<route hosts=' R13' destination='224.0.0.0' netmask='240.0.0.0' interface='eth2'/>"
                        + "<route hosts='R13' destination='224.0.0.0' netmask='240.0.0.0' interface='eth3'/>"
                        + "</config>");
        }
        scenarioManager: ScenarioManager {
            @display("p=100,200;is=s");
        }
    connections:
        H11.ethg[0] <--> Eth1G <--> R11.ethg[0];
        H13.ethg[0] <--> Eth1G <--> R13.ethg[0];
        H14.ethg[0] <--> Eth1G <--> R14.ethg[0];
        R11.ethg[1] <--> C <--> R13.ethg[1];
        R13.ethg[2] <--> C <--> R12.ethg[1];
        R12.ethg[0] <--> Eth1G <--> H12.ethg[0];
        R13.ethg[3] <--> C <--> R14.ethg[1];

}

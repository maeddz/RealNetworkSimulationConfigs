from ixnetwork_restpy import SessionAssistant, StatViewAssistant
import json
import time
import os



with open('traffic.json') as file:
    data = json.load(file)

for i in range(len(data['scenarios'])):
    flows = data['scenarios'][i]
    while True:
        try:
            session_assistant = SessionAssistant(IpAddress="", 
                                                LogLevel=SessionAssistant.LOGLEVEL_INFO, 
                                                ClearConfig=True, SessionId=1)
            ixnetwork = session_assistant.Ixnetwork

            ixChassisIp = ''
            port_map_dict = {
            }

            port_map = session_assistant.PortMapAssistant()
            vports = {}


            for flow in flows['flows']:
                src = str(flow['src'])
                dest = str(flow['dest'])

                src_port_id = f"Port_{src}"
                dest_port_id = f"Port_{dest}"

                if src_port_id not in vports:
                    vports[src_port_id] = ixnetwork.Vport.add(Name=src_port_id)
                    port_map.Map(IpAddress=port_map_dict[src][0], CardId=port_map_dict[src][1], PortId=port_map_dict[src][2], Name=src_port_id)

                if dest_port_id not in vports:
                    vports[dest_port_id] = ixnetwork.Vport.add(Name=dest_port_id)
                    port_map.Map(IpAddress=port_map_dict[dest][0], CardId=port_map_dict[dest][1], PortId=port_map_dict[dest][2], Name=dest_port_id)

            port_map.Connect()

            topology_dict = {}
            for key, vport in vports.items():
                
                topology = ixnetwork.Topology.add(Name=key, Vports=vport)
                device_group = topology.DeviceGroup.add(Name=f"DG_{key}", Multiplier=1)
                ethernet = device_group.Ethernet.add(Name=f"Ethernet_{key}")
                ipv4 = ethernet.Ipv4.add(Name=f"IPv4_{key}")
                ipv4.Address.Single(f"1.0.{key[-1]}.2")
                ipv4.GatewayIp.Single(f"1.0.{key[-1]}.1")
                topology_dict[key] = topology
                view = ixnetwork.Statistics.View.find()
                for statistic in view.Statistic.find():
                    statistic.Enabled = True

            ixnetwork.StartAllProtocols(Arg1='sync')


            for flow in flows['flows']:
                msgLen = flow['packetSize'] 
                sendInterval = flow['sendInterval']
                src = str(flow['src'])
                dest = str(flow['dest'])
                src_port_id = f"Port_{src}"
                dest_port_id = f"Port_{dest}"
                src_topo_id = f"Topo_TX_{src}"
                dest_topo_id = f"Topo_RX_{dest}"

                traffic_item = ixnetwork.Traffic.TrafficItem.add(Name=f"Flow_{src}_to_{dest}", BiDirectional=False, TrafficType='ipv4')
                traffic_item.EndpointSet.add(Sources=topology_dict[src_port_id], 
                                            Destinations=topology_dict[dest_port_id])

                config_element = traffic_item.ConfigElement.find()
                config_element.FrameRate.update(Type='bitsPerSecond', Rate=sendInterval*8)
                config_element.FrameSize.FixedSize = msgLen
                config_element.FrameRateDistribution.PortDistribution = 'splitRateEvenly'
                traffic_item.Tracking.find()[0].TrackBy = ['trackingenabled0']
                traffic_item.Generate()
                
            ixnetwork.Traffic.Apply()
            ixnetwork.Traffic.Start()

            time.sleep(30)  

            simulationResult = { "msgLen":msgLen, "sendInterval":sendInterval, "flows":[]}


            traffic_statistics = session_assistant.StatViewAssistant("Traffic Item Statistics")
            for row in traffic_statistics.Rows:
                print(row)
                portInfo = row['Traffic Item'].split("_")
                flow = {
                        "total_packets_transmitted": row['Tx Frames'],
                        "total_packets_lost": row['Frames Delta'],
                        "send_interval": row['Tx Frame Rate'],
                        "msg_length": float(row['Tx Rate (Bps)']) / float(row['Tx Frame Rate']),
                        "avg_ln_delay": row['Store-Forward Avg Latency (ns)'],
                        "timeStamp": row['Last TimeStamp'],
                        "src": portInfo[1],
                        "dst": portInfo[3],
                        "loss": row['Loss %']
                    }
                simulationResult['flows'].append(flow)

            # ixnetwork.StopAllProtocols()
            print("Traffic generation complete.")

            with open('result3.json', 'w') as file:
                json.dump(simulationResult, file, indent=4)
            
            time.sleep(30)
            break
        except Exception as e:
            print(e)

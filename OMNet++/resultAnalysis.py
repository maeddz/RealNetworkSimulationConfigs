import pandas as pd
import json
import sys

vector_file = 'result_vec.csv'
sca_file = 'result_sca.json'

with open(sca_file, 'r') as file:
    sca_data = json.load(file)


data = []
with open('traffic.json', 'r') as f:
    traffic_data = json.load(f)
    traffic_data = traffic_data['scenarios'][int(sys.argv[1])]
app_index = 0
hosts = {"H11":{"numApp":0, "destHosts":[], "srcs":0, "dsts":0}, "H12":{"numApp":0, "destHosts":[],"srcs":0, "dsts":0}
         , "H13":{"numApp":0, "destHosts":[],"srcs":0, "dsts":0}, "H14":{"numApp":0, "destHosts":[],"srcs":0, "dsts":0}}
for flow in traffic_data["flows"]:
    src_host = f"H1{flow['src']}"
    dest_host = f"H1{flow['dest']}"
    hosts[src_host]['numApp'] += 1
    hosts[dest_host]['numApp'] += 1
    hosts[src_host]['destHosts'].append(dest_host)
    hosts[dest_host]['dsts'] += 1
    hosts[src_host]['srcs'] += 1

for run, result in sca_data.items():
    run_data = []
    for config in result['config']:
        for key, value in config.items():
            if "sendInterval" in key:
                sendInterval = value
            if "messageLength" in key:
                messageLength = value
            if "datarate" in key:
                datarate = value
            if "delay" in key:
                delay = value

    for scalar in result["scalars"]:
        if scalar['module'].startswith(("Network.H12.app[", "Network.H13.app[", "Network.H14.app[", "Network.H11.app[")) and scalar['name'] == 'packets sent':
            run_data.append({"run":run, "module": scalar['module'], 'attr': scalar['name'], 'value': scalar['value']})
        
        if scalar['module'].startswith(("Network.H12.udp", "Network.H13.udp", "Network.H14.udp", "Network.H11.udp")) and scalar['name'].startswith('packetReceived:count') and scalar["value"] != 0:
            run_data.append({"run":run, "module": scalar['module'], 'attr': scalar['name'], 'value': scalar['value']})
            
            
        # if scalar['module'].startswith(("Network.H12.app[0]", "Network.H13.app[", "Network.H14.app[")) and scalar['name'].startswith('packetReceived'):
        #     run_data.append({"run":run, "module": scalar['module'], 'attr': scalar['name'], 'value': scalar['value']})
    
    for hist in result['histograms']:
        if hist['module'].startswith(("Network.H12.app[", "Network.H13.app[", "Network.H14.app[", "Network.H11.app[")) and hist['name'].startswith('endToEndDelay'):
            run_data.append({"run":run, "module": hist['module'], 'attr': hist['name'], 'count': hist['count'], 
                  "mean":hist['mean'], "stddev":hist["stddev"], 'min':hist['min'], 'max':hist['max'],
                  'sum':hist['sum'], 'sqrsum':hist['sqrsum'], 'underflows':hist['underflows'], 'overflows':hist['overflows']})
    
            
    data.append({"run": run, "messageLength": messageLength, "sendInterval":sendInterval, "result": run_data})
    

old_data = []

import os


if os.path.exists('newresult.json'):
    with open('newresult.json', 'r') as file:
        try:
            old_data = json.load(file)
        except json.JSONDecodeError:
            old_data = []
else:
    old_data = []
    
paths = {"H11":{"dests":[]}, "H12":{"dests":[]}
         , "H13":{"dests":[]}, "H14":{"dests":[]}}
for flow in traffic_data["flows"]:
    src_host = f"H1{flow['src']}"
    dest_host = f"H1{flow['dest']}"
    paths[dest_host]['dests'].append((src_host, flow['sendInterval'] / flow['packetSize'] * 22))
print(paths)
         
for i in data:
    for j in i['result']:
        if 'Delay' in j['attr']:   
            dst = j['module'].split('.')[1]
            j['dst'] = dst
            j['src'], packet_size = paths[dst]['dests'].pop(0)
            j['packet_sent'] = packet_size
old_data.append(data)

with open('newresult.json', 'w') as file:
    json.dump(old_data, file, indent=4)

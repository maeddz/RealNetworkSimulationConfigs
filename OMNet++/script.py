import json
import sys 

# Read the JSON file
with open('traffic.json', 'r') as f:
    traffic_data = json.load(f)

traffic_data = traffic_data["scenarios"][int(sys.argv[1])]


# Prepare the INI file content
ini_content = """
[General]
network=Network
**.ospf.ospfConfig=xmldoc("config.xml")
output-scalar-precision=10
output-vector-precision=10
repeat=4
seed-set=${repetition}
cmdenv-express-mode=true
rng-class=cMersenneTwister
sim-time-limit=210s
**.app[*].**.scalar-recording=true
*.usenew = true

"""

# Add host applications based on the traffic data
app_index = 0
hosts = {"H11":{"numApp":0, "destHosts":[], "flows": [], "dstAdded":0, "dsts":[]}, "H12":{"numApp":0, "destHosts":[], "flows": [],"dstAdded":0, "dsts":[]}
         , "H13":{"numApp":0, "destHosts":[], "flows": [],"dstAdded":0, "dsts":[]}, "H14":{"numApp":0, "destHosts":[], "flows": [],"dstAdded":0, "dsts":[]}}
for flow in traffic_data["flows"]:
    src_host = f"H1{flow['src']}"
    dest_host = f"H1{flow['dest']}"
    hosts[src_host]['numApp'] += 1
    hosts[dest_host]['numApp'] += 1
    hosts[src_host]['destHosts'].append([dest_host, flow['packetSize'], flow['sendInterval']])
    hosts[dest_host]['dsts'].append(flow['src'] - 1)
h = 0
for key, values in hosts.items():
    ini_content += f"""
**.{key}.numApps={values['numApp']} """
    i = 0
    for dst in values['destHosts']:
        ini_content += f"""
**.{key}.app[{i}].typename="UdpBasicApp" 
**.{key}.app[{i}].destAddresses="{dst[0]}"
**.{key}.app[{i}].destPort={5000 + h}
**.{key}.app[{i}].messageLength={dst[1] - 64}bytes
**.{key}.app[{i}].sendInterval={1 / (dst[2])}s
        """
        i += 1
    for j in range(len(values['dsts'])):
        ini_content += f"""
**.{key}.app[{i + j}].typename="UdpSink" 
**.{key}.app[{i + j}].localPort={5000 + values['dsts'][j]}
        """
    h += 1
        


ini_content += f"""
**.app[*].startTime=200s
**.H*.app[*].stopTime=205.0s


**.eth[*].mac.queue.typename = "DropTailQueue"
**.eth[*].mac.queue.packetCapacity = 1000



"""

# Write the INI content to a file
with open('omnetpp.ini', 'w') as f:
    f.write(ini_content)

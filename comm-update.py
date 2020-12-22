import json
import tempfile
from pathlib import Path
import urllib.request
import uuid

# helper to call the webservice and parse the response
def webApiGet(methodName, instanceName, clientRequestId):
    ws = "https://endpoints.office.com"
    requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
    request = urllib.request.Request(requestPath)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())

# path where client ID and latest version number will be stored
datapath = Path(tempfile.gettempdir() + '/worldwide_endpoints_clientid_latestversion.txt')

# fetch client ID and version if data exists; otherwise create new file
if datapath.exists():
    with open(datapath, 'r') as fin:
        clientRequestId = fin.readline().strip()
        latestVersion = fin.readline().strip()
else:
    clientRequestId = str(uuid.uuid4())
    latestVersion = '0000000000'
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + latestVersion)

# call version method to check the latest version, and pull new data if version number is different
version = webApiGet('version', 'Worldwide', clientRequestId)

# UNCOMMENT if you want to force an update (you can also delete the tmp file in /tmp)
#latestVersion = '0'

if version['latest'] > latestVersion:
    print('New version of Office 365 worldwide commercial service instance endpoints detected')
    # write the new version number to the data file
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + version['latest'])
    # invoke endpoints method to get the new data
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []

            for indx, entry in enumerate(urls):
            # Loop through all URLs and if you see an asterisk with no trailing period
            # Modify the entry to fit within the confines of an EDL entry
                if entry[0] == "*" and entry[1] != ".":
                    # Remove the asterisk
                    urls[indx] = entry[1:]
                    print(entry + " has been updated to " + urls[indx])

            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])

    flatIps = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            # IPv4 strings have dots while IPv6 strings have colons
            ip4s = [ip for ip in ips if '.' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])
#    print('IPs')
#    print('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    print('URLs')
    print('\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))
    MyURLList = '\n'.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls])))

    with open('/home/fedadmin/edlserver/commedl.txt', 'w') as f:
            f.write("%s\n" % MyURLList)

else:
    print('Office 365 worldwide commercial service instance endpoints are up-to-date')

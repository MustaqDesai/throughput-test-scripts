import iperf3
iperf_client = iperf3.Client()
iperf_client.server_hostname = "10.1.32.22"
iperf_client.json_output = False
result = iperf_client.run()
#print(result)
#del iperf_client
#iperf_client = None

#iperf_client = iperf3.Client()
#iperf_client.server_hostname = "10.1.32.22"
#iperf_client.reverse = True
#result = iperf_client.run()
#print(result)
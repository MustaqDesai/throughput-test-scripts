import iperf3
iperf_client = iperf3.Client()
iperf_client.server_hostname = "10.1.32.22"
result = iperf_client.run()
print(result)

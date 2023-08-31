import sys # To read command line arguments
from pathlib import Path # To create folders and files
import datetime # To use date and time
import iperf3 # To create and use iPerf3 client

#current_datetime = datetime.datetime.now().strftime("%04Y-%02m-%02d-%H-%M-%S")
#print(current_datetime)

# Modify ip address pool if needed, but should not have to modify it often. 
ip_pool = "10.1.32." # for use as prefix later, in a for-loop with iperf servers

test_duration = 10 # For quick tests
#duration = 600  # To give UniFi Network application more than 5 minutes to gather data for test client

intro_message = """Script needs at least 4 arguments:
Firmware version, friendly AP name, Wi-Fi band (2G or 5G), followed by IP address of client(s).
For client IP address, enter only the last octet.
Example: python3 testAP.py 1.23.456 UAP-AC-Pro 2G 23"""  
#print(intro_message)

cli_args = sys.argv # Store commnd line args
arg_count = len(cli_args)

if arg_count < 5: # Confirm requried input is entered
    print(intro_message)
else:
    # Name of this file is cli_args[0], use next 3 args
    firmware = cli_args[1]
    ap_name = cli_args[2]
    band = cli_args[3]
    iperf_servers = cli_args[4:arg_count] # Create list of iperf servers
    # Below line works same as above line, but I like how the above line looks
    # iperf_servers = cli_args[4:]
    
    # Store current date for use in log file name
    current_date = datetime.datetime.now().strftime("%04Y-%02m-%02d")
   
    # Create folders in parent direcotry to store log files
    log_path = "../" + firmware + "/" + ap_name
    Path(log_path).mkdir(parents=True, exist_ok=True)
     # Contruct log file name
    log_file_name = current_date + "-" + firmware + "-" + ap_name + "-" + band + ".log"
    # Contruct log folder and file location
    log_location = log_path + "/" + log_file_name
    #print(log_location)
    # Show the location and name of log file
    log_message = "Logging results in %s" % (log_location)
    print(log_message)
    # Write to log file
    with open(log_location,'a') as out_file:
        # Tests are executed/run from a linux machine (test runner), 
        # but are executed on iperf server running on test device(s). 
        # DN is when the test runner is receving traffic from test device
        # UP is when the test runner is sending traffic to test device
        directions=["DN","UP"]
        # Main loop that sets direction of iPerf3 tests
        for direction in directions:
            print(direction) # Show direction on screen
            out_file.write(direction + "\n")
            # Insert some lines for better visibility and readability of log
            # Need to figure out how to insert content into log file
            #echo "_________________________________________________________________" >> $logLocation
            #echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" >> $logLocation
        
            #echo $direction >> $logLocation # insert direction into log
            for iperf_server in iperf_servers:
                server_address = ip_pool + iperf_server # compose full ip address of device
                #print("")
                #print("Client: " + server_address)  # Show device ip on screen
                
                # Detailed time stamp for tests
                current_datetime = datetime.datetime.now().strftime("%04Y-%02m-%02d-%H-%M-%S")
                #print(current_datetime)
                server_address_and_time_stamp = "Client: " + server_address + ", TimeStamp: " + current_datetime
                print(server_address_and_time_stamp)
                out_file.write(server_address_and_time_stamp + "\n")                           
                
                # Set number of prallel streams
                for streams in range(1,3): 
                    
                    # Create and use iPerf3 client
                    iperf_client = iperf3.Client()
                    iperf_client.duration = test_duration
                    #iperf_client.verbose = True
                    
                    iperf_client.server_hostname = server_address 
                    iperf_client.num_streams = int(streams)
                    if direction == "UP":
                        iperf_client.reverse = True # Device sends data to test runner
                    
                    #print(streams)
                    #print(direction)
                    #print(iperf_client.reverse)
                    result = iperf_client.run()
                    #print(result)

                    # Most of the below code is copied from https://github.com/thiezn/iperf3-python/blob/master/examples/client.py
                    if result.error:
                        print(result.error)
                    else:
                        
                        #print('Test completed:')
                        #print('  started at         {0}'.format(result.time))
                        #print('  bytes transmitted  {0}'.format(result.sent_bytes))
                        #print('  retransmits        {0}'.format(result.retransmits))
                        #print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

                        #print('Average transmitted data in all sorts of networky formats:')
                        #print('  bits per second      (bps)   {0}'.format(result.sent_bps))
                        #print('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
                        #print('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
                        #print('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
                        #print('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))
                        result_message  = "Streams: %i, Throughput: %i Mbits/sec" % (int(streams), int(result.sent_Mbps))
                        print(result_message)
                        out_file.write(result_message + "\n")
                            
                    # Can not reuse iPerf3 client after a test is completed.
                    # Destroy after each test to avoid "unable to send cookie to server" error for next run
                    iperf_client = None
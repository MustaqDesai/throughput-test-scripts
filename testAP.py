import sys # To read command line arguments
from pathlib import Path # To create folders and files
import datetime # To use date and time
import iperf3 # To create and use iperf3 client

#right_now = datetime.datetime.now().strftime("%04Y-%02m-%02d-%H-%M-%S")
#print(right_now)

# Modify ip address pool if needed, but should not have to modify it often. 
ip_pool = "10.1.32." # for use as prefix later, in the for-loop with iperf servers

duration = 30 # For quick tests
#duration = 600  # To give controller more than 5 minutes to gather data for test client

intro_message = """Script needs at least 4 arguments:
Firmware version, friendly AP name, Wi-Fi band (2G or 5G), followed by IP address of client(s).
For client IP address, enter only the last octet.
Example: python3 testAP.py 1.23.456 UAP-AC-Pro 2G 23"""  
#print(intro_message)

cli_args = sys.argv # Store the commnd line args
arg_count = len(cli_args)

if arg_count < 5: # Confirm requried input is entered
    print(intro_message)
else:
    # Name of this file is cli_args[0], so we need next 3 args
    firmware = cli_args[1]
    ap_name = cli_args[2]
    band = cli_args[3]
    
    # Create folders to store logs
    Path("./firmware/ap_name").mkdir(parents=True, exist_ok=True)
    # Store today's date for use in log file name
    date_today = datetime.datetime.now().strftime("%04Y-%02m-%02d")
    # Contruct log file name
    log_file = date_today + "-" + firmware + "-" + ap_name + "-" + band + ".log"
    # Contruct log file location
    log_location = firmware + "/" + ap_name + "/" + log_file
    #print(log_location)
    # Show the location and name of log file
    log_message = "Logging results in %s" % (log_location)
    print(log_message)
    
    iperf_servers = cli_args[4:arg_count] # Create list of iperf servers
    # Below line works same as above line, but I like how the above line looks
    #clients = cli_args[4:]
    #print(clients)

    base_command = "" # Start with empty string, to build an iPerf3 command
    
    # Create iPerf3 client
    iperf_client = iperf3.Client()
    iperf_client.duration = duration
    iperf_client.verbose =  True
    #iperf_client.json_output = False
    #iperf_client = True


    # Need to rememer that tests are controlled/executed/run from server, but are executed for mobile clients
    # DN is when the sever is receving traffic from client
    # UP is when the server is sending traffic to client
    directions=["DN","UP"]
    # Main loop that sets direction of iPerf3 tests
    for direction in directions:
        print(direction) # Show direction on screen
        if direction == "DN":
            # The -R sets the reverse direction, so the mobile client generates and sends the data to server
            base_command = "iperf3 --forceflush -t" + str(duration) + " -i5 -V -R -c"
            iperf_client.reverse = True
            #print(base_command)
        else:
            base_command = "iperf3 --forceflush -t" + str(duration) + " -i5 -V -c"
            iperf_client.reverse = False
            #print(base_command)
    
        # Insert some lines for better visibility and readability of log
        # Need to figure out how to insert content into log file
        #echo "_________________________________________________________________" >> $logLocation
        #echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" >> $logLocation
    
        #echo $direction >> $logLocation # insert direction into log
        for iperf_server in iperf_servers:
            iperf_client.server_hostname = ip_pool + iperf_server
            #print(client)
            # Need detailed time stamp for tests
            right_now = datetime.datetime.now().strftime("%04Y-%02m-%02d-%H-%M-%S")
            print(right_now)
            #echo "$dtNow" >> $logLocation

            # Set number of prallel streams
            for streams in range(1,2): 
                print(streams)
                # The complete iPerf3 command 
                #complete_command = base_command + ip_pool + client + " -P" + str(streams)
                iperf_client.num_streams = int(streams)
                #print(complete_command)
                #echo "Executing $finalCommand" #show current command on screen
                #echo $finalCommand >> $logLocation 
                #$finalCommand >> $logLocation # insert current command into log
                result = iperf_client.run()
                print(result)


            
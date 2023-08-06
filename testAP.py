import sys # Needed to read command line arguments
import os # Needed create folders and files
import datetime # Needed for use date and time

#right_now = datetime.datetime.now().strftime("%04Y-%02m-%02d-%H-%M-%S")
#print(right_now)

# Modify ip address pool if needed, but should not have to modify it often. 
ipPool="10.1.21." # for use as prefix later, in a for-loop 

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
    
    # Create new folders if needed to store logs
    os.mkdir(firmware/ap_name) 
    # Store today's date for use in log file name
    date_today = datetime.datetime.now().strftime("%04Y-%02m-%02d")
    # Contruct log file name
    log_file = date_today + firmware + ap_name + band + ".log"
    # Contruct log file location
    log_location = firmware/ap_name/log_file
    # Show the location and name of log file
    print("Logging results in %s.") % (log_location)
    
    clients = cli_args[4:arg_count] # Create list of mobile clients
    # Below line works same as above line, but I like how the above line looks
    #clients = cli_args[4:]
    print(clients)

    #for client in clients:


import sys # Need it read command line arguments
    
print("Script needs at least 4 arguments:")
print("Firmware version, friendly AP name, band (2G or 5G), followed by ip address of client(s)")
print("CLI example: python3 testAP.py 1.23.456 UAP-AC-Pro 2G 23") 

# confirm all requried input is entered
cli_args = sys.argv #store all the commnd line args
arg_count = len(cli_args)
print(arg_count)
print(cli_args)

if arg_count < 5:
    print("Provide at least 4 arguments.")
else:
    # cli_args[0] is the name of file, so we need next 3
    firmware = cli_args[1]
    ap_name = cli_args[2]
    band = cli_args[3]
    print(firmware)
    print(ap_name)
    print(band)
    
    clients = cli_args[4:arg_count]
    print(clients)

    ipPool="10.1.21." # for use as prefix later, in a for-loop
    # string loop with element #4 (5th element). Prior elements are used above.

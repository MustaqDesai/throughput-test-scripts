import sys
def testAP():
    print("Script needs 3 arguments:")
    print("The firmware version, the friendly name of AP, and band (2G or 5G) being tested.")
    print("CLI example: python3 testAP.py 1.23.456 UAP-AC-Pro 2G") 
    
    # confirm all requried input is entered
    arg_count = len(sys.argv)
    print(arg_count)

    if arg_count != 4:
        print("Provide 3 arguments.")
    else:
        # sys.argv[0] is the name of file, so we need next 3
        firmware = sys.argv[1]
        ap_name = sys.argv[2]
        band = sys.argv[3]
        print(firmware)
        print(ap_name)
        print(band)

testAP()
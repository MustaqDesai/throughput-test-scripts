
#!/bin/bash

# Confirm all required input is entered
if [ "$#" -ne "3" ]; then
  echo "ERROR: script needs 3 arguments, the firmware version, the friendly name of AP, and band (2G or 5G) being tested."
  echo
  exit 1
else
  firmwareVersion=$1
  apName=$2
  band=$3
fi 

# List of mobile clients
#declare -a clients=("iPhone7Plus")
#declare -a clients=("GalaxyS6EdgePlus" "iPhone7Plus" "iPadGen5" "MBP2014")
declare -a clients=("3" "4" "5" "6" "7" "8" "9")
#declare -a clients=("2")
 
ipPool="192.168.1." # To use as prefix later, in a for-loop

sleepTime="3s"
duration=30 # For quick tests
#duration=600  # Longer test, to give controller more than 5 minutes to gather data for test client

text_format_BOLD="\e[1m"
text_color_RED="\e[31m"
text_color_GREEN="\e[32m"
text_RESET="\e[0m"



mkdir -p $firmwareVersion/$apName # Create new folders if needed
# Get today date for use in log file name
dtToday=$(date '+%Y'-'%m'-'%d');
# Construct log file name
logFile=$dtToday-$firmwareVersion-$apName-$band.log
# Construct log file location
logLocation=$firmwareVersion/$apName/$logFile
# Show the location and name of log file
echo "Logging results in $logLocation"

baseCommand="iperf3 --forceflush -t$duration -i5 -fm" # Start with empty string, to build an iPerf3 command

# Main loop that sets direction of iPerf3 tests
# Need to remember that tests are controlled/executed/run from server, but are executed for mobile clients
# RSV is when the mobile client is sending to sever
# SND is when the mobile client is receiving from server
for direction in RSV SND; do
  if [ $direction == RSV ]; then
    # The -R sets the reverse direction, so the mobile client generates and sends the data
    dir=" -R"
    getLines=4
  else
    dir=""
    getLines=3
  fi
  echo $direction #display direction on screen
  # Insert some lines for better visibility and readability of log
  echo "_________________________________________________________________" >> $logLocation
  echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" >> $logLocation
 
  echo $direction >> $logLocation # Insert direction into log
  for client in "${clients[@]}"; do
    # We need more detailed time info for tests
    dtNow=$(date '+%Y %m %d %H:%M:%S');
    echo "$dtNow"
    echo "$dtNow" >> $logLocation

    tput_max=0
    # Secondary loop that controls the number of parallel streams
    for streams in {1..31}; do
      # Final iperf3 command
      finalCommand="$baseCommand$dir -c$ipPool$client -P$streams"
      echo "Executing $finalCommand" # Show current command on screen
      echo $finalCommand >> $logLocation # Insert current command into log

      $finalCommand >> $logLocation # Insert current command results into log

      # Depending on the direction, grab either the sender or receiver line of the iperf3 summary
      # Important to know that the tests are executed from the server, so it is important to understand the receiver and sender roles
      tail_string=$(tail -$getLines $logLocation | head -1 | awk '{if($1~"[SUM]") {a=$6;b=$7} else {a=$7;b=$8}} END{print a,b}')
      read -a tput_string <<< ${tail_string%% }

      if [ ${#tput_string} -gt 0 ]; then
        echo "Throughput: ${tput_string[0]} ${tput_string[1]}"
        tput_value=${tput_string[0]}
        #echo $tput_value
        tput_value_rounded=$(printf "%.0f" $tput_value)
        # echo $tput_value_rounded

        if [ $tput_value_rounded -lt $tput_max ]; then
          sleep $sleepTime # pause before next execution to give iPerf3 service to be ready again
          break 
        elif [ $tput_value_rounded -gt $tput_max ]; then
          tput_max=$tput_value_rounded
          #echo "New max! "$tput_max

        fi
      else
        sleep $sleepTime # pause before next execution to give iPerf3 service to be ready again
        break
      fi
      sleep $sleepTime # pause before next execution to give iPerf3 service to be ready again
    done # Streams loop
    if [ $tput_max -gt 0 ]; then
        echo $(printf "${text_format_BOLD}Max Throughput: $tput_max${text_RESET}")
    fi
    
    echo # Show empty line 
  done # Clients loop
  sleep $sleepTime # pause before next execution to give iPerf3 service to be ready again
done # Direction loop

echo # Show empty line
echo "See $logLocation for details." # Show location of log

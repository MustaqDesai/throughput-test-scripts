#!/bin/bash

# iPerf3 test script with output in megabits per second (Mbps)
# Runs iPerf3 in both Reverse mode (-R) and Normal mode
# Tests eight clients in each mode (192.168.1.2 to 192.168.1.9)
# Each mode runs from 1 to 31 parallel streams (-P 1 to -P 31)
# Accepts 3 arguments: Firmware version, AP name, Band (2G, 5G, 6G)
# Extracts and compares values: Exits loop if a new extracted value is lower than the previous one
# Displays the extracted value after each stream test and shows all highest values at the end
# Adds a delay after each iteration to allow the client to prepare for the next test

# Define clients from .2 to .9
CLIENTS=(192.168.1.{3..9})

# Validate input arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <firmware_version> <ap_name> <band (2G|5G|6G)>"
    exit 1
fi

FIRMWARE_VERSION="$1"
AP_NAME="$2"
BAND="$3"

# Validate band input
if [[ "$BAND" != "2G" && "$BAND" != "5G" && "$BAND" != "6G" ]]; then
    echo "Error: Band must be either 2G, 5G, or 6G."
    exit 1
fi

echo "Starting iPerf3 test..."
echo "Firmware Version: $FIRMWARE_VERSION"
echo "AP Name: $AP_NAME"
echo "Band: $BAND"

# Function to display centered mode messages
display_mode_message() {
    local mode_text="$1"
    local color="$2"
    local line="================================================"
    local total_length=${#line}
    local text_length=${#mode_text}
    local padding_left=$(( (total_length - text_length) / 2 ))
    local padding_right=$(( total_length - text_length - padding_left ))

    echo -e "$color$line\e[0m"
    printf "$color%*s%s%*s\e[0m\n" "$padding_left" "" "$mode_text" "$padding_right" ""
    echo -e "$color$line\e[0m"
}

# Declare associative arrays to store highest throughput per client for both modes
declare -A HIGHEST_DOWNLOAD
declare -A HIGHEST_UPLOAD

# Outer loop: First runs Reverse mode (-R), then runs Normal mode
for MODE in "Reverse" "Normal"; do
    if [[ "$MODE" == "Reverse" ]]; then
        REVERSE_FLAG="-R"
        FILTER="sender"
        display_mode_message "Reverse Mode (-R): Measuring Download Speed" "\e[1;34m"  # Bold Blue
    else
        REVERSE_FLAG=""
        FILTER="receiver"
        display_mode_message "Normal Mode: Measuring Upload Speed" "\e[1;36m"  # Bold White
    fi

    # Loop through each client
    for CLIENT in "${CLIENTS[@]}"; do

        # Check if iperf3 server is running
        if ! nc -z -w3 $CLIENT 5201; then
            echo -e "\e[1;31mError: iPerf3 server is NOT running on $CLIENT. Skipping.\e[0m"
            continue
        fi

        echo "Testing Client: $CLIENT"
        echo "Streams | Throughput (Mbps)"
        echo "----------------------------"

        NUMERIC_VALUE=0  # Initialize extracted numeric value to zero
        HIGHEST_VALUE=0  # Track highest value found for this client in current mode

        # Inner loop: Runs from 1 to 31 streams (-P 1 to -P 31)
        for STREAMS in {1..31}; do

            # Run iperf3 silently
            IPERF_OUTPUT=$(iperf3 -c "$CLIENT" -t 30 -P "$STREAMS" -f m $REVERSE_FLAG 2>/dev/null)

            # Extract relevant summary line based on filter
            RESULT=$(echo "$IPERF_OUTPUT" | grep "$FILTER" | tail -n 1)

            # Extract the 6th value if "SUM" is in the line, otherwise extract the 7th value
            if echo "$RESULT" | grep -q "SUM"; then
                EXTRACTED_VALUE=$(echo "$RESULT" | awk '{print $6}')
            else
                EXTRACTED_VALUE=$(echo "$RESULT" | awk '{print $7}')
            fi

            # Convert extracted value to an integer (remove decimal and non-numeric characters)
            NUMERIC_VALUE=${EXTRACTED_VALUE%.*}  # Remove decimal part

            # Ensure NUMERIC_VALUE is a valid number
            if [[ ! "$NUMERIC_VALUE" =~ ^[0-9]+$ ]]; then
                NUMERIC_VALUE=0
                continue
            fi

            # Display only the stream count and throughput value
            echo "$STREAMS       | $NUMERIC_VALUE"

            # Track the highest value found
            if [ "$NUMERIC_VALUE" -gt "$HIGHEST_VALUE" ]; then
                HIGHEST_VALUE=$NUMERIC_VALUE
            fi

            # Exit loop if performance drops
            if [ "$NUMERIC_VALUE" -lt "$HIGHEST_VALUE" ]; then
                break
            fi

            # Add delay between iterations to allow the client to recover
            sleep 3

        done

        # Store the highest value for this client in the appropriate mode
        if [[ "$MODE" == "Reverse" ]]; then
            HIGHEST_DOWNLOAD["$CLIENT"]=$HIGHEST_VALUE
        else
            HIGHEST_UPLOAD["$CLIENT"]=$HIGHEST_VALUE
        fi

        # Add delay before switching to the next client
        sleep 3

    done

done

# Display all highest values at the end for both modes
echo -e "\n\e[1;32m================ FINAL RESULTS ================\e[0m"
printf "\e[1;32m%-15s %-15s %-15s\e[0m\n" "Client" "Download (Mbps)" "Upload (Mbps)"
echo -e "\e[1;32m-------------------------------------------------------\e[0m"
for CLIENT in "${CLIENTS[@]}"; do
    printf "\e[1;32m%-15s %-15s %-15s\e[0m\n" "$CLIENT" "${HIGHEST_DOWNLOAD[$CLIENT]}" "${HIGHEST_UPLOAD[$CLIENT]}"
done
echo -e "\e[1;32m===============================================\e[0m"

#!/usr/bin/env bash



# ---- Check that at least 1 arg is given (i.e the IP) ----
if [[ "$#" -lt 1 ]]; then
    echo "Usage: $0 <ip_camera> [<cam_name>]"
    exit 1
fi

# ---- Check that .env file exists ----
if [ -f .env ]; then
source .env
else
echo "Missing .env file"
exit 1
fi 

CAM_IP="$1"

if [ -n "$2" ]; then
STR_NAME="CAM"
else
STR_NAME="$2"
fi

# ---- Main script logic ----
echo "Camera IP: $CAM_IP"

curl -k -u "$KASA_UNAME:$PWD" --ignore-content-length "https://${CAM_IP}:19443/https/stream/mixed?video=h264&resolution=hd" --output -|ffplay -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 0 -window_title "$STR_NAME" -
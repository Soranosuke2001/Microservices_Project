#!/bin/bash

# Array of folder names
folders=("Audit" "EventLogger" "Storage" "Dashboard" "Receiver" "Processing")

# Array of corresponding image names
image_names=("audit_log" "event_logger" "storage" "dashboard" "receiver" "processing")

# Length of the array
length=${#folders[@]}

# Loop through the arrays
for ((i=0; i<$length; i++)); do
    folder=${folders[$i]}
    image_name=${image_names[$i]}
    echo "Starting Docker build for $folder with image name $image_name..."

    # Build and push the Docker image for the current directory
    docker buildx build --platform linux/amd64,linux/arm64 -t "soranosuke/${image_name}:latest" --push "./$folder" &
done

# Wait for all background jobs to finish
wait

echo "All Docker builds completed."

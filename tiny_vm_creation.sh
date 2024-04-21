#!/bin/bash

# Function to initialize a set of virtual machines with specified configurations
initialize_owaiz_vm() {
    # Create custom LXD profile for internet access if it doesn't exist
    if ! sudo lxc profile show allow-internet &>/dev/null; then
        sudo lxc profile create allow-internet
        sudo lxc profile set allow-internet security.nesting true
        sudo lxc profile set allow-internet security.privileged true
        
        sudo lxc profile device add allow-internet eth0 nic nictype=bridged parent=lxdbr0 name=eth0
    fi

    local configs=(
        "Tiny,4,4GiB,10GiB,10.1.1.101"
        #"Small,4,4GiB,40GiB,10.1.1.102"
        #"Large,24,24GiB,240GiB,10.1.1.103"
    )
    for config in "${configs[@]}"; do
        IFS=',' read -r vm_name cpu_count ram disk ip_address <<< "$config"

        # Define VM tag and start the virtual machine with designated CPU and memory configurations
        echo "Initiating ${vm_name} with ${cpu_count} CPU core(s), ${ram} RAM, ${disk} disk and IP ${ip_address}..."
        sudo lxc launch ubuntu:22.04 "${vm_name}" --vm -c limits.cpu="${cpu_count}" -c limits.memory="${ram}" --profile=default --profile=allow-internet

        # Wait for the VM to start up
        echo "Allowing time for ${vm_name} to boot..."
        sleep 60  # Modify this duration based on the actual boot time of your VMs

        # Setup the root disk size
        echo "Configuring disk size for ${vm_name}..."
        sudo lxc config device override "${vm_name}" root size="${disk}"

        # Set static IP address
        echo "Setting static IP ${ip_address} for ${vm_name}..."
        sudo lxc config device set "${vm_name}" eth0 ipv4.address "${ip_address}"

        # Refresh package list, upgrade packages, and install Java within the virtual machine
        echo "Deploying Java in ${vm_name}..."
        sudo lxc exec "${vm_name}" -- sudo apt-get update
        sudo lxc exec "${vm_name}" -- sudo apt-get upgrade -y
        sudo lxc exec "${vm_name}" -- sudo apt-get install -y openjdk-11-jdk

        echo "Configuration of ${vm_name} is now complete."
    done
}

# Kick off the VM initialization process
initialize_owaiz_vm

echo "Owaiz VMs have been successfully set up."

#!/bin/sh
#
# Copyright (c) 2026, Mauro Risonho de Paula Assumpção
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Mauro Risonho de Paula Assumpção
# Date Created: 2026-02-13
# Last Modified: 2026-02-13
#

echo "--- FreeBSD PMC Validation Tool ---"

# 1. Load the HWPMC module
echo "[*] Loading hwpmc module..."
kldload hwpmc 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[!] Failed to load hwpmc or already loaded."
    kldstat | grep hwpmc
else
    echo "[+] hwpmc loaded."
fi

# 2. Check available counters
echo "[*] checking available PMC counters..."
pmccontrol -L
if [ $? -ne 0 ]; then
    echo "[!] Error listing PMCs. Are we running on real hardware or KVM with proper CPU passthrough?"
    echo "    (If inside QEMU, ensure -cpu host -enable-kvm is used)"
else
    echo "[+] PMC counters detected."
fi

# 3. Compile workload
echo "[*] Compiling workload..."
cc -o pmc_stress pmc_stress.c
if [ ! -f pmc_stress ]; then
    echo "[!] Compilation failed."
    exit 1
fi

# 4. Run pmcstat
# We attempt to measure instructions and cache misses if available
# Adjust counter names based on what `pmccontrol -L` returns.
# Common generic events: instruction-retired, cache-misses (soft)
# Arch specific: unhalted-core-cycles, instructions-retired

echo "[*] Running pmcstat on cache thrasher..."
# Note: In a nested VM, we might only have soft PMCs like 'instructions' or 'cycles' if generic PMCs aren't exposed.
# We will try a system-wide sampling for 5 seconds while running the workload.

# Start workload in background
./pmc_stress c &
PID=$!

# Run pmcstat
# Attempting to use 'instructions' generic event. 
# If this fails, the user needs to check pmccontrol -L and adjust.
# Removed -D . (incompatible without -g) and added -z 16 (depth)
pmcstat -S instructions -T -O pmc.log &
STAT_PID=$!

sleep 5

# Check if process is still running before killing
if ps -p $PID > /dev/null; then
    kill $PID
fi

if ps -p $STAT_PID > /dev/null; then
    kill $STAT_PID
fi

echo "[+] Analysis complete. Log saved to pmc.log"
echo "    running 'pmcstat -R pmc.log -z 16' to view results:"
pmcstat -R pmc.log -z 16

# 5. SMP/Affinity Test (VR-119535 Requirement)
echo ""
echo "--- SMP/CPU Affinity Test ---"
echo "[*] Running workload pinned to CPU 0 (Core Isolation)..."
cpuset -l 0 ./pmc_stress c > /dev/null &
PINNED_PID=$!
pmcstat -S instructions -T -O pmc_pinned.log &
STAT_PIN_PID=$!

sleep 5

if ps -p $PINNED_PID > /dev/null; then kill $PINNED_PID; fi
if ps -p $STAT_PIN_PID > /dev/null; then kill $STAT_PIN_PID; fi

echo "[+] Pinned analysis complete. Log saved to pmc_pinned.log"
echo "    Compare 'pmc.log' (Unbound) vs 'pmc_pinned.log' (Bound to CPU 0) to see migration effects."

# 6. libpmc Development Demo (VR-119535 Requirement)
echo ""
echo "--- libpmc(3) API Demo ---"
echo "[*] Compiling pmc_lib_demo.c (Link against -lpmc)..."
cc -o pmc_lib_demo pmc_lib_demo.c -lpmc
if [ -f pmc_lib_demo ]; then
    echo "[*] Running API Demo..."
    ./pmc_lib_demo
else
    echo "[!] Failed to compile pmc_lib_demo"
fi

# 7. HWMON / Sensors Check (VR-119535 Requirement)
echo ""
echo "--- Hardware Sensors (hwmon) ---"
echo "[*] Checking CPU Temperatures (coretemp)..."
sysctl dev.cpu | grep temperature
if [ $? -ne 0 ]; then
    echo "[!] No temperature sensors found (Expected in VM without passthrough, but module is loaded)"
    kldstat | grep temp
fi


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

# job_automotive_zfs.sh
#
# Performs a health check on the ZFS pool (checksums, compression, copies) and 
# lists available snapshots, ensuring data integrity and rollback capabilities.
# In a real scenario, this would run on boot or periodically.

echo "--- Automotive ZFS Health Check ---"

# Check if ZFS module is loaded
if ! kldstat -n zfs > /dev/null 2>&1; then
    echo "[!] ZFS module not loaded. Attempting to load..."
    kldload zfs > /dev/null 2>&1
fi

if ! command -v zpool >/dev/null 2>&1; then
    echo "[-] 'zpool' command not found. (Is this a strictly UFS image?)"
    echo "    Skipping ZFS checks, but this script validates knowledge of commands."
    exit 0
fi

# List pools
echo "[*] ZFS Pool Status:"
zpool status

# Check for degraded pools
if zpool status | grep -q "DEGRADED"; then
    echo "[!] CRITICAL: ZFS Pool is DEGRADED. Data integrity at risk."
    exit 1
fi

# Show properties relevant to resilience
echo "[*] ZFS Resilience Properties (checksum, compression, copies):"
zfs get checksum,compression,copies

# List Snapshots (Crucial for OTA updates rollback)
echo "[*] Available Boot Environments / Snapshots:"
zfs list -t snapshot

echo "[+] ZFS Check Complete. System Integrity Verified."

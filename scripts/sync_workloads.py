#!/usr/bin/env python3
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

import os
import subprocess
import sys

# Configuration matches run_lab.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SSH_PORT = 2222
SSH_USER = "root"
SSH_PASS = "toor"
HOST = "localhost"
LOCAL_DIR = os.path.join(PROJECT_ROOT, "workloads")
# We use /root/workloads/ directly. 
# Note: scp -r workloads/ user@host:/root/workloads/ results in /root/workloads/workloads if target exists.
# To sync contents INTO /root/workloads, we should be careful.
# Simplest is to copy directory contents.
REMOTE_DIR = "/root/" 

def check_sshpass():
    try:
        subprocess.run(["sshpass", "-V"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def sync():
    print("--- FreeBSD Lab: Workload Sync Tool ---")
    
    if not check_sshpass():
        print("[!] Error: 'sshpass' is not installed.")
        print("    Please run: sudo apt-get install sshpass")
        sys.exit(1)

    if not os.path.exists(LOCAL_DIR):
        print(f"[!] Error: Local directory '{LOCAL_DIR}' not found.")
        sys.exit(1)

    print(f"[*] Syncing '{LOCAL_DIR}' -> VM ({HOST}:{SSH_PORT})...")
    
    # Using scp -r workloads/ root@host:/root/
    # This will create/update /root/workloads on the guest.
    cmd = [
        "sshpass", "-p", SSH_PASS,
        "scp",
        "-P", str(SSH_PORT),
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-r",
        LOCAL_DIR,
        f"{SSH_USER}@{HOST}:{REMOTE_DIR}"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("[+] Sync complete! Files updated in VM at /root/workloads/")
    except subprocess.CalledProcessError as e:
        print(f"[!] Sync failed. Is the VM running? (Error: {e})")
        sys.exit(1)

    FINDINGS_DIR = os.path.join(PROJECT_ROOT, "findings")
    if not os.path.exists(FINDINGS_DIR):
        os.makedirs(FINDINGS_DIR)

    # Pull artifacts back
    FILES_TO_PULL = ["pmc.log", "pmc_pinned.log", "pmc_stress.core", "dtrace_profile.txt"]
    print(f"[*] Pulling artifacts from VM to '{FINDINGS_DIR}'...")
    
    for filename in FILES_TO_PULL:
        remote_path = f"{SSH_USER}@{HOST}:/root/workloads/{filename}"
        local_path = os.path.join(FINDINGS_DIR, filename)
        
        cmd_pull = [
            "sshpass", "-p", SSH_PASS,
            "scp",
            "-P", str(SSH_PORT),
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            remote_path,
            local_path
        ]
        
        try:
            # We suppress stderr here because file might not exist yet
            subprocess.run(cmd_pull, check=True, stderr=subprocess.DEVNULL)
            print(f"    [+] Retrieved: {filename}")
        except subprocess.CalledProcessError:
            print(f"    [-] Not found: {filename} (Run validation first)")

if __name__ == "__main__":
    sync()

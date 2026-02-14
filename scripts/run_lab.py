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

import pexpect
import sys
import time
import os
import subprocess

# Configuration
# Determine absolute paths based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMAGE_NAME = os.path.join(PROJECT_ROOT, "img", "freebsd_debug.qcow2")
WORKLOADS_DIR = os.path.join(PROJECT_ROOT, "workloads")

SSH_PORT = 2222
TIMEOUT = 300
MEMORY = "2G"
CPU_CORES = "2"

def main():
    print("--- FreeBSD Engineering Lab: Automated Runner (VR-119535) ---")
    
    # Simple argument parsing
    debug_mode = "--debug" in sys.argv
    zen_mode = "--zen" in sys.argv
    
    if not os.path.exists(IMAGE_NAME):
        print(f"[!] Error: {IMAGE_NAME} not found.\n    Run 'python3 scripts/setup_lab.py' first.")
        sys.exit(1)

    # VirtFS configuration to share 'workloads' directory
    if not os.path.exists(WORKLOADS_DIR):
        print(f"[!] Warning: Workloads directory not found at {WORKLOADS_DIR}")
        os.makedirs(WORKLOADS_DIR)
        
    cmd_list = [
        "qemu-system-x86_64",
        "-m", MEMORY,
        "-smp", CPU_CORES,
        "-display", "none", # Use none instead of nographic to avoid curses clutter if possible, but nographic is safer for pexpect
        "-nographic",
        "-hda", IMAGE_NAME,
        "-netdev", f"user,id=net0,hostfwd=tcp::{SSH_PORT}-:22",
        "-device", "e1000,netdev=net0",
        "-serial", "mon:stdio",
        # VirtFS args (kept for reference, though userland tools might be missing)
        "-virtfs", f"local,path={WORKLOADS_DIR},mount_tag=workloads,security_model=none,id=workloads"
    ]
    
    if zen_mode:
        print("[!] ZEN MODE ENABLED: Emulating AMD EPYC-Milan (Zen 3).")
        print("    Performance will be slower due to emulation overhead.")
        print("    This allows testing 'amd_zen3_pmc' driver attachment.")
        # Emulation requires TCG (software) usually if host is Intel, or KVM might fail to set some MSRs.
        # We try to use KVM if available but force the CPU model.
        if os.path.exists("/dev/kvm"):
             print("    [+] KVM is available, but some Zen features might be masked by Intel host.")
             cmd_list.append("-enable-kvm")
        cmd_list.append("-cpu")
        cmd_list.append("EPYC-Milan")
    elif os.path.exists("/dev/kvm"):
        cmd_list.append("-enable-kvm")
        cmd_list.append("-cpu")
        cmd_list.append("host")
    else:
        print("[!] Warning: KVM not available. PMCs will likely NOT work. Using 'max' cpu model.")
        cmd_list.append("-cpu")
        cmd_list.append("max")



    if debug_mode:
        print("[!] DEBUG MODE ENABLED: QEMU will wait for GDB on localhost:1234")
        print("    Run 'gdb kernel' and 'target remote :1234' in another terminal.")
        cmd_list.append("-s")
        cmd_list.append("-S")

    cmd = " ".join(cmd_list)
    print(f"[*] Executing: {cmd}")

    child = pexpect.spawn(cmd, encoding='utf-8')
    child.logfile = sys.stdout

    try:
        # 1. Wait for "Autoboot"
        print("\n[+] Waiting for Autoboot countdown...")
        child.expect('Autoboot', timeout=60)
        
        # 2. Interrupt boot by pressing 3 for "Escape to loader prompt"
        print("\n[+] Sending '3' to escape to loader prompt...")
        # Send '3' once and wait. Sending multiple times causes "unknown command" errors.
        child.send('3') 
        
        # 3. Wait for "OK" prompt
        print("\n[+] Waiting for loader prompt...")
        # We might get "unknown command" if we were trigger happy, or just the prompt.
        # We wait for the prompt to settle.
        child.expect(r'OK', timeout=20)
        
        # stabilize
        time.sleep(1)
        
        # Clear buffer by sending Enter and waiting for a clean OK
        print("\n[+] Clearing buffer...")
        child.sendline('')
        child.expect(r'OK', timeout=5)
        
        # 4. Set console to comconsole
        print("\n[+] Setting console to comconsole...")
        time.sleep(1)
        # Send characters slowly to avoid dropping them
        for char in 'set console="comconsole"':
            child.send(char)
            time.sleep(0.05)
        child.sendline('')
        
        # Match using exact string to avoid false positives
        child.expect('OK', timeout=30)
        
        # 5. Boot
        print("\n[+] Booting...")
        child.sendline('boot')
        
        # 6. Wait for login
        print("\n[+] Waiting for login prompt...")
        # Increase timeout for boot process
        child.expect('login:', timeout=TIMEOUT)
        
        # 7. Login as root
        print("\n[+] Logging in as root...")
        child.sendline('root')
        
        # 8. Check if password is needed (usually empty on dev images, but might be 'toor')
        i = child.expect(['Password:', '#', 'root@'], timeout=10)
        if i == 0:
            print("\n[+] Password prompt detected. Sending 'toor'...")
            child.sendline('toor')
            # Check if login successful
            j = child.expect(['#', 'root@', 'Login incorrect'], timeout=10)
            if j == 2:
                 print("\n[!] Login incorrect with 'toor'. Trying empty password...")
                 # This loop is simplified; assuming strict lab conditions.
                 child.sendline('')
                 child.expect(['#', 'root@'], timeout=10)
            
        print("\n[+] Logged in!")
        
        # 9. Make change permanent
        print("\n[+] Configuring /boot/loader.conf...")
        child.sendline('echo \'console="comconsole"\' >> /boot/loader.conf')
        child.expect(['#', 'root@'], timeout=5)
        
        # 10. Enable SSH
        print("\n[+] Enabling SSHD...")
        child.sendline('echo \'sshd_enable="YES"\' >> /etc/rc.conf')
        child.expect(['#', 'root@'], timeout=5)
        
        # Configure sshd to allow root login with password
        print("\n[+] Configuring sshd_config...")
        child.sendline('echo \'PermitRootLogin yes\' >> /etc/ssh/sshd_config')
        child.expect(['#', 'root@'], timeout=5)
        child.sendline('echo \'PermitEmptyPasswords yes\' >> /etc/ssh/sshd_config') # Just in case
        child.expect(['#', 'root@'], timeout=5)
        child.sendline('echo \'PasswordAuthentication yes\' >> /etc/ssh/sshd_config')
        child.expect(['#', 'root@'], timeout=5)
        
        # Set root password to 'toor'
        print("\n[+] Setting root password to 'toor'...")
        child.sendline('passwd')
        i = child.expect(['New Password:', 'Changing local password for root'], timeout=5)
        if i == 1:
             child.expect('New Password:', timeout=5)
        child.sendline('toor')
        child.expect('Retype New Password:', timeout=5)
        child.sendline('toor')
        child.expect(['#', 'root@'], timeout=5)
        
        # Start SSHD
        print("\n[+] Starting SSHD...")
        child.sendline('service sshd restart')
        child.expect(['#', 'root@'], timeout=10)
        
        # 11. Automate SCP Transfer (Robust fallback for VirtFS)
        print("\n[+] Automating workload deployment via SCP...")
        child.sendline('mkdir -p /root/workloads')
        child.expect(['#', 'root@'], timeout=5)
        
        # We need to run SCP from the host. 
        # Since pexpect holds the QEMU process, we can use subprocess.
        # We might need to wait for SSH to actually be up.
        print("[+] Waiting 5s for SSHD to stabilize...")
        time.sleep(5)
        
        scp_cmd = [
            "scp", 
            "-P", str(SSH_PORT), 
            "-o", "StrictHostKeyChecking=no", 
            "-o", "UserKnownHostsFile=/dev/null", 
            "-r", 
            f"{WORKLOADS_DIR}/.", 
            "root@localhost:/root/workloads/"
        ]
        
        env = os.environ.copy()
        # We are using 'toor' password. SCP needs it.
        # Installing 'sshpass' would be ideal, but we can't assume root on HOST.
        # So we tell the user what is happening.
        pass_cmd = f"sshpass -p toor {' '.join(scp_cmd)}"
        
        # Try using sshpass if available, else warn user
        try:
             subprocess.run(["sshpass", "-V"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
             print(f"[+] 'sshpass' found. Auto-deploying files...")
             ret = subprocess.run(["sshpass", "-p", "toor"] + scp_cmd, capture_output=True, text=True)
             if ret.returncode == 0:
                 print("[+] Workloads deployed successfully to /root/workloads!")
             else:
                 print(f"[!] SCP failed: {ret.stderr}")
        except FileNotFoundError:
             print("[!] 'sshpass' not found on host. Cannot auto-type password.")
             print(f"[!] Please run this manually in another terminal: \n    {' '.join(scp_cmd)}")
             print("[!] Password is: toor")

        
        print("\n[+] Lab environment ready.")
        print(f"[+] SSH is listening on localhost:{SSH_PORT}")
        print("[+] You are logged in as root. 'workloads' should be in /root/workloads.")
        
        # Keep the session alive
        child.logfile = None # Disconnect logger to avoid encoding conflicts in interactive mode
        child.interact()
        
    except pexpect.ExceptionPexpect as e:
        print(f"\n[!] Error: {e}")
        # Try to close gracefully
        child.close()
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")

if __name__ == "__main__":
    main()

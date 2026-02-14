<!--
Copyright (c) 2026, Mauro Risonho de Paula Assumpção
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author: Mauro Risonho de Paula Assumpção
Date Created: 2026-02-13
Last Modified: 2026-02-13
-->

# FreeBSD PMC Validation Lab Workflow

This workflow automates the setup, execution, and validation of the FreeBSD PMC Lab.

1. **Setup the Environment**
   Downloads the FreeBSD image and installs dependencies.
   // turbo

   ```bash
   python3 scripts/setup_lab.py

   # Create .venv and install requirements
   ./scripts/install_dependencies.sh
   # Activate environment
   source .venv/bin/activate
   ```

2. **Run the Lab (Choose One)**

   **Option A: Standard Mode (Intel Host / Generic)**
   Boots the VM. Optimized for KVM if available.

   ```bash
   python3 scripts/run_lab.py
   ```

   **Option B: AMD Zen 3 Emulation (Deep Dive)**
   Boots the VM with `EPYC-Milan` CPU model.

   ```bash
   python3 scripts/run_lab.py --zen
   ```

   _Note: This step is interactive. You will see the boot process and an SSH termination status._

3. **Deploy Workloads (Hot Reload)**
   Push the latest code from `workloads/` to the VM and pull artifacts (logs/cores) to `findings/`.
   Run this in a **new terminal** while the lab is running.
   // turbo

   ```bash
   python3 scripts/sync_workloads.py
   ```

4. **Validation (Interactive SSH)**
   Connect to the VM to run manual tests.

   ```bash
   ssh -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@localhost
   ```

5. **In-Guest Validation Commands**
   Paste these commands inside the SSH session to verify PMC support:

   ```bash
   # Check Hardware Model
   sysctl hw.model

   # Load PMC Module
   kldload hwpmc

   # Check Driver Attachment
   dmesg | grep -i pmc

   # List Counters
   pmccontrol -L

   # Run Automated Test Suite
   sh validate_pmc.sh
   ```

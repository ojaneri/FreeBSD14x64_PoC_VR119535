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

# FreeBSD14x64_PoC_VR119535: PMC Validation Lab

This lab environment serves as a **Technical Portfolio and Proof-of-Concept** for the **FreeBSD Kernel Testing Engineer (PMC Validation)** role (Req: VR-119535). It implements a simulated environment to perform Performance Monitoring Counters (PMC) validation, upstream integration, and debugging.

## Quick Start

1.  **Setup Environment:**

    ```bash
    python3 scripts/setup_lab.py
    ```

    _Downloads FreeBSD image, installs dependencies, checks KVM._

    ```bash
    # (Optional) Setup Python venv
    ./scripts/install_dependencies.sh
    ```

2.  **Run Lab:**

    ```bash
    python3 scripts/run_lab.py
    ```

    _Boots FreeBSD in QEMU, configures console, enables SSH._

3.  **Run Validation (Inside Lab):**
    From your host (while `run_lab.py` is running):

    ```bash
    # Upload workloads
    scp -P 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null workloads/* root@localhost:/root/

    # SSH into guest
    ssh -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@localhost
    ```

    Inside FreeBSD:

    ```bash
    sh validate_pmc.sh
    ```

## Lab Structure

| File                                | Description                                                    |
| :---------------------------------- | :------------------------------------------------------------- |
| `scripts/setup_lab.py`              | Consolidates environment setup and image downloading.          |
| `scripts/run_lab.py`                | Automated QEMU runner with PMC support (`-cpu host`).          |
| `workloads/pmc_stress.c`            | C program generating Cache Misses and Branch Mispredictions.   |
| `workloads/validate_pmc.sh`         | Script to load `hwpmc` and run `pmcstat` analysis.             |
| `findings/`                         | Directory storing collected artifacts (logs, cores, profiles). |
| `LUXOFT_FREEBSD_JOB-VR-119535.*.md` | Detailed job analysis and requirements.                        |

## PMC Validation Scenarios

The `workloads/` directory contains tools to simulate the job requirements:

1.  **Measure Cache Misses:**
    - **Goal:** Verify `pmcstat` can detect L2/L3 thrashing.
    - **Tool:** `pmc_stress c` (walks through a 64MB array with 4KB stride).
2.  **Measure Branch Misprediction:**
    - **Goal:** Verify counters for branch prediction units.
    - **Tool:** `pmc_stress b` (random conditional jumps).

## Requirements

- **Linux Host** with KVM support (`/dev/kvm`) is highly recommended for real PMC access.
- **QEMU** with `qemu-system-x86_64`.
- **Python 3** with `pexpect` and `tqdm`.

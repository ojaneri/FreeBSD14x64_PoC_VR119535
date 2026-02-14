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

# Job Description: FreeBSD Kernel Testing Engineer (PMC Validation) (VR-119535)

This document outlines the technical specifications and requirements for the **FreeBSD Kernel Testing Engineer (PMC Validation)** role (Req: VR-119535), targeting the automotive sector.

## 1. Job Post Metadata

- **Requisition ID:** VR-119535
- **Date Posted:** 02/12/2026
- **Sector:** Automotive Industry (C Embedded)
- **Location:** Remote Brazil
- **Specialization:** C Embedded

## 2. Strategic Project Description

Luxoft is assembling a team to work on the **Performance Monitoring Counter (PMC)**. The goal is not just to maintain, but to **develop new features** and integrate them upstream.

- **Main Focus:** `hwmon`, `libpmc`, `pmcstat`.
- **Hardware:** Specific support for **AMD Zen era** processors.

## 3. Responsibility Matrix (Minute Details)

| Responsibility           | What You Must Prove              | Engineering Detail                                                                                                                      |
| :----------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **Develop PMC**          | Ability to extend the framework. | Knowledge of how the FreeBSD kernel handles architecture-specific performance events (PMU).                                             |
| **Investigate Perform.** | Mastery of profiling tools.      | Practical use of `pmcstat` to identify "hot loops" or "cache misses" in kernel code.                                                    |
| **Bug Fixes**            | Low-level debugging.             | Ability to use `kgdb` to analyze memory dumps and trace stack corruption.                                                               |
| **Upstream Integration** | Open source collaboration.       | Familiarity with the community review process (atomic commits, clear messages, response to feedback).                                   |
| **AMD Zen Support**      | x86_64 Hardware Specialist.      | Understanding of AMD-exclusive **IBS** (Instruction Based Sampling) counters and how they differ from Intel's LBR (Last Branch Record). |

## 4. Detailed Skills (Interview Checklist)

### Must Have

- **Experience (7+ years):** Focus on operating systems development or infrastructure software.
- **x86 Microarch:** Know how to explain the difference between **Instruction Retirement**, **Branch Prediction** and how PMC measures this.
- **C Language Expert:**
  - Kernel data structures (linked lists, radix trees).
  - Safe programming (no `std` library, kernel built-ins only).
- **FreeBSD Internals:**
  - Driver hierarchy (`newbus`).
  - SMP subsystem and CPU affinity.

### Nice to Have

- **Upstream Contributions:** Any previous commit in FreeBSD is a "game changer".
- **AMD Zen Deep Dive:** Real experience with optimization for Zen 3/4.

## 5. Automotive Context (Critical)

The job is under the **Automotive** vertical. In FreeBSD, this usually means:

- **Low Latency Networks:** Adapting the TCP/IP stack or using frameworks like `netmap`.
- **Data Integrity:** Configuring ZFS for maximum resilience against sudden power failures.
- **Security Compliance:** Development following best practices that may align with standards like **ISO 26262** (functional safety), although FreeBSD is not officially certified, its robustness is used as a base.

---

_Document generated for technical consolidation._

/*
 * Copyright (c) 2026, Mauro Risonho de Paula Assumpção
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Author: Mauro Risonho de Paula Assumpção
 * Date Created: 2026-02-13
 * Last Modified: 2026-02-13
 */

/*
 * pmc_lib_demo.c - VR-119535
 * 
 * Demonstrates "Ability to extend the framework" by using libpmc(3) directly.
 * This program programmatically allocates a hardware counter (instructions)
 * and measures a workload without using external tools like pmcstat.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pmc.h>

#define WORKLOAD_LOOPS 1000000

// Volatile to prevent optimization
volatile int sink = 0;

void dummy_workload() {
    for (int i = 0; i < WORKLOAD_LOOPS; i++) {
        sink++;
    }
}

int main() {
    int pmcid;
    uint64_t start_count, end_count;
    
    printf("--- libpmc(3) Developer Demo ---\n");

    // 1. Initialize the library
    if (pmc_init() < 0) {
        perror("[-] pmc_init failed (module not loaded?)");
        return 1;
    }

    // 2. Allocate a process-scope counting PMC
    // We try 'instructions' which is a generic alias
    if (pmc_allocate("instructions", PMC_MODE_TC, 0, PMC_CPU_ANY, &pmcid) < 0) {
        perror("[-] pmc_allocate failed (counters unavailable?)");
        printf("    (If inside QEMU, ensure -cpu host is passed)\n");
        return 1;
    }
    printf("[+] PMC Allocated (ID: %d)\n", pmcid);

    // 3. Attach to self
    if (pmc_attach(pmcid, 0) < 0) { // 0 = self
        perror("[-] pmc_attach failed");
        return 1;
    }

    // 4. Start counting
    if (pmc_start(pmcid) < 0) {
        perror("[-] pmc_start failed");
        return 1;
    }

    // Read initial value
    if (pmc_read(pmcid, &start_count) < 0) {
        perror("[-] pmc_read failed");
        return 1;
    }

    printf("[*] Running workload (%d loops)...\n", WORKLOAD_LOOPS);
    dummy_workload();

    // Read final value
    if (pmc_read(pmcid, &end_count) < 0) {
        perror("[-] pmc_read failed");
        return 1;
    }

    printf("[+] Instructions Executed: %lu\n", end_count - start_count);

    // Cleanup
    pmc_stop(pmcid);
    pmc_release(pmcid);

    return 0;
}

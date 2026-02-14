#!/usr/sbin/dtrace -s
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
 * profile_workload.d - DTrace script for FreeBSD VR-119535 Lab
 *
 * Usage: ./profile_workload.d -c "./pmc_stress c"
 *
 * This script demonstrates "Mastery of profiling tools" by:
 * 1. Counting Context Switches (sched)
 * 2. Counting System Calls (syscall)
 * 3. Profiling Kernel Stacks (profile)
 */

#pragma D option quiet

dtrace:::BEGIN
{
	printf("--- FreeBSD DTrace Profiler (VR-119535) ---\n");
	printf("[*] Tracing Context Switches, Syscalls, and Kernel Stacks...\n");
}

/* Trace Context Switches for the target command */
sched:::off-cpu
/pid == $target/
{
	@switches = count();
}

/* Trace System Calls for the target command */
syscall:::entry
/pid == $target/
{
	@syscalls[probefunc] = count();
}

/* Profile Kernel Stacks at 99Hz to find "hot loops" */
profile:::profile-99
/pid == $target/
{
	@stacks[stack()] = count();
}

dtrace:::END
{
	printf("\n[+] Analysis Complete.\n");
	
	printf("\n--- Context Switches ---\n");
	printa(@switches);
	
	printf("\n--- Top System Calls ---\n");
	printa(@syscalls);
	
	printf("\n--- Kernel Stack Profile (Hot Spots) ---\n");
	/* Truncate to top 5 for readability in lab */
	trunc(@stacks, 5);
	printa(@stacks);
}

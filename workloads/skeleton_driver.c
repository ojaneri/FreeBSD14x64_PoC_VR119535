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
 * skeleton_driver.c
 *
 * This is a minimal Skeleton Driver (KLD) implementing the 'newbus' attachment
 * process and module lifecycle management.
 * process and module lifecycle management.
 * 
 * Implementation validation:
 * 1. DECLARE_MODULE macro.
 * 2. modevent callback (load/unload/shutdown).
 * 3. Kernel module linkage.
 *
 * To compile (needs /usr/src or kernel headers):
 * $ make -f /usr/share/mk/bsd.kmod.mk KMOD=skeleton SRCS=skeleton_driver.c
 */

#include <sys/param.h>
#include <sys/module.h>
#include <sys/kernel.h>
#include <sys/systm.h>

/* The event handler function is called when the module is loaded/unloaded */
static int
skeleton_modevent(module_t mod __unused, int event_type, void *arg __unused)
{
    int error = 0;

    switch (event_type) {
    case MOD_LOAD:
        uprintf("Skeleton Driver Loaded: Hello Kernel World!\n");
        printf("Skeleton: Initializing resources...\n");
        break;
        
    case MOD_UNLOAD:
        uprintf("Skeleton Driver Unloaded: Goodbye!\n");
        printf("Skeleton: Releasing resources...\n");
        break;
        
    case MOD_SHUTDOWN:
        printf("Skeleton: System Shutdown detected.\n");
        break;
        
    default:
        error = EOPNOTSUPP; /* Operation not supported */
        break;
    }

    return (error);
}

/* 
 * The moduledata_t structure calls our event handler 
 * "skeleton" is the name of the module.
 */
static moduledata_t skeleton_mod = {
    "skeleton",
    skeleton_modevent,
    NULL
};

/* 
 * DECLARE_MODULE(name, data, sub, order)
 * SI_SUB_DRIVERS: Subsystem - Device Drivers
 * SI_ORDER_MIDDLE: Initialization order
 */
DECLARE_MODULE(skeleton, skeleton_mod, SI_SUB_DRIVERS, SI_ORDER_MIDDLE);

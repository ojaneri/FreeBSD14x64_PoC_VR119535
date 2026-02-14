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

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE (1024 * 1024 * 64) // 64MB - larger than L3 cache
#define STEPS 10000000

// Volatile to prevent compiler optimization
volatile int sink;

void cache_thrasher() {
    printf("[*] Generating L2/L3 Cache Misses...\n");
    int *arr = malloc(ARRAY_SIZE * sizeof(int));
    if (!arr) {
        perror("malloc");
        return;
    }

    // Initialize
    for (int i = 0; i < ARRAY_SIZE; i++) {
        arr[i] = i;
    }

    // Access disjoint memory locations to thrash cache
    // Stride of 4096 (page size) to likely miss TLB too
    for (int k = 0; k < STEPS; k++) {
        // Cast to size_t to prevent 32-bit integer overflow
        size_t idx = ((size_t)k * 4096) % ARRAY_SIZE;
        sink = arr[idx];
    }

    free(arr);
}

void branch_mispredictor() {
    printf("[*] Generating Branch Mispredictions...\n");
    
    srand(time(NULL));
    int limit = rand(); 

    // Random pattern usually defeats branch predictor
    for (int i = 0; i < STEPS; i++) {
        if (rand() % 2) {
            sink++;
        } else {
            sink--;
        }
    }
}

int main(int argc, char **argv) {
    if (argc > 1) {
        if (argv[1][0] == 'c') {
            cache_thrasher();
        } else if (argv[1][0] == 'b') {
            branch_mispredictor();
        }
    } else {
        cache_thrasher();
        branch_mispredictor();
    }
    return 0;
}

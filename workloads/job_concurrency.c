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
 * job_concurrency.c
 *
 * This program implements a multithreaded counter to analyze race conditions
 * in an SMP environment and demonstrates resolution using POSIX mutex locking.
 * locking primitives. We create two threads that increment a shared counter.
 * Without locking (commented out), the result is unpredictable (race).
 * With locking (mutex), the result is correct.
 *
 * Implementation validation:
 * 1. pthreads (POSIX Threads) in FreeBSD.
 * 2. Race Conditions in SMP environments.
 * 3. Synchronization (mutexes).
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define THREADS 2
#define ITERATIONS 1000000

volatile int shared_counter = 0;
pthread_mutex_t lock;

// The unsafe function (if used without lock)
void *increment_counter(void *arg) {
    for (int i = 0; i < ITERATIONS; i++) {
        // Critical Section Start
        pthread_mutex_lock(&lock);
        
        shared_counter++;
        
        pthread_mutex_unlock(&lock);
        // Critical Section End
    }
    return NULL;
}

int main() {
    pthread_t threads[THREADS];

    printf("--- FreeBSD SMP/Concurrency Demo (Pthreads) ---\n");
    printf("[*] Spawning %d threads, each incrementing %d times.\n", THREADS, ITERATIONS);
    printf("[*] Expected Final Value: %d\n", THREADS * ITERATIONS);

    if (pthread_mutex_init(&lock, NULL) != 0) {
        perror("[-] Mutex init failed");
        return 1;
    }

    for (int i = 0; i < THREADS; i++) {
        if (pthread_create(&threads[i], NULL, increment_counter, NULL) != 0) {
            perror("[-] Thread creation failed");
            return 1;
        }
    }

    // Wait for threads
    for (int i = 0; i < THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock);

    printf("[+] Final Shared Counter: %d\n", shared_counter);

    if (shared_counter == THREADS * ITERATIONS) {
        printf("[SUCCESS] Locking correctly prevented race condition.\n");
    } else {
        printf("[FAIL] Race condition detected! Expected %d, got %d.\n", 
               THREADS * ITERATIONS, shared_counter);
    }

    return 0;
}

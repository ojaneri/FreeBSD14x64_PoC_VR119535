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
 * job_data_structures.c
 *
 * This program implements a Singly Linked List (SLIST) using FreeBSD's 
 * <sys/queue.h> macros, demonstrating standard kernel data structure manipulation.
 * specifically SLIST (Singly Linked List), which is heavily used in the
 * FreeBSD kernel (e.g., usually for task queues or simple object lists).
 *
 * Implementation validation:
 * 1. Defining a struct with a list entry.
 * 2. initializing the list head.
 * 3. Inserting elements (Head/After).
 * 4. Traversing the list (SLIST_FOREACH).
 * 5. Safe removal of elements.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/queue.h>

// Define a struct that will be part of the linked list
struct packet_buffer {
    int id;
    char data[64];
    SLIST_ENTRY(packet_buffer) entries; // Glue for the list
};

// Define the Head type
SLIST_HEAD(slisthead, packet_buffer) head = SLIST_HEAD_INITIALIZER(head);

int main() {
    struct packet_buffer *n1, *n2, *np;

    printf("--- FreeBSD Kernel Data Structures Demo (sys/queue.h) ---\n");

    // Initialize list
    SLIST_INIT(&head);

    // Create first node
    n1 = malloc(sizeof(struct packet_buffer));
    n1->id = 1;
    strcpy(n1->data, "Packet 1 (ARP)");
    SLIST_INSERT_HEAD(&head, n1, entries);
    printf("[+] Inserted Head: ID %d\n", n1->id);

    // Create second node
    n2 = malloc(sizeof(struct packet_buffer));
    n2->id = 2;
    strcpy(n2->data, "Packet 2 (ICMP)");
    SLIST_INSERT_AFTER(n1, n2, entries);
    printf("[+] Inserted After ID 1: ID %d\n", n2->id);

    // Traversal
    printf("[*] Traversing List:\n");
    SLIST_FOREACH(np, &head, entries) {
        printf("    -> ID: %d | Data: %s\n", np->id, np->data);
    }

    // Removal
    printf("[*] Removing ID 1...\n");
    SLIST_REMOVE(&head, n1, packet_buffer, entries);
    free(n1);

    // Verify
    printf("[*] List after removal:\n");
    SLIST_FOREACH(np, &head, entries) {
        printf("    -> ID: %d | Data: %s\n", np->id, np->data);
    }

    // Cleanup rest
    while (!SLIST_EMPTY(&head)) {
        n1 = SLIST_FIRST(&head);
        SLIST_REMOVE_HEAD(&head, entries);
        free(n1);
    }

    return 0;
}

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

import os
import sys
import subprocess
import requests
from tqdm import tqdm

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMAGE_URL = "https://download.freebsd.org/releases/VM-IMAGES/14.2-RELEASE/amd64/Latest/FreeBSD-14.2-RELEASE-amd64.qcow2.xz"
IMAGE_XZ = os.path.join(PROJECT_ROOT, "img", "FreeBSD-14.2-RELEASE-amd64.qcow2.xz")
IMAGE_NAME = os.path.join(PROJECT_ROOT, "img", "freebsd_debug.qcow2")

def print_header():
    print("--- FreeBSD Engineering Lab: Setup & Provisioning ---")

def check_kvm():
    if os.path.exists("/dev/kvm"):
        print("[+] KVM support detected.")
        return True
    else:
        print("[-] KVM not detected. Emulation will be slower but functional.")
        return False

def download_image():
    img_dir = os.path.dirname(IMAGE_NAME)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    if os.path.exists(IMAGE_NAME):
        print(f"[+] Image {IMAGE_NAME} already exists. Skipping download.")
        return

    if os.path.exists(IMAGE_XZ):
        print(f"[+] Compressed image {IMAGE_XZ} found. Skipping download.")
    else:
        print(f"[*] Downloading {IMAGE_URL}...")
        response = requests.get(IMAGE_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 * 1024 # 1MB

        with open(IMAGE_XZ, 'wb') as f, tqdm(
            desc=IMAGE_XZ,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                bar.update(size)

    print(f"[*] Extracting {IMAGE_XZ}...")
    subprocess.run(["unxz", "-k", "-f", IMAGE_XZ], check=True)
    
    # Rename if necessary (the extracted file will be FreeBSD-14.2-RELEASE-amd64.qcow2)
    extracted_name = IMAGE_XZ.replace(".xz", "")
    if extracted_name != IMAGE_NAME:
        print(f"[*] Renaming {extracted_name} to {IMAGE_NAME}...")
        os.rename(extracted_name, IMAGE_NAME)

    print("[+] Image ready.")

def main():
    print_header()
    check_kvm()
    download_image()
    print("[+] Setup complete. You can now run 'python3 run_lab.py'.")

if __name__ == "__main__":
    main()

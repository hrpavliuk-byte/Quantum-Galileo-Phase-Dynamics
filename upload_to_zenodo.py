#!/usr/bin/env python3
"""
Automated Zenodo Deposition Publisher for Quantum Galileo Phase Dynamics Paper
Author: H. Pavliuk Analytics System
Usage:
    python upload_to_zenodo.py [ZENODO_TOKEN] [--publish]
"""

import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILE = os.path.join(PKG_DIR, "Quantum_Galileo_Phase_Dynamics.pdf")
MD_FILE = os.path.join(PKG_DIR, "Quantum_Galileo_Phase_Dynamics.md")
TEX_FILE = os.path.join(PKG_DIR, "Quantum_Galileo_Phase_Dynamics.tex")
PNG_FILE = os.path.join(PKG_DIR, "quantum_galileo_phase_dynamics.png")
JSON_FILE = os.path.join(PKG_DIR, "zenodo_metadata_quantum_galileo.json")
ZIP_FILE = os.path.join(PKG_DIR, "Zenodo_Quantum_Galileo_Deposit.zip")

def get_token():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        return args[0]
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        return token
    return None

def main():
    token = get_token()
    auto_publish = "--publish" in sys.argv

    if not token:
        print("=" * 70)
        print("[!] ZENODO_TOKEN is required to communicate with Zenodo API.")
        print("Please provide the token in one of these ways:")
        print("  1) Run: python upload_to_zenodo.py <YOUR_ZENODO_TOKEN> [--publish]")
        print("  2) In PowerShell: $env:ZENODO_TOKEN='<YOUR_TOKEN>'; python upload_to_zenodo.py [--publish]")
        print("=" * 70)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("\n[1/4] Creating new deposition draft on Zenodo...")
    req = urllib.request.Request(
        "https://zenodo.org/api/deposit/depositions",
        data=b"{}",
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            deposition = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error creating deposition: {e.code} {e.reason}")
        print(e.read().decode("utf-8"))
        sys.exit(1)

    dep_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    reserved_doi = deposition.get("metadata", {}).get("prereserve_doi", {}).get("doi", f"10.5281/zenodo.{dep_id}")
    print(f"-> Draft created: Deposition ID = {dep_id}")
    print(f"-> Reserved DOI = {reserved_doi}")

    print("\n[2/4] Uploading files to bucket...")
    files_to_upload = [
        ("Quantum_Galileo_Phase_Dynamics.pdf", PDF_FILE),
        ("Quantum_Galileo_Phase_Dynamics.md", MD_FILE),
        ("Quantum_Galileo_Phase_Dynamics.tex", TEX_FILE),
        ("quantum_galileo_phase_dynamics.png", PNG_FILE),
        ("Zenodo_Quantum_Galileo_Deposit.zip", ZIP_FILE),
    ]

    upload_headers = {"Authorization": f"Bearer {token}"}
    for filename, filepath in files_to_upload:
        if not os.path.exists(filepath):
            print(f"-> Warning: file not found {filepath}, skipping.")
            continue
        print(f"  Uploading {filename} ({os.path.getsize(filepath):,} bytes)...")
        file_url = f"{bucket_url}/{urllib.parse.quote(filename)}"
        with open(filepath, "rb") as fp:
            file_data = fp.read()
        req_file = urllib.request.Request(file_url, data=file_data, headers=upload_headers, method="PUT")
        with urllib.request.urlopen(req_file) as resp:
            if resp.status in (200, 201):
                print(f"  -> Uploaded successfully.")
            else:
                print(f"  -> Upload returned status: {resp.status}")

    print("\n[3/4] Updating metadata...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        meta_payload = json.load(f)

    meta_url = f"https://zenodo.org/api/deposit/depositions/{dep_id}"
    req_meta = urllib.request.Request(
        meta_url,
        data=json.dumps(meta_payload).encode("utf-8"),
        headers=headers,
        method="PUT"
    )
    with urllib.request.urlopen(req_meta) as resp:
        updated_dep = json.loads(resp.read().decode("utf-8"))
        print("-> Metadata successfully updated.")

    draft_html_url = f"https://zenodo.org/deposit/{dep_id}"
    print(f"\n-> Deposition Draft Ready at: {draft_html_url}")

    if auto_publish:
        print("\n[4/4] Publishing deposition to Zenodo...")
        pub_url = f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/publish"
        req_pub = urllib.request.Request(pub_url, data=b"", headers=headers, method="POST")
        with urllib.request.urlopen(req_pub) as resp:
            published_dep = json.loads(resp.read().decode("utf-8"))
            final_doi = published_dep["doi"]
            final_record_url = published_dep["links"]["record_html"]
            print("=" * 70)
            print("SUCCESSFULLY PUBLISHED TO ZENODO!")
            print(f"Permanent DOI: https://doi.org/{final_doi}")
            print(f"Record URL:    {final_record_url}")
            print("=" * 70)
    else:
        print("\n[!] Deposition is saved as DRAFT.")
        print(f"To finalize and publish, either:")
        print(f"  a) Open {draft_html_url} in your browser and click 'Publish'")
        print(f"  b) Run: python upload_to_zenodo.py {token} --publish")

if __name__ == "__main__":
    main()

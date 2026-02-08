#!/usr/bin/env python3
import os
import sys

def sync_readme():
    source = "docs/docs/index.md"
    target = "README.md"

    if not os.path.exists(source):
        print(f"Error : {source} does not exist.")
        sys.exit(1)

    with open(source, "r", encoding="utf-8") as f:
        content = f.read()

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Synchronisation success : {source} → {target}")

if __name__ == "__main__":
    sync_readme()

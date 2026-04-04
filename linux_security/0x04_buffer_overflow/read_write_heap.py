#!/usr/bin/python3
"""Read/write a string in another process heap via /proc."""

import sys


def usage_error(msg):
    print(msg, file=sys.stdout)
    sys.exit(1)


def parse_heap_regions(pid):
    path = f"/proc/{pid}/maps"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        usage_error(f"error: cannot read {path}: {e}")

    regions = []
    for line in lines:
        if "[heap]" not in line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        start_hex, end_hex = parts[0].split("-", 1)
        if "r" not in parts[1]:
            continue
        start = int(start_hex, 16)
        end = int(end_hex, 16)
        if end > start:
            regions.append((start, end))
    return regions


def main():
    if len(sys.argv) != 4:
        usage_error(
            "usage: read_write_heap.py pid search_string replace_string"
        )

    try:
        pid = int(sys.argv[1])
    except ValueError:
        usage_error("error: pid must be an integer")

    if pid <= 0:
        usage_error("error: pid must be positive")

    try:
        search = sys.argv[2].encode("ascii")
        replace = sys.argv[3].encode("ascii")
    except UnicodeEncodeError:
        usage_error("error: strings must be ASCII")

    if not search:
        usage_error("error: search_string must be non-empty")

    if len(replace) > len(search):
        usage_error(
            "error: replace_string must not be longer than search_string"
        )

    padded = replace + b"\x00" * (len(search) - len(replace))

    regions = parse_heap_regions(pid)
    if not regions:
        usage_error("error: no readable [heap] region in maps")

    mem_path = f"/proc/{pid}/mem"
    total = 0

    try:
        mem = open(mem_path, "r+b", buffering=0)
    except OSError as e:
        usage_error(f"error: cannot open {mem_path}: {e}")

    try:
        with mem:
            for start, end in regions:
                size = end - start
                try:
                    mem.seek(start)
                    data = mem.read(size)
                except OSError as e:
                    usage_error(f"error: cannot read heap [{start:#x}-{end:#x}): {e}")

                if len(data) != size:
                    usage_error(
                        f"error: incomplete heap read [{start:#x}-{end:#x}) "
                        f"({len(data)}/{size} bytes)"
                    )

                idx = 0
                while True:
                    pos = data.find(search, idx)
                    if pos == -1:
                        break
                    addr = start + pos
                    try:
                        mem.seek(addr)
                        mem.write(padded)
                    except OSError as e:
                        usage_error(f"error: write failed at {addr:#x}: {e}")
                    total += 1
                    idx = pos + len(search)
    except OSError as e:
        usage_error(f"error: {mem_path}: {e}")

    if total == 0:
        usage_error("error: string not found in heap")

    print("SUCCESS!")


if __name__ == "__main__":
    main()

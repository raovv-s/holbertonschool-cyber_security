#!/usr/bin/python3
"""HEAP Bufferoverflow"""

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
        perms = parts[1]
        if "r" not in perms:
            continue
        start = int(start_hex, 16)
        end = int(end_hex, 16)
        if end > start:
            regions.append((start, end))
    return regions


def find_non_overlapping(haystack, needle):
    out = []
    idx = 0
    n = len(needle)
    limit = len(haystack) - n
    while idx <= limit:
        pos = haystack.find(needle, idx)
        if pos == -1:
            break
        out.append(pos)
        idx = pos + n
    return out


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
    try:
        mem = open(mem_path, "r+b", buffering=0)
    except OSError as e:
        usage_error(f"error: cannot open {mem_path}: {e}")

    total = 0
    try:
        with mem:
            for start, end in regions:
                size = end - start
                try:
                    mem.seek(start)
                    heap_data = mem.read(size)
                except OSError as e:
                    usage_error(f"error: cannot read heap at {start:#x}: {e}")

                if len(heap_data) < size:
                    usage_error(
                        f"error: short read heap [{start:#x}-{end:#x}) "
                        f"({len(heap_data)}/{size} bytes)"
                    )

                for off in find_non_overlapping(heap_data, search):
                    addr = start + off
                    try:
                        mem.seek(addr)
                        mem.write(padded)
                    except OSError as e:
                        usage_error(f"error: write failed at {addr:#x}: {e}")
                    total += 1
    except OSError as e:
        usage_error(f"error: {mem_path}: {e}")

    if total == 0:
        usage_error("error: string not found in heap")

    print("SUCCESS!")


if __name__ == "__main__":
    main()

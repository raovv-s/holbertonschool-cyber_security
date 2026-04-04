#!/usr/bin/python3
""" Heap Buffer Overflowing."""

import sys


def fail():
    print("FAIL")
    sys.exit(1)


def parse_heap_regions(pid):
    try:
        with open(f"/proc/{pid}/maps", "r") as f:
            regions = []
            for line in f:
                if "[heap]" not in line:
                    continue
                parts = line.split()
                start, end = parts[0].split("-")
                if "r" not in parts[1]:
                    continue
                regions.append((int(start, 16), int(end, 16)))
            return regions
    except:
        fail()


def main():
    if len(sys.argv) != 4:
        fail()

    try:
        pid = int(sys.argv[1])
        search = sys.argv[2].encode()
        replace = sys.argv[3].encode()
    except:
        fail()

    if not search or len(replace) > len(search):
        fail()

    replace_padded = replace + b"\x00" * (len(search) - len(replace))

    regions = parse_heap_regions(pid)
    if not regions:
        fail()

    try:
        with open(f"/proc/{pid}/mem", "r+b", buffering=0) as mem:
            total = 0
            for start, end in regions:
                mem.seek(start)
                data = mem.read(end - start)

                idx = 0
                while True:
                    pos = data.find(search, idx)
                    if pos == -1:
                        break
                    mem.seek(start + pos)
                    mem.write(replace_padded)
                    total += 1
                    idx = pos + len(search)

        if total > 0:
            print("SUCCESS!")
        else:
            fail()

    except:
        fail()


if __name__ == "__main__":
    main()

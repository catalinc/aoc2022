def find_start_of_marker(s: str, maker_len: int) -> int:
    i = 0
    while (end := i + maker_len) < len(s):
        buff = set(s[i : end])
        if len(buff) == maker_len:
            return end
        i += 1
    return -1


import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day6.txt"
with open(fname) as infile:
    data_buffer = infile.read()

# part 1 & 2
print(find_start_of_marker(data_buffer, 4))
print(find_start_of_marker(data_buffer, 14))

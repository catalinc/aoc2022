from typing import Iterator


class File:
    def __init__(
        self, name: str, size: int = 0, is_dir: bool = False, parent: "File" = None
    ) -> None:
        self.name = name
        self.size = size
        self.is_dir = is_dir
        self.parent = parent
        if self.is_dir:
            self.children: dict[str, File] = {}

    def get_total_size(self) -> int:
        if self.size != 0:
            return self.size
        if self.is_dir:
            for f in self.children.values():
                self.size += f.get_total_size()
        return self.size

    def __repr__(self) -> str:
        return f"File(name={self.name}, size={self.size}, is_dir={self.is_dir})"


def parse_fs(term_output: str) -> File:
    root, cwd = None, None
    for line in term_output.splitlines():
        if line.startswith("$ cd "):
            dname = line[5:]
            if dname == "..":
                cwd = cwd.parent
            else:
                if not root:
                    root = File(name=dname, is_dir=True)
                    cwd = root
                else:
                    cwd = cwd.children[dname]
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir "):
            dname = line[4:]
            cwd.children[dname] = File(name=dname, is_dir=True, parent=cwd)
        else:
            fsize, fname = line.split(" ")
            cwd.children[fname] = File(name=fname, size=int(fsize), parent=cwd)
    return root


def walk_fs(file: File, filter_fn) -> Iterator[File]:
    if filter_fn(file):
        yield file
    if file.is_dir:
        for f in file.children.values():
            yield from walk_fs(f, filter_fn)


import sys

fname = sys.argv[1] if len(sys.argv) == 2 else "input/day7.txt"
with open(fname) as infile:
    root_dir = parse_fs(infile.read())

# part 1
print(
    sum(
        f.size
        for f in walk_fs(root_dir, lambda f: f.is_dir and f.get_total_size() < 100000)
    )
)

# part 2
total = 70000000
free = 30000000
used = root_dir.get_total_size()

all_dirs = list(walk_fs(root_dir, lambda f: f.is_dir))
all_dirs.sort(key=lambda f: f.get_total_size())
for d in all_dirs:
    if total - (used - d.get_total_size()) >= free:
        print(d.get_total_size())
        break

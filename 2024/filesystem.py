#!/usr/bin/env python3

"""Dataclass version of AoC 2024 Day 9"""

import dataclasses
import heapq


@dataclasses.dataclass()
class DiskBlock:
    """Class representing a file or free block in the filesystem"""

    start: int
    end: int
    fileno: int = None

    def __post_init__(self):
        assert self.end > self.start

    def __lt__(self, other):
        """Files are ordered in reverse by end block descending"""
        if self.fileno is not None:
            return self.end > other.end
        return self.start < other.start

    def size(self) -> int:
        return self.end - self.start

    def sum(self) -> int:
        return (
            sum(self.fileno * n for n in range(self.start, self.end))
            if self.fileno is not None
            else 0
        )


@dataclasses.dataclass
class Filesystem:
    input: dataclasses.InitVar[str]
    files: list[DiskBlock] = dataclasses.field(init=False)
    free: list[DiskBlock] = dataclasses.field(init=False)

    def __post_init__(self, input):
        self.files = []
        self.free = []
        offset = 0
        for i, c in enumerate(input):
            num_blocks = int(c)
            if not num_blocks:
                continue
            if i % 2 == 0:
                # Files are stored as (-end, -start, fileno)
                self.files.append(DiskBlock(offset, offset + num_blocks, i // 2))
            else:
                # Free space represnted as (start, end, None)
                self.free.append(DiskBlock(offset, offset + num_blocks))
            offset += num_blocks
        heapq.heapify(self.files)
        heapq.heapify(self.free)

    def defrag_blocks(self) -> int:
        while self.free and self.free[0].start < self.files[0].end:
            file = heapq.heappop(self.files)
            free_block = heapq.heappop(self.free)
            moved_blocks = min(file.size(), free_block.size())
            heapq.heappush(
                self.files,
                DiskBlock(
                    free_block.start, free_block.start + moved_blocks, file.fileno
                ),
            )
            if moved_blocks < file.size():
                file.end -= moved_blocks
                heapq.heappush(self.files, DiskBlock(file.start, file.end, file.fileno))
            free_block.start += moved_blocks
            if free_block.size() > 0:
                heapq.heappush(self.free, free_block)
        total = 0
        for block in self.files:
            total += sum(block.fileno * n for n in range(block.start, block.end))
        return total

    def defrag_wholefile(self) -> int:
        free_blocks = sorted(self.free)
        files = sorted(self.files, key=lambda b: b.fileno, reverse=True)
        self.files = []
        for file in files:
            free_block = None
            for i, b in enumerate(free_blocks):
                if b.start > file.start:
                    break
                if b.size() >= file.size():
                    free_block = (i, b)
                    break
            if free_block is None:  # No room
                self.files.append(file)
                continue
            i, free_block = free_block
            assert free_block.size() >= file.size()
            self.files.append(
                DiskBlock(free_block.start, free_block.start + file.size(), file.fileno)
            )
            free_block.start += file.size()
            if free_block.size() <= 0:
                free_blocks.pop(i)

        return self.checksum()

    def checksum(self) -> int:
        return sum(block.sum() for block in self.files)


if __name__ == "__main__":
    from aocd.models import Puzzle

    p = Puzzle(year=2024, day=9)
    fs = Filesystem(p.input_data)
    print(fs.defrag_blocks())
    fs = Filesystem(p.input_data)
    print(fs.defrag_wholefile())
    print(p.answers)

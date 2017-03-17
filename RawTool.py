from FileMetaData import FileMetadata
from FileBuffer import FileBuffer
import numpy as np
from struct import unpack


class raw_tools:
    def __init__(self):
        pass

    def get_metadata(self, file_name: str):
        self.file_buffer = FileBuffer(file_name)
        self.metadata = FileMetadata(self.file_buffer)
        if self.metadata.status != 0:
            print('bad status')
            print(self.metadata.status_message)
            return -1
        self.raw_ifd = self.metadata.raw_ifd

    def get_beyer(self):
        print('in get_beyer')
        base = self.raw_ifd.offset
        height = self.raw_ifd.height
        width = self.raw_ifd.width
        blocks = int(width / 32)
        b = memoryview(self.file_buffer.tmf)

        for row in range(self.raw_ifd.height):
            for index in range(blocks):
                block = base + (row * width) + (index * 32)
                max0 = (b[block:block+2])
                max0 = (max0 >> 5) & 0x7F
                i = 1

    def get_interpolated(self):
        pass

    def get_post_processed(self):
        pass

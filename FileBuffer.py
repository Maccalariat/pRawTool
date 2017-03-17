from struct import unpack
import numpy as np
from ctypes import c_ubyte, c_uint16, c_uint32


class FileBuffer():
    def __init__(self, file_name: str):
        """Create an in-memory numpy array of the file

        Parameters
        ----------
        file_name : string
            Name of file.
            The file is automatically closed after copying into a numpy in-memory array.
        """

        self.tmf = np.fromfile(file_name, dtype=np.uint8, count=-1)

        self.endian = (unpack('2s', self.tmf[0:2]))[0].decode()
        # endian, fourtytwo, first_offset = unpack('2sBl', self.tmf[0:8])

        if self.endian == "II":
            self.endian = '<'
        elif self.endian == "MM":
            self.endian = '>'
        else:
            print("invalid endian specification")
            exit()
            self.first_offset = (unpack(self.endian + 'L', self.tmf[4:8]))[0]

        print("exit __init__")

    def get_uint16(self, offset: int) -> int:
        return (unpack(self.endian + "H", self.tmf[offset:offset + 2]))[0]

    def get_uint32(self, offset: int) -> int:
        return (unpack(self.endian + 'L', self.tmf[offset:offset + 4]))[0]

    def get_block(self, offset: int, length: int) -> object:
        """

        :type length: object
        """
        return self.tmf[offset:offset + length]

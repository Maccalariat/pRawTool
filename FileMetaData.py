from ctypes import *
from FileBuffer import FileBuffer


class TiffIFD:
    def __init__(self):
        self.file_offset = 0
        self.ifd_type = 0
        self.width = 0
        self.height = 0
        self.bps = 0
        self.comp = 0
        self.phint = 0
        self.offset = 0
        self.flip = 0
        self.samples = 0
        self.stripByteCount = 0
        self.tile_width = 0
        self.tile_lengh = 0
        self.shutter = 0
        self.sonyRawFileType = 0
        self.rowsPerStrip = 0


class FileMetadata:
    def __init__(self, file_buffer: FileBuffer) -> None:
        self.status = 0
        self.status_message = ''
        print('FileMetadata.__init__')
        self.file_buffer = file_buffer
        self.tiff_ifd_list = []
        self.endian = file_buffer.endian
        self.make = ''
        self.model = ''
        if file_buffer.tmf[2] != 0x2A:
            print("wrong magic number - invalid tiff file")
            self.status = 99
            self.status_message = 'wrong magic number - invalid tiff file'
        self.parse_file()

        # get the non-scaled image
        for ifd in self.tiff_ifd_list:
            if ifd.type == 0:
                self.raw_ifd = ifd

        # some memory management
        self.tiff_ifd_list.clear()

    def parse_file(self):
        first_offset = self.file_buffer.get_uint16(4)
        next_ifd = first_offset
        while next_ifd != 0:
            next_ifd = self.process_ifd(next_ifd)

    def process_ifd(self, offset: int) -> int:
        """

        :type offset: int
        """
        de_count = self.file_buffer.get_uint16(offset)
        print("DE of ", de_count, " entries")
        ifd = TiffIFD()
        ifd.offset = offset
        self.tiff_ifd_list.append(ifd)
        o = offset + 2
        for index in range(1, de_count + 1):
            self.process_de((index - 1) * 12 + o, ifd)
        return self.file_buffer.get_uint32(offset + 2 + (de_count * 12))

    def process_de(self, offset: int, ifd: TiffIFD) -> None:
        tag = self.file_buffer.get_uint16(offset)
        tag_type = self.file_buffer.get_uint16(offset + 2)
        tag_count = self.file_buffer.get_uint32(offset + 4)
        tag_value_offset = self.file_buffer.get_uint32(offset + 8)
        print('tag: ', tag)
        if tag == 0x14A:  # value = 330 SubIFD
            ifd.type = tag_value_offset
            self.process_ifd(tag_value_offset)
        elif tag == 0x00FE:     # subfiletype
            ifd.type = tag_value_offset
        elif tag == 0x010F:     # MAKE
            self.make = ''.join(map(chr, (self.file_buffer.get_block(tag_value_offset, tag_count))))
            print("it's a ", self.make, " Jim")
        elif tag == 0x0110:     # model
            self.model = ''.join(map(chr, (self.file_buffer.get_block(tag_value_offset, tag_count))))
            print("it's a ", self.make, "of type ", self.model, " Jim")
        elif tag == 0x0100:     # ImageWidth
            ifd.width = tag_value_offset
        elif tag == 0x0101:     # ImageHeight
            ifd.height = tag_value_offset
        elif tag == 0x0111:     # StripOffsets - assumed to be one right now
            ifd.offset = tag_value_offset
        elif tag == 0x0116:     # RowsPerStrip
            ifd.rowsPerStrip = tag_value_offset
        elif tag == 0x0117:     # StripByteCounts
            ifd.stripByteCount = tag_value_offset

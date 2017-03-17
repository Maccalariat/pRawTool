from RawTool import raw_tools

if __name__ == '__main__':
    print('started rawtools test')
    rt = raw_tools()
    rt.get_metadata('sony1.ARW')
    rt.get_beyer()
    print('finished rawtools test')
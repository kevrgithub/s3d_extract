import sys, os, struct, operator, zlib

class File:
    def __init__(self):
        self.Checksum = 0
        self.Offset   = 0
        self.Size     = 0

def DecompressFile(file, size):

    # the data is stored in chunks
    # have to decompress each chunk and combine it

    filecontents = ''

    inflated = 0

    while inflated != size:

        # compressed size
        filedeflatedlength, = struct.unpack('i', file.read(4))

        # decompressed size
        fileinflatedlength, = struct.unpack('i', file.read(4))

        filedatacompressed = file.read(filedeflatedlength)

        filecontents = filecontents + zlib.decompress(filedatacompressed)

        inflated += fileinflatedlength

    return filecontents

filelist = []

filelistnames = []

print 'EverQuest S3D Extract'

extracttexturesonly = 0

numarguments = len(sys.argv)

if numarguments > 0:
    if sys.argv[1] == 'textures':
        extracttexturesonly = 1

filenames = [filename for filename in os.listdir('.') if os.path.isfile(filename) if '.s3d' in filename]

for filename in filenames:

    filelist = []

    filelistnames = []

    print 'File Name', filename

    file = open(filename, 'rb')

    filesoffset, = struct.unpack('i', file.read(4))

    #print 'Files Offset:', hex(filesoffset)

    filemagicnumber, = struct.unpack('i', file.read(4))

    #print 'File Magic Number:', hex(filemagicnumber)

    # 542328400 == 0x20534650 == 'PFS '
    if (filemagicnumber != 542328400):

        print 'File PFS signature not found!'
        continue

    file.seek(filesoffset)

    numfiles, = struct.unpack('i', file.read(4))

    print 'Number of Files:', numfiles

    for i in xrange(numfiles):

        filelistfile = File()

        filelistfile.Checksum, = struct.unpack('i', file.read(4))
        filelistfile.Offset,   = struct.unpack('i', file.read(4))
        filelistfile.Size,     = struct.unpack('i', file.read(4))

        filelist.append(filelistfile)

    # sort the files by offset
    filelist.sort(key = operator.attrgetter('Offset'))

    # the last file contains the file names of all the files

    #print 'Last File Offset:', hex(filelist[-1].Offset)

    file.seek(filelist[-1].Offset)

    filecontents = DecompressFile(file, filelist[-1].Size)

    #print 'File Contents:', filecontents

    temp = open('temp.txt', 'wb')
    temp.write(filecontents)
    temp.close()

    filecontents = open('temp.txt', 'rb')

    filecontents.seek(0)

    numstrings, = struct.unpack('i', filecontents.read(4))

    for i in xrange(numfiles - 1):

        filelistnamelength, = struct.unpack('i', filecontents.read(4))

        #print 'File List File Name Length:', filelistnamelength

        filelistnamestring = filecontents.read(filelistnamelength)

        filelistname = filelistnamestring.decode('ascii')

        #print 'File List File Name:', filelistname

        filelistnames.append(filelistname)

    filecontents.close()

    filefoldername = filename[:-4]

    if not os.path.exists(filefoldername):

        os.mkdir(filefoldername)

    for i in xrange(numfiles - 1):

        if extracttexturesonly == 1:

            if not '.bmp' in filelistnames[i]:
                if not '.BMP' in filelistnames[i]:
                    if not '.dds' in filelistnames[i]:
                        if not '.DDS' in filelistnames[i]:

                            continue

        file.seek(filelist[i].Offset)

        outputfilecontents = DecompressFile(file, filelist[i].Size)

        outputfilename = filefoldername + '\\' + filelistnames[i]

        print outputfilename

        outputfile = open(outputfilename, 'wb')
        outputfile.write(outputfilecontents)
        outputfile.close()

    file.close()

os.remove('temp.txt')

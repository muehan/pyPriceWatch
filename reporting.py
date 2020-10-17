
fileWriter = {}

def write(text):
    fileWriter = getFileWriter()
    fileWriter.write(text + '\n')

def getFileWriter():
    global fileWriter
    if fileWriter:
        return fileWriter
    else:
        fileWriter = open('report.txt', 'a')
        return fileWriter

def close():
    if fileWriter:
        return fileWriter.close()
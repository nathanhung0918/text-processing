
# python huff-decompress.py -s 'word' -f mobydick.txt

import getopt,sys,pickle,array,importlib,time,os
# mImport = __import__('huff-compress')
class CommandLine:#decide method word/char
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:], 's:f:')
        opts = dict(opts)
        self.exit = True
        if '-s' in opts:
            if opts['-s'] in ('char', 'word'):
                self.symbolType = opts['-s']
        else:
            self.symbolType = 'word'
        if '-f' in opts:
            self.infile = opts['-f']
            self.infile1 = os.path.splitext(self.infile)[0]
            self.infile2 = os.path.splitext(self.infile)[1]        
        else:
            infile = "mobydick.txt"
            self.infile1 = os.path.splitext(infile)[0]#mobydick
            self.infile2 = os.path.splitext(infile)[1]#.txt
class MakeNode:
    def __init__(self,symbol,prob):
        self.symbol = symbol
        self.prob = prob
        self.code = ""
        self.lchild = None
        self.rchild = None

class ReadFile:
    def __init__(self,infile1):
        self.mDict = pickle.load( open( infile1 + "-symbol-model.pkl", "rb" ) )
        self.mData = ""
        self.mStory = ""
        self.Tree = MakeNode(None,0)
        with open(infile1 + ".bin", "rb") as binary_file:
            byte = binary_file.read(1)
            temp = int.from_bytes(byte, byteorder='big')#byte to int
            trans = "{0:b}".format(temp)
            data = ""
            if len(trans) < 8:
                for i in range(8 - len(trans)):
                    data += "0"
                data += trans
                self.mData += data
            else:
                self.mData += trans
            while byte :
                data = ""
                byte = binary_file.read(1)
                temp = int.from_bytes(byte, byteorder='big')
                trans = "{0:b}".format(temp)
                if len(trans) < 8:
                    for i in range(8 - len(trans)):
                        data += "0"
                    data += trans
                    self.mData += data
                else:
                    self.mData += trans

    def treeReconStruct(self):
        for mSymbol in self.mDict:
            currentNode = self.Tree
            mCode = self.mDict[mSymbol]
            for c in mCode:
                if c == "1":
                    newNode = MakeNode(None,0)
                    newNode.code = "1"
                    if currentNode.lchild == None:
                        currentNode.lchild = newNode
                    currentNode = currentNode.lchild
                if c == "0":
                    newNode = MakeNode(None,0)
                    newNode.code = "0"
                    if currentNode.rchild == None:
                        currentNode.rchild = newNode
                    currentNode = currentNode.rchild
            currentNode.symbol = mSymbol

    def decompress(self,symbolType):
        currentNode = self.Tree
        for c in self.mData:
            if currentNode.symbol == None:
                if c == "1":
                    currentNode = currentNode.lchild
                if c == "0":
                    currentNode = currentNode.rchild
            if currentNode.symbol == "****":
                break
            if currentNode.symbol != None:
                self.mStory += currentNode.symbol
                currentNode = self.Tree

    def outPut(self,infile):
        f = open(infile1 + "-decompressed.txt", "w")
        f.write(self.mStory)
        f.close()

if __name__ == '__main__':   
    start = time.time()
    cmd = CommandLine()
    symbolType = cmd.symbolType
    infile1 = cmd.infile1 
    infile2 = cmd.infile2
    mFile = ReadFile(infile1)
    print("aaa",time.time())
    mFile.treeReconStruct()
    mFile.decompress(symbolType)
    mFile.outPut(infile1)
    end = time.time()
    print("decompress time: ",end - start)  


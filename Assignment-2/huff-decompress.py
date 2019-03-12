# python huff-decompress.py -s 'word' -f mobydick.txt

import getopt,sys,pickle,array,importlib,time,os
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
    def __init__(self,infile):
        self.mDict = pickle.load( open( infile1 + "-symbol-model.pkl", "rb" ) )
        self.mData = ""
        self.mStory = ""
        self.Tree = MakeNode(None,0)
        
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

    def decompress(self,infile):
        currentNode = self.Tree
        f = open(infile1 + "-decompressed.txt", "w")
        with open(infile + ".bin", "rb") as binary_file:
            byte = binary_file.read(1)
            while byte :            
                temp = int.from_bytes(byte, byteorder='big')
                trans = "{0:08b}".format(temp)
                for c in trans:
                    if currentNode.symbol == None:
                        if c == "1":
                            currentNode = currentNode.lchild
                        if c == "0":
                            currentNode = currentNode.rchild
                    if currentNode.symbol == "****":
                        break
                    if currentNode.symbol != None:
                        self.mStory = currentNode.symbol
                        f.write(self.mStory)
                        currentNode = self.Tree    
                byte = binary_file.read(1)
  
        f.close()

if __name__ == '__main__':   
    start = time.time()
    cmd = CommandLine()
    symbolType = cmd.symbolType
    infile1 = cmd.infile1 
    infile2 = cmd.infile2
    mFile = ReadFile(infile1)
    print("read time:",time.time()-start)
    mFile.treeReconStruct()
    print("tree time:",time.time()-start)
    mFile.decompress(infile1)
    print("decompress time:",time.time()-start)
    end = time.time()


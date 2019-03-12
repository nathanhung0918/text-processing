 # python huff-compress.py -s 'word' -f mobydick.txt

import sys, getopt, re, time, array,pickle,time,os

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

class IndexLoader:#load the data from file and count freq
    def __init__(self,symbolType,infile):
        self.counts = {}
        self.total = 0
        if symbolType == 'word':
            wordRE = re.compile(r'[A-Za-z]+|\d|\W')
            with open(infile,'r') as infile:
                for line in infile:
                    for word in wordRE.findall(line):
                        if word not in self.counts:
                            self.counts[word] = 0
                        self.counts[word] += 1
                        self.total += 1

        if symbolType == 'char':
            with open(infile,'r') as infile:
                mChar = infile.read(1)
                if mChar not in self.counts:
                    self.counts[mChar] = 0
                self.counts[mChar] += 1
                self.total += 1
                while mChar:
                    mChar = infile.read(1)
                    if mChar not in self.counts:
                        self.counts[mChar] = 0
                    self.counts[mChar] += 1
                    self.total += 1

    def getIndex(self):
        return self.counts    

    def getTotal(self):
        return self.total  #char / word

class MakeNode:#structure of Node
    def __init__(self,symbol,prob):
        self.symbol = symbol
        self.prob = prob
        self.code = ""
        self.lchild = None
        self.rchild = None
      
class MakeTree:#create huffman tree
    def __init__(self,nodeList):
        self.nodeList = nodeList
        self.codes = {}

    def getList(self):
        return self.nodeList

    def combineNsort(self):# combine and sort till one Node last
        for i in range(len(nodeList)-1):
            sortedList = sorted(self.nodeList,key = lambda x:x.prob)
            first = sortedList[0]
            second = sortedList[1]
            newProb = first.prob + second.prob
            newNode = MakeNode(None,newProb)
            newNode.lchild = sortedList[0]
            newNode.rchild = sortedList[1]
            sortedList.append(newNode)
            del sortedList[0]
            del sortedList[0]                 
            self.nodeList = sortedList   
            

    def makeCode(self,root,str): #use the tree to make code of symbol
        if(root.symbol != None):
            self.codes[root.symbol] = root.code
        if(root.lchild != None):
            root.lchild.code = root.code + "1"
            self.makeCode(root.lchild, root.code)
        if(root.rchild != None):
            root.rchild.code = root.code + "0"
            self.makeCode(root.rchild, root.code)   

    def storePickle(self,infile):#dump the model to pickle
        pickle.dump(self.codes,open(infile + "-symbol-model.pkl","wb"))

    def codeArray(self,symbolType,infile1,infile2):#write the code to byte array
        stopSign = self.codes['****']
        codeArray = array.array('B')
        nowProcessing = ""

        if symbolType == 'word':
            wordRE = re.compile(r'[A-Za-z]+|\d|\W')
            with open(infile1+infile2,'r') as infile:
                for line in infile:
                    for word in wordRE.findall(line):
                        nowProcessing += self.codes[word]
                        while len(nowProcessing)>8:
                            cutString = nowProcessing[:8]
                            codeArray.append(int(cutString,2))
                            nowProcessing = nowProcessing[8:]

            nowProcessing += stopSign
            while len(nowProcessing) > 8:
                cutString = nowProcessing[:8]
                codeArray.append(int(cutString,2))
                nowProcessing = nowProcessing[8:]
            for i in range(8-len(nowProcessing)):
                nowProcessing += "0"
            codeArray.append(int(nowProcessing,2))

        if symbolType == 'char':
            with open(infile1+infile2,'r') as infile:
                mChar = infile.read(1)
                nowProcessing += self.codes[mChar]
                while len(nowProcessing)>8:
                    cutString = nowProcessing[:8]
                    codeArray.append(int(cutString,2))
                    nowProcessing = nowProcessing[8:]
                while mChar:
                    mChar = infile.read(1)
                    nowProcessing += self.codes[mChar]
                    while len(nowProcessing)>8:
                        cutString = nowProcessing[:8]
                        codeArray.append(int(cutString,2))
                        nowProcessing = nowProcessing[8:]
            nowProcessing += stopSign
            while len(nowProcessing) > 8:
                cutString = nowProcessing[:8]
                codeArray.append(int(cutString,2))
                nowProcessing = nowProcessing[8:]
            for i in range(8-len(nowProcessing)):
                nowProcessing += "0"
            codeArray.append(int(nowProcessing,2))

        f = open(infile1 + '.bin','wb')
        codeArray.tofile(f)
        f.close()
                    
if __name__ == '__main__':   
    start = time.time()
    cmd = CommandLine()
    infile1 = cmd.infile1 
    infile2 = cmd.infile2
    index = IndexLoader(cmd.symbolType,infile1+infile2).getIndex()
    nodeList = []
    for symbol in index:
    	temp = MakeNode(symbol,index[symbol])
    	nodeList.append(temp)
    stopSign = "****"
    stopNode = MakeNode(stopSign,0)
    nodeList.append(stopNode)

    mTree = MakeTree(nodeList)
    mTree.combineNsort()
    mList = mTree.getList()

    mTree.makeCode(mList[0],mList[0].code)
    BuildModelTime = time.time()
    print("Build Model Time =" ,BuildModelTime-start)

    mTree.storePickle(infile1)

    mTree.codeArray(cmd.symbolType,infile1,infile2)
    encodeTime = time.time()
    print("Encode Time =" ,encodeTime-BuildModelTime)
    
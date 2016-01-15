#coding=utf-8
import os
import copy
'''
文件夹扫描类:
只扫描当前文件夹，不递归扫描
'''
class FileScanclass(object):
    
    ALLFILE = "all file"

    #文件夹绝对路径，需要扫描的文件特征["abc", "bcd"]
    def __init__( self, folder, feature ):
        self.folder = folder
        self.feature = list(set(copy.deepcopy(feature)))
        self.filedict = {}
        
        #判断路径是否正确
        self.__forderexsist()
        
    def __forderexsist(self):
        if os.path.exists(self.folder) == False or os.path.isdir(self.folder) == False:
            self.folder = "."
            self.feature = [FileScanclass.ALLFILE]
    
    def __marchFeature( self, filename ):
        if FileScanclass.ALLFILE == self.feature[0]:
            if FileScanclass.ALLFILE in self.filedict:
                self.filedict[FileScanclass.ALLFILE].append(filename)
            else:
                self.filedict[FileScanclass.ALLFILE] = [filename]
            return
        
        for str in self.feature:
            tempname = filename.lower()
            tempstr = str.lower()
            if tempname.find(tempstr) != -1:
                if str in self.filedict:
                    self.filedict[str].append(filename)
                else:
                    self.filedict[str] = [filename]
                return
            
    #扫描目录返回信息
    def scanFile(self):
        #print self.folder
        for filename in os.listdir(self.folder + "/"):
            path = self.folder + "/" + filename
            #print path
            if os.path.isdir(path) == True:
                continue
            self.__marchFeature(filename)
        
        return self.filedict
        
def main():
    scan = FileScanclass(r"D:/activator-dist-1.3.7", ["class", "READ", "log", "add"])
    print scan.scanFile()
    
if __name__ == "__main__":
    main()
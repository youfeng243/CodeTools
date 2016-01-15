#coding=utf-8
import zipfile
import copy
import os
'''
文件压缩类
'''
class Zipclass(object):
    #zip 文件名 需要压缩的文件路径  文件列表
    def __init__(self, zipname, path, filelist):
        self.zipname = zipname
        self.path = path
        self.filelist = filelist
        self.valid = False
        
        #对传入信息合法性进行检查
        self.__availability()
        
        #对文件进行压缩
        
    
    #筛选合法文件
    def __filevalid(self):
        
        filedict = {}
        filelist = []
        listlen = len(self.filelist)
        for i in xrange(listlen):
            
            if len(self.filelist[i]) <= 0:
                continue
            
            filepath = self.path + r"/" + self.filelist[i]
            
            #先判断文件是否存在
            if os.path.exists(filepath) == False:
                continue
            
            #去重
            if self.filelist[i] in filedict:
                continue
            
            filelist.append(self.filelist[i])
            filedict[self.filelist[i]] = filepath
        
        self.filedict = filedict
        self.filelist = copy.deepcopy(filelist)
        if len(self.filedict) == 0:
            return False
            
        print "filedict =", self.filedict
        print "filelist =", self.filelist
        return True
    
    #判断是否包含某些特定字符
    def __matchSpecialchar(self, matchstr, speciallist):
        
        for i in speciallist:
            if matchstr.find(i) != -1:
                return True
        
        return False
        
    #判断zip name的合法性
    def __zipnamevalid(self):
        if len(self.zipname) <= 0:
            return False
        
        #文件名命名合法性判断
        if self.__matchSpecialchar( self.zipname, "\\/:*?\"<>|" ) == True: 
            print "WARN: zipname invalid"
            return False
        
        self.zipname += r".zip"
        
        print "zipname =", self.zipname
        return True
        
        
    #信息合法性检查
    def __availability(self):
        
        #判断路径是否合法
        if os.path.isdir(self.path) == False:
            print "ERROR: path invalid!"
            return
        
        #筛选合法的文件名
        if self.__filevalid() == False:
            print "ERROR: have no valid file"
            return
        
        
        #zip文件名合法性检查
        if self.__zipnamevalid() == False:
            #文件名不合法则取第一个压缩文件命名
            self.zipname = self.filelist[0].split(".")[0] + r".zip"
            print "WARN: rename zipname = ", self.zipname
        
        self.valid = True
        print "INFO: all valid"


        
def main():
    ziptest = Zipclass("test", ".", ["zipclass.py", "zipclass.py", "zipclass.py", "fasd"])
        
if __name__ == "__main__":
    main()
        
        

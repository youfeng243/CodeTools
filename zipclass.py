#coding=utf-8
import zipfile
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
        self.filedict = {}
        self.valid = False
        
        #对传入信息合法性进行检查
        self.__availability()
        
        #对文件进行压缩
        self.__compress()
    
    #文件压缩
    def __compress(self):
        
        print "INFO: begin compress..."
        
        zippath = self.path + r"/" + self.zipname
        zfile = zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED, True)
        for i in self.filedict:
            try:
                zfile.write(self.filedict[i])
            except:
                IOError("压缩当前文件失败" + i)
        zfile.close()
        
        print "INFO: compress success!"
    
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
        self.filelist = filelist
        if len(self.filedict) == 0:
            return False
            
        print "INFO: filedict =", self.filedict
        print "INFO: filelist =", self.filelist
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
        return True
        
    def __renamezip( self, filename ):
        
        path = self.path + r"/" + filename + r".zip"
        if os.path.exists(path) == False:
            return
        
        cnt = 0
        while True:
            newfilename = filename + str(cnt)
            path = self.path + r"/" + newfilename + r".zip"
            if os.path.exists(path) == False:
                self.zipname = newfilename
                return
            cnt += 1
        
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
            self.zipname = self.filelist[0].split(".")[0]
        
        self.__renamezip(self.zipname)
        self.zipname += r".zip"
        print "INFO: zipname = ", self.zipname
        
        self.valid = True
        print "INFO: all valid"


        
def main():
    ziptest = Zipclass("state-changetest", ".", ["zipclass.py", "新建文本文档.txt", "README.md", "test.txt", "state-change.log"])
        
if __name__ == "__main__":
    main()
        
        

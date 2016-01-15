#coding=utf-8
import zipfile
import threading
import copy
import time
import os

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
    
    #判断是否是压缩文件
    def isZipFile(self, filepath):
        #判断是否是压缩文件
        return zipfile.is_zipfile(filepath)
    
    #文件压缩
    def __compress(self):
        
        if self.valid == False:
            return
        
        print "INFO: begin compress..."
        
        zippath = self.path + r"/" + self.zipname
        zfile = zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED, True)
        for i in self.filedict:
            try:
                #zfile.write(i)
                zfile.write(self.filedict[i])
                #print self.filedict[i]
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
            
            #对压缩包不进行压缩
            #ext = self.filelist[i].split(".")[-1]
            #if ext == "zip" or ext == "rar" or ext == "7z":
            #    continue
            
            filepath = self.path + r"/" + self.filelist[i]
            
            #判断是否是压缩文件
            if zipfile.is_zipfile(filepath) == True:
                continue
            
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
            
        #print "INFO: filedict =", self.filedict
        #print "INFO: filelist =", self.filelist
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
        
        while True:
            newfilename = filename + time.strftime('%Y%m%d%H%M%S', time.gmtime())
            path = self.path + r"/" + newfilename + r".zip"
            if os.path.exists(path) == False:
                self.zipname = newfilename
                return
        
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
        #print "INFO: zipname = ", self.zipname
        
        self.valid = True

def work( file, filepath,  scandict ):
    zipname = file + time.strftime('%Y%m%d', time.gmtime())
    zippoint = Zipclass(zipname, filepath, scandict[file])
    for path in scandict[file]:
        temppath = filepath + "/" + path
        if zippoint.isZipFile(temppath) == True:
            continue
        try:
            if os.path.exists(temppath):
                os.remove(temppath)
        except:
            print("ERROR: delete error " + temppath)
    
def main():
    filepath = r"E:/C++Code/FixStockClient/Debug/StockDataFile"
    filefeature = ["FixQuoteLog", "perStockContributeLog", "quoteLog"]
    scandict = FileScanclass(filepath, filefeature).scanFile()
    
    threads = []
    for file in scandict:
        t = threading.Thread( target = work, args = ( file, filepath, scandict ) )
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        threading.Thread.join(t)
    
    print "INFO: All compressed !!!"

if __name__ == "__main__":
    main()


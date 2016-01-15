#coding=utf-8
import zipfile
import os
'''
�ļ�ѹ����
'''
class Zipclass(object):
    #zip �ļ��� ��Ҫѹ�����ļ�·��  �ļ��б�
    def __init__(self, zipname, path, filelist):
        self.zipname = zipname
        self.path = path
        self.filelist = filelist
        self.filedict = {}
        self.valid = False
        
        #�Դ�����Ϣ�Ϸ��Խ��м��
        self.__availability()
        
        #���ļ�����ѹ��
        self.__compress()
    
    #�ļ�ѹ��
    def __compress(self):
        
        print "INFO: begin compress..."
        
        zippath = self.path + r"/" + self.zipname
        zfile = zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED, True)
        for i in self.filedict:
            try:
                zfile.write(self.filedict[i])
            except:
                IOError("ѹ����ǰ�ļ�ʧ��" + i)
        zfile.close()
        
        print "INFO: compress success!"
    
    #ɸѡ�Ϸ��ļ�
    def __filevalid(self):
        
        filedict = {}
        filelist = []
        listlen = len(self.filelist)
        for i in xrange(listlen):
            
            if len(self.filelist[i]) <= 0:
                continue
            
            filepath = self.path + r"/" + self.filelist[i]
            
            #���ж��ļ��Ƿ����
            if os.path.exists(filepath) == False:
                continue
            
            #ȥ��
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
    
    #�ж��Ƿ����ĳЩ�ض��ַ�
    def __matchSpecialchar(self, matchstr, speciallist):
        
        for i in speciallist:
            if matchstr.find(i) != -1:
                return True
        
        return False
        
    #�ж�zip name�ĺϷ���
    def __zipnamevalid(self):
        if len(self.zipname) <= 0:
            return False
        
        #�ļ��������Ϸ����ж�
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
        
    #��Ϣ�Ϸ��Լ��
    def __availability(self):
        
        #�ж�·���Ƿ�Ϸ�
        if os.path.isdir(self.path) == False:
            print "ERROR: path invalid!"
            return
        
        #ɸѡ�Ϸ����ļ���
        if self.__filevalid() == False:
            print "ERROR: have no valid file"
            return
        
        
        #zip�ļ����Ϸ��Լ��
        if self.__zipnamevalid() == False:
            #�ļ������Ϸ���ȡ��һ��ѹ���ļ�����
            self.zipname = self.filelist[0].split(".")[0]
        
        self.__renamezip(self.zipname)
        self.zipname += r".zip"
        print "INFO: zipname = ", self.zipname
        
        self.valid = True
        print "INFO: all valid"


        
def main():
    ziptest = Zipclass("state-changetest", ".", ["zipclass.py", "�½��ı��ĵ�.txt", "README.md", "test.txt", "state-change.log"])
        
if __name__ == "__main__":
    main()
        
        

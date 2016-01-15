#coding=utf-8
import zipfile
import copy
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
        self.valid = False
        
        #�Դ�����Ϣ�Ϸ��Խ��м��
        self.__availability()
        
        #���ļ�����ѹ��
        
    
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
        self.filelist = copy.deepcopy(filelist)
        if len(self.filedict) == 0:
            return False
            
        print "filedict =", self.filedict
        print "filelist =", self.filelist
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
        
        self.zipname += r".zip"
        
        print "zipname =", self.zipname
        return True
        
        
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
            self.zipname = self.filelist[0].split(".")[0] + r".zip"
            print "WARN: rename zipname = ", self.zipname
        
        self.valid = True
        print "INFO: all valid"


        
def main():
    ziptest = Zipclass("test", ".", ["zipclass.py", "zipclass.py", "zipclass.py", "fasd"])
        
if __name__ == "__main__":
    main()
        
        

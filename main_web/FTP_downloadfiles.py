#coding=utf-8

import ftplib
import os
import socket

class TXT_FTP_INFO:
    def __init__(self):
        self.name = "FTP_IP_user_password.txt"
        self.infomation = []
    def read(self):
        print u'从 %s 中读取访问对象及账户密码'%('/'+self.name)
        try:
            fileTxt = open(self.name,'r')
        except Exception,e:
            print e
            return
        for line in fileTxt:
            line = line.strip()
            line = line.strip()
            self.infomation.append(line)
        return self.infomation

class FTP_DOWNLOAD_APPEND_FILES:
    def __init__(self):
        self.ftp = ftplib.FTP()

    def login(self,
              host_address,
              user_name,
              password,
              port):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print u'开始连接到 %s' %(host_address)
            ftp.connect(host_address, port)
            print u'成功连接到 %s' %(host_address)
            print u'开始登录到 %s' %(host_address)
            ftp.login(user_name, password)
            print u'成功登录到 %s' %(host_address)
            print ftp.getwelcome()
        except Exception:
            print u'连接或登录失败'

    def get_localFileList(self,fileTxt):
        print u'从 %s 中读取本地文件列表'%(fileTxt)
        try:
            fileTxt_obj = open(fileTxt,'r')
            local_files = []
            for line in fileTxt_obj:
                line = line.strip()
                line = line.strip()
                #print line
                local_files.append(line)

            fileTxt_obj.close()
            return local_files

        except Exception,e:
            print e
            return




    def downloadFiles(self,path,destination):
        ftp = self.ftp
        excute_file_list = self.get_localFileList('file_list.txt')
    #path & destination are str of the form "/dir/folder/something/"
    #path should be the abs path to the root FOLDER of the file tree to download

        try:
            ftp.cwd(path)
            #clone path to destination

            if not os.path.isdir(destination):
                os.makedirs(destination)

            print destination + " built"
        except OSError:
            #folder already exists at destination
            pass
        except ftplib.error_perm:
            #invalid entry (ensure input form: "/dir/folder/something/")
            print "error: could not change to "+path
            #sys.exit("ending session")

        #list children:
        filelist = ftp.nlst()
        print u"获取目标文件列表，开始下载"
        #print filelist
        append_file_list = []
        for file in filelist:
            if file in excute_file_list:
                continue
            append_file_list.append(file)
            try:
                #this will check if file is folder:
                ftp.cwd(path+file+"/")
                #if so, explore it:
                self.downloadFiles(path+file+"/",destination + "/" + file + "/")
            except ftplib.error_perm:
                #not a folder with accessible content
                #download & return
                #os.chdir(destination)
                #possibly need a permission exception catch:
                ftp.retrbinary("RETR "+file, open(os.path.join(destination,file),"wb").write)
                print file + " downloaded"
        return append_file_list

    def update_localFileList(self, file, appendFiles):
        print u'更新 %s 中文件列表'%(file)
        try:
            fileTxt = open(file,'a')
            fileTxt.writelines([x + '\n' for x in appendFiles])
            fileTxt.close()
        except Exception,e:
            print e

        return

    def get_append_files(self):
        get_ftp_info = TXT_FTP_INFO()
        ftp_info_list = get_ftp_info.read()
        hostaddr = ftp_info_list[0] # ftp地址
        username = ftp_info_list[1] # 用户名
        password = ftp_info_list[2] # 密码
        rootdir_local = ftp_info_list[3] #本地增量下载目录
        source_local = ftp_info_list[4] #本地主历史下载目录
        port = 21
        #tp = FTP(hostaddr)
        #ftp.login(username, password)
        FTP_get_files = self
        FTP_get_files.login(hostaddr, username, password, port)
        append_list = FTP_get_files.downloadFiles(source_local, rootdir_local)
        FTP_get_files.update_localFileList('file_list.txt', append_list)

'''
if  __name__ == '__main__':
    FTP_get = FTP_DOWNLOAD_APPEND_FILES()
    FTP_get.get_append_files()
'''
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler
import itchat,time,os,shutil #,platform

class MyHandler(FileSystemEventHandler):
    def on_created(self,event):
        if not event.is_directory:
            self.file_path = event.src_path
            basename = os.path.basename(self.file_path)
            for differ in self.chatrooms_dict.keys(): 
                if differ in basename:
                    room_name = self.chatrooms_dict[differ]
                    time.sleep(1) #若不增加暂停时间无法发送信息
                    try:
                        r = itchat.search_chatrooms(room_name)[0]
                        ext = ('jpeg','jpg','png','bmp','gif')
                        this_time = time.strftime('%H:%M:%S')
                        if basename.endswith(ext):
                            r.send_image(self.file_path)                            
                            print('[%s]已发送到[%s]群！==>%s'%(basename,room_name,this_time))
                            time.sleep(5)
                        else:
                            r.send_file(self.file_path)
                            print('[%s]已发送到[%s]群！==>%s'%(basename,room_name,this_time))
                            time.sleep(5)
                    except Exception as err:
                        print(err)
            self.backup_file()

class fileHandle(MyHandler):
    def in_chatroom_msg(self):
        self.chatrooms_dict={}
        while True:
            group_name = input('PUSH微信群名识别词：')
            name_differ = input('对应PUSH文件识别符：')
            self.chatrooms_dict.update({name_differ:group_name})
            print('\n')
            more = input('*** 继续增加群 Y/N ***：')
            if more.upper() == 'N':
                break
        if '' in self.chatrooms_dict:
            self.chatrooms_dict.pop('')

    def is_chatroom(self):
        el = []
        for differ in list(self.chatrooms_dict.keys()): #因dict在遍历中无法改变，所以需要转成list
            room_name = self.chatrooms_dict[differ]
            try:
                itchat.search_chatrooms(room_name)[0]
            except:
                el.append(room_name)                
                self.chatrooms_dict.pop(differ)
        if len(el) > 0:
            key_word = str(el).replace(r',','和').replace(r'[',r'（').replace(r']',r'）').replace(r']',r'）')
            print('找不到含识别词%s的微信群!'%key_word,'\n','（原因：1、群不存在；2、群没保存到通讯录；3、输入的群名识别词含特殊符号无法识别！）')
        return self.chatrooms_dict
    
    def creat_path(self):
        while True:
            self.monitor_path = input('输入监控路径(不能含中文)：')
            if (':/' in self.monitor_path or
                ':\\' in self.monitor_path):
                self.monitor_path = self.monitor_path
            else:
                self.monitor_path = os.path.join(os.getcwd(),self.monitor_path)
            if os.path.isdir(self.monitor_path):
                break
            else:
                if_creat = input('*** “%s”路径不存在！重新输入按 R 或新创建路径回车 ***：'%self.monitor_path)
                if if_creat.upper() != 'R':
                    try:
                        os.mkdir(self.monitor_path)
                        break
                    except:
                        print('%s路径无效，请重新输入！')
        return self.monitor_path

    def clear_path(self):
        ld = os.listdir(self.monitor_path)
        for i in ld:
            c_path = os.path.join(self.monitor_path,i)
            if os.path.isdir(c_path):
                pass
            else:
                os.remove(c_path)

    def backup_file(self):
        now = time.localtime(time.time())
        month_stamp = str(now[1])+'月'
        day_stamp = str(now[2])+'日'
        hour_stamp = str(now[3])+'点'
        min_stamp = str(now[4])+'分'
        
        backup_dst = os.path.join(self.monitor_path,'backup')
        if not os.path.exists(backup_dst):
            os.mkdir(backup_dst)
        backup_day_dst = os.path.join(backup_dst,month_stamp + day_stamp)
        if not os.path.exists(backup_day_dst):
            os.mkdir(backup_day_dst)      

        (old_name,file_ext) = os.path.splitext(os.path.split(self.file_path)[1])        
        new_name = old_name + '(' + hour_stamp + min_stamp + ')'+ file_ext
        new_path = os.path.join(self.monitor_path,new_name)
        time.sleep(1) #若不增加暂停时间会提示文件被占用
        try:
            os.rename(self.file_path,new_path)
            shutil.move(new_path,backup_day_dst)
        except Exception as err:
            print(err)

if __name__ == "__main__":
    fh = fileHandle()
    fh.in_chatroom_msg()
    monitor_path = fh.creat_path()
    fh.clear_path()
    itchat.auto_login(enableCmdQR=True,hotReload=True)
    fh.is_chatroom()    
    observer = Observer()
    observer.schedule(fh,monitor_path, recursive=False)  
    observer.start()
    itchat.run()
#    os.system('cls' if platform.system() == 'Windows' else 'clear')
    try:  
        while True:  
            time.sleep(1)
    except KeyboardInterrupt:  
        observer.stop()
        itchat.logout()
    observer.join() 

    	


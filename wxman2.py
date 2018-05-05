#!/usr/bin/env python
# -*- coding:utf-8 -*-


from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler

import itchat,time,os,shutil

#qunname=input('输入群名：')
filepath=input('输入文件路径：')

#itchat.auto_login()
#os.popen('taskkill.exe /IM microsoft.Photos.exe /f')

#room=itchat.search_chatrooms(name=qunname)[0]

class MyHandler(FileSystemEventHandler):
    def on_created(self,event):
        if not event.is_directory:            
            file_path=event.src_path
            #time.sleep(1)
            #room.send_image(file_path)          
            this_time=time.localtime(time.time())
            tm_day=str(this_time[1])+'月'+str(this_time[2])+'日'
            tm_hour=str(this_time[3])+'点'
            tm_min=str(this_time[4])+'分'
            bakup_dst=str(os.path.split(file_path)[0])+'\\bakup\\'
            bakup_day_dst=str(os.path.split(file_path)[0])+'\\bakup\\'+tm_day+'\\'
            new_file_path=str(os.path.split(file_path)[0])+'\\bakup\\'+tm_day+'\\'+str(os.path.split(file_path)[1])
            file_name=str(os.path.split(file_path)[1])
            file_name_ext=str(file_name.split('.')[1])
            new_file_name=new_file_path[:-4]+'('+tm_hour+tm_min+').'+file_name_ext

            if not os.path.exists(bakup_dst):
                os.mkdir(bakup_dst)
            time.sleep(4)            

            if os.path.exists(bakup_day_dst):
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)                        
                if os.path.exists(new_file_name):
                    os.remove(new_file_name)
                shutil.move(file_path,bakup_day_dst)
                os.rename(new_file_path,new_file_name)
                                
            else:
                os.mkdir(bakup_day_dst)
                shutil.move(file_path,bakup_day_dst)
                os.rename(new_file_path,new_file_name)


if __name__ == "__main__":  
    event_handler = MyHandler()  
    observer = Observer()  
    observer.schedule(event_handler, path=filepath, recursive=False)  
    observer.start()  
    try:  
        while True:  
            time.sleep(1)  
    except KeyboardInterrupt:  
        observer.stop()  
    observer.join()  

#itchat.run()	


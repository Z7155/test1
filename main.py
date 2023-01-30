import tkinter as tk
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time,os,requests,re
import tkinter.messagebox

class VIP:
    def __init__(self):
        # tkinter窗口打开。
        window = tk.Tk()
        window.geometry('450x150+380+200')

        tk.Label(window,text="万能视频解析",font=("黑体",25),fg="red",relief="flat").pack(fill='both')

        DownloadFrame = tk.LabelFrame(window,relief='flat')
        DownloadFrame.pack(fill='both')
        self.if_download = tk.IntVar()
        self.if_download.set(0)
        tk.Label(DownloadFrame,text="是否下载视频?",fg='green',font=("黑体",15)).pack(side=tk.LEFT)
        tk.Radiobutton(DownloadFrame,variable=self.if_download,value=0,text="在线观看").pack(side=tk.LEFT,padx=5)
        tk.Radiobutton(DownloadFrame,variable=self.if_download,value=1,text="边下载边观看").pack(side=tk.LEFT,padx=5)

        InputHtmlFrame = tk.LabelFrame(window,relief='flat')
        InputHtmlFrame.pack(fill='both')
        self.html=tk.StringVar()
        tk.Label(InputHtmlFrame,text='网址  ',fg='black',font=("宋体",10,"bold")).pack(side=tk.LEFT)
        tk.Entry(InputHtmlFrame,textvariable=self.html,font=('楷体',10),relief='flat',width=100).pack(side=tk.LEFT)

        tk.Button(window,text="开始解析",font=("黑体",15),command=self.jiexi).pack(pady=5)

        window.mainloop()

    def jiexi(self):
        choose = self.if_download.get()
        html = self.html.get()
        if len(html) > 59:
            html = html[:59]
        title = self.biaoti(html)
        url = "https://jx.xmflv.com/?url=" + html
        if choose==0:       # 在线观看
            os.system(f'start {url}')
        elif choose==1:     # 边观看边下载
            web = Chrome()
            web.get(url)
            tkinter.messagebox.askyesno(title="DOWNLOAD",message="您的视频加载出后请选择确定。")
            videoURL=web.find_element(By.XPATH,'//*[@id="a1"]/div[2]/video').get_attribute('src')
            tkinter.messagebox.showinfo(title="DOWNLOAD",message='start downloading!')
            resp = requests.get(videoURL)
            with open(f'{title}.mp4','wb') as f:
                f.write(resp.content)
            tkinter.messagebox.showinfo(title="DOWNLOAD",message="finish downloading!")

    def biaoti(self,url):
        tengxun = re.search('v.qq.com',url)
        aiqiyi = re.search('iqiyi.com',url)
        youku = re.search('v.youku.com',url)

        resp = requests.get(url)
        resp.encoding='utf-8'

        if tengxun:
            title = re.findall('play-title__content" data-v-cab4c54f>(.*?)</span>',resp.text)[0]
        elif aiqiyi:
            title = re.findall('irTitle" content="(.*?)"',resp.text)[0]
        elif youku:
            title = re.findall('irTitle" content="(.*?)"',resp.text)[0]
        return title

if __name__ == '__main__':
    main = VIP()

from tkinter import *
from tkinter import messagebox as mbox
from tkinter import font , filedialog
from markdown2 import Markdown
from tkhtmlview import HTMLLabel

class Window(Frame): # 主界面框架
    def __init__(self, master=None): # 初始化frame
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family='Helvetica', size=15)
        self.init_window()
    def init_window(self): # 添加样式
        # 基本配置
        self.master.title('markdown editor (markdown编辑器)') 
        self.pack(fill=BOTH, expand=1)
        # 输入框
        self.inputeditor = Text(self, width='1', font=self.myfont) 
        self.inputeditor.pack(fill=BOTH, expand=2, side=LEFT)
        # 输出区域
        self.outputbox = HTMLLabel(self, width="1", background="white", html="<h2>实时预览区</h2>")
        self.outputbox.pack(fill=BOTH, expand=2, side=RIGHT)
        self.outputbox.fit_height()
        # 事件绑定
        self.inputeditor.bind("<<Modified>>", self.onInputChange)
        # 菜单栏
        self.mainmenu = Menu(self)
        # 文件存储读取
        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label='打开', command=self.openfile)
        self.filemenu.add_command(label='另存为', command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='退出', command=self.quit)
        self.mainmenu.add_cascade(label='文件', menu=self.filemenu)
        self.master.config(menu=self.mainmenu)
    def onInputChange(self , event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        # 获取输入值并扫描,转化为markdown格式
        self.outputbox.set_html(md2html.convert(self.inputeditor.get('1.0' , END)))
    def openfile(self):
        # 文件类型
        openfilename = filedialog.askopenfilename(filetypes=
            (('Markdown File', '*.md , *.mdown , *.markdown'),
            ('Text File', '*.txt'),
            ('All Files', '*.*')))
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END) # 删除原来内容
                self.inputeditor.insert(END , open(openfilename, encoding='utf-8').read()) # 加入新的内容
            except:
                mbox.showerror('打开文件错误' , '您选择的文件：{}无法打开!'.format(openfilename))
    def savefile(self):
        filedata = self.inputeditor.get('1.0' , END) # 获取输入
        savefilename = filedialog.asksaveasfilename(filetypes = # 文件类型
                (('Markdown File', '*.md'),
                ('Text File', '*.txt')), 
            title='保存 Markdown 文件')
        if savefilename:
            try:
                # 写入文件
                f = open(savefilename , 'w', encoding='utf-8')
                f.write(filedata)
            except:
                mbox.showerror('保存文件错误' , '文件: {} 保存错误！'.format(savefilename))
root = Tk() # 新建窗口
root.geometry('800x600') # 大小
app = Window(root) # 使用框架
app.mainloop() # 主界面循环
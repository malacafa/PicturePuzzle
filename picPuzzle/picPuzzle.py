##################################################################
#Tkinter를 이용한 사진퍼즐 만들기
#by 윤성훈
##################################################################
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
from random import randrange
import time
import threading
##################################################################
#변수선언
##################################################################
blank =15
p = [None] *16
pb = [None] *16
movement=0
istime = False
ismix = False
anslist = ""
chklist = ""
l=[]
logic = False
##################################################################
#Tk창 선언
##################################################################
window = Tk()
window.title('그림 퍼즐 V.1')
window.resizable(False,False)
##################################################################
#클릭한 화면이 빈칸인지의 여부 판단
##################################################################
def chkif(click,blank):
    if logic:
        return 1
    if click//4 == blank//4:
        if abs(click%4-blank%4) ==1:
            return 1
        else:
            return 0
    if click%4 == blank%4:
        if abs(click//4-blank//4) ==1:
            return 1
        else:
            return 0
    return 0
##################################################################
#게임이 종료되었는지의 여부를 판단
##################################################################
def chkend():
    global l,score
    cnt=0
    for x in range(0,16):
        if p[x]==l[x]:
            cnt+=1
    if cnt == 16:
        score=cnt
        score_label.configure(text='score:%12d'%(score*100//16))
        return 99
    score=cnt
    score_label.configure(text='score:%12d'%(score*100//16))
##################################################################
#화면을 섞을 때 사용됨
##################################################################
def mix_button(click):
    global blank
    if chkif(click,blank):
        p[click],p[blank]=p[blank],p[click]
        pb[blank].grid()
        pb[blank].configure(image=p[blank])
        pb[click].grid_remove()
        pb[click].configure(image=p[click])
        blank=click
##################################################################
#클릭을 받아와서 퍼즐을 이동시키고 게임의 종료 여부 등 판단
##################################################################
def click_button(click):
    global istime
    global blank
    global movement
    global chklist
    global ismix

    if istime == False:
        istime = True
    if chkif(click,blank):
        p[click],p[blank]=p[blank],p[click]
        pb[blank].grid()
        pb[blank].configure(image=p[blank])
        pb[click].grid_remove()
        pb[click].configure(image=p[click])
        blank=click
        movement +=1
    else:      
        messagebox.showerror('에러','그 버튼은 움직일 수 없습니다')
    if chkend()==99:
        for x in range(16):
            pb[x].configure(state="disabled")
        istime=False
        messagebox.showinfo('성공','그 그림은 움직일 필요 없습니다')
        chklist = ""
        ismix=False
    else:
        movementlabel.configure(text="movement:%5d"%movement)
##################################################################
#상하좌우 키보드 클릭을 처리
##################################################################
def clickUp(event,k=False):
    click=blank+4
    if click < 16:
        if k:
            mix_button(click)
            return "U"
        else:
            click_button(click)
    return ""
##################################################################
def clickDown(event,k=False):
    click=blank-4
    if click >= 0:
        if k:
            mix_button(click)
            return "D"
        else:
            click_button(click)
    return ""
##################################################################
def clickLeft(event,k=False):
    click=blank+1
    if click//4 == blank//4:
        if k:
            mix_button(click)
            return "L"
        else:
            click_button(click)
    return ""
##################################################################
def clickRight(event,k=False):
    click=blank-1
    if click//4 == blank//4 :
        if k:
            mix_button(click)
            return "R"
        else:
            click_button(click)
    return ""
##################################################################
#퍼즐을 섞는 함수
##################################################################
def randmix():
    global ismix,blank,movement,istime,chklist,anslist,score
    score=0
    for x in range(16):
        pb[x].configure(state='normal')
    anslist = ''
    if ismix:
        messagebox.showerror('에러','이미 섞인 그림입니다')
        return
    ismix = True
    istime = False
    movement=0
    movementlabel.configure(text="movement:%5s"%"0")
    for x in range(100):
        clk=randrange(0,4)
        if clk==0:
            s=clickUp(0,True)
        if clk==1:
            s=clickDown(1,True)
        if clk==2:
            s=clickLeft(2,True)
        if clk==3:
            s=clickRight(3,True)
        chklist+=s
    chkend()
    while True:
        if "RL" in chklist:
            chklist=chklist.replace("RL","")
        elif "LR" in chklist:
            chklist=chklist.replace("LR","")
        elif "UD" in chklist:
            chklist=chklist.replace("UD","")
        elif "DU" in chklist:
            chklist=chklist.replace("DU","")
        else:
            break
    for c in chklist:
        if c =="U":
            anslist+="D"
        elif c =="D":
            anslist+="U"
        elif c =="R":
            anslist+="L"
        elif c =="L":
            anslist+="R"
    anslist=anslist[::-1]
##################################################################
#힌트 화면을 출력하는 함수
##################################################################
def hint():
    hint_window=Toplevel()
    hint_window.geometry("400x400")
    hint_window.title("Hint")
    photo = ImageTk.PhotoImage(Image.open("imgs/img02.jpg"))
    img=Label(hint_window,image=photo)
    img.img = photo
    img.pack()
##################################################################
#게임시간을 측정하는 함수
##################################################################
def runtime():
    global istime
    st = time.time()
    rt = 0
    while True:
        time.sleep(0.2)
        t=time.time()
        if st+1<t and istime == True:
            rt+=1
            label.configure(text='time:%5d'%rt)
            st=t
        if istime == False:
            rt = 0
            st=time.time()
##################################################################
#정답 화면을 출력하는 함수
##################################################################
def ans():
    global anslist
    cheat_window=Toplevel()
    cheat_window.geometry("350x40")
    cheat_window.title("ANS")
    i=Label(cheat_window,text="섞기 버튼을 누른 직후 명령에 따라 키보드를 누르시오")
    i.pack()
    if len(anslist) == 0:
        l=Label(cheat_window,text="섞기 버튼을 눌렀을 때만 정답이 주어집니다")
    else:
        l=Label(cheat_window,text=anslist)
    l.pack()
##################################################################
#게임을 초기화시키는 함수
##################################################################  
def reset():
    global ismix,istime,movement,blank,anslist,chklist,l,score
    score=0
    score_label.configure(text='score:%12d'%score)
    movementlabel.configure(text="movement:%5s"%"0")
    label.configure(text='time:%5d'%0)
    chklist = ""
    anslist = ""
    ismix = False
    istime = False
    movement = 0
    l=[]
    for i in range(16):
        pb[i].grid_remove()
    for i in range(16):
        p[i] = ImageTk.PhotoImage(Image.open("imgs/img" + str(i) + ".gif"))
        l.append(p[i])
        pb[i] = Button(window, image=p[i],command = partial(click_button,i))
        pb[i].grid(row=i//4+2,column=i%4)
    blank = 15
    pb[blank].grid_remove()
##################################################################
#클릭 규칙을 무시하게 해 주는 함수
##################################################################
def cheat():
    global logic
    if logic:
        logic = False
        window.title('그림 퍼즐 V.1')
    else:
        logic = True
        window.title('그림 퍼즐 V.1<Cheat On>')
##################################################################
#라벨 선언
##################################################################
score=0
movementlabel=Label(window,text="movement:%5s"%"0")
movementlabel.grid(row=0,column=0)
label=Label(window,text='time:%5d'%0)
label.grid(row=0,column=1)
score_label=Label(window,text='score:%12d'%score)
score_label.grid(row=1,column=0)
##################################################################
#초기 버튼 설정
##################################################################
l=[]
for i in range(16):
    p[i] = ImageTk.PhotoImage(Image.open("imgs/img" + str(i) + ".gif"))
    l.append(p[i])
    pb[i] = Button(window, image=p[i],command = partial(click_button,i))
    pb[i].grid(row=i//4+2,column=i%4)
pb[blank].grid_remove()
##################################################################
#키보드 입력 설정
##################################################################
window.bind("<Up>",clickUp)
window.bind("<Down>",clickDown)
window.bind("<Right>",clickRight)
window.bind("<Left>",clickLeft)
##################################################################
#버튼 선언
##################################################################
mix_btn = Button(window,text='섞기',height=2,command=randmix)
mix_btn.place(x=355,y=0)
hint_btn = Button(window,text='힌트',height=2,command=hint)
hint_btn.place(x=390,y=0)
reset_btn = Button(window,text='초기화',height=2,command=reset)
reset_btn.place(x=310,y=0)
ans_btn = Button(window,text='정답',height=2,command=ans)
ans_btn.place(x=275,y=0)
cheat_btn = Button(window,text='치트',height=2,command=cheat)
cheat_btn.place(x=240,y=0)
##################################################################
#시간 측정 스레드 실행
##################################################################
t = threading.Thread(target=runtime)
t.start()
##################################################################
#mainloop 시작
##################################################################
window.mainloop()
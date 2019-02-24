import tkinter as tk
import tkinter.messagebox
import tweepy
import time
from tweepy.parsers import JSONParser
import sys
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
##################################################
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_key = '2153338314-access_key'
access_secret = 'access_secret'
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, parser=JSONParser())
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
################################################

window = tk.Tk()
window.title('Twitter Friend Checker')
window.geometry('900x400')
canvas = tk.Canvas(window, bg='white', height=400, width=900)
canvas.pack(side='top')
tk.Label(window, text='User name 1', bg="white", font=('Arial', 14)).place(x=100, y=10)
tk.Label(window, text='User name 2', bg="white", font=('Arial', 14)).place(x=550, y=10)
user1 = tk.StringVar()
user2 = tk.StringVar()
user1.set("KingJames")
user2.set("kobebryant")
e1 = tk.Entry(window, textvariable=user1, font=('Arial', 14))
e1.place(x=100, y=50)
e2 = tk.Entry(window, textvariable=user2, font=('Arial', 14))
e2.place(x=550, y=50)
user_image = Image.open("user.jpg")
user_image = user_image.resize((200, 200), Image.ANTIALIAS)
user_image = ImageTk.PhotoImage(user_image)
l1 = tk.Label(window, image=user_image).place(x=100, y=100)
l2 = tk.Label(window, image=user_image).place(x=550, y=100)


def showphoto(user, x, y):
    try:
        userinfo = api.get_user(user)
        photo_url = str(userinfo['profile_image_url'])
        photo_url = photo_url.replace("normal", "400x400")
        u = urllib.request.urlopen(photo_url)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        photo = im.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        label = tk.Label(window, image=photo)
        label.image = photo
        label.pack()
        label.place(x=x, y=y)
    except:
        tk.messagebox.showinfo(title='Error', message='請確認名稱是否正確')


def check():
    target = user1.get()
    user = user2.get()
    relation = []
    showphoto(target, 100, 100)
    showphoto(user, 550, 100)
    try:
        relation = api.show_friendship(source_screen_name=target, target_screen_name=user)

    except tweepy.TweepError:
        time.sleep(1)
        try:
            relation = api.show_friendship(source_screen_name=target, target_screen_name=user)
        except:
            pass
    if relation:
        relat = relation['relationship']['source']
        if relat['following'] and relat['followed_by']:
            canvas.create_line(290, 150, 540, 150, arrow=tk.LAST, fill='blue', width='10', arrowshape="8 10 8")
            canvas.create_line(540, 250, 310, 250, arrow=tk.LAST, fill='red', width='10', arrowshape="8 10 8")
            tk.messagebox.showinfo(title='Result', message='BFF  !!')
        elif relat['following']:
            canvas.create_line(290, 150, 540, 150, arrow=tk.LAST, fill='blue', width='10', arrowshape="8 10 8")
            canvas.create_line(540, 250, 310, 250, arrow=tk.LAST, fill='white', width='10', arrowshape="8 10 8")
            tk.messagebox.showinfo(title='Result', message='Only ' + target + ' following ' + user)
        elif relat['followed_by']:
            canvas.create_line(290, 150, 540, 150, arrow=tk.LAST, fill='white', width='10', arrowshape="8 10 8")
            canvas.create_line(540, 250, 310, 250, arrow=tk.LAST, fill='red', width='10', arrowshape="8 10 8")
            tk.messagebox.showinfo(title='Result', message='Only ' + user + ' following ' + target)
        else:
            canvas.create_line(290, 150, 540, 150, arrow=tk.LAST, fill='white', width='10', arrowshape="8 10 8")
            canvas.create_line(540, 250, 310, 250, arrow=tk.LAST, fill='white', width='10', arrowshape="8 10 8")
            tk.messagebox.showinfo(title='Result', message='They are not friend on Twitter !!')

btn_Enter = tk.Button(window, text='Enter', command=check, font=('Arial', 14))
btn_Enter.place(x=400, y=50)

window.mainloop()

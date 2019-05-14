# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

fighters=[]
btimer=30


@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id not in fighters:
        fighters.append(createplayer(m.from_user))
        bot.send_message(m.chat.id, 'Вы успешно зашли в игру! Теперь ждите, пока ваш боец прострелит кому-нибудь яйцо.\nСоветую кинуть бота в мут!')
     
    
@bot.message_handler(commands=['settimer'])
def settimer(m):
    if m.from_user.id==441399484:
        try:
            global btimer
            btimer=int(m.text.split(' ')[1])
        except:
            pass
        
@bot.message_handler(commands=['stats'])
def stats(m):
    me=None
    for ids in fighters:
        if ids['id']==m.from_user.id:
            me=ids
    if me!=None:
        text=''
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        bot.send_message(m.chat.id, text)


def createplayer(user):
    return {
        'hp':1000,
        'damage':10,
        'killchance':5,
        'name':user.first_name,
        'id':user.id,
        'hitted':0,  # сколько раз попали
        'killed':0,   # сколько уебал
        'killer':''
           }
           
   
    
def fight():
    for ids in fighters:
        alive=[]
        for idss in fighters:
            if idss['hp']>0 and idss['id']!=ids['id']:
                alive.append(idss)
        if len(alive)>0:
            text=''
            target=random.choice(alive)
            dmg=ids['damage']+ids['damage']*(random.randint(-20, 20)/100)
            target['hp']-=dmg
            target['hitted']+=1
            text+='Вы попали в '+target['name']+'! Нанесено '+str(dmg)+' урона.\n'
            if target['hp']<=0:
                ids['killed']+=1
                target['killer']=ids['name']
                text+='Вы убили цель!\n'
            else:
                if random.randint(1,100)<=ids['killchance']:
                    target['hp']=0
                    ids['killed']+=1
                    target['killer']=ids['name']
                    text+='Вы прострелили яйцо цели! Та погибает.\n'
            bot.send_message(ids['id'], text)
    dellist=[]
    for ids in fighters:
        if ids['hp']<=0:
            dellist.append(ids)
    for ids in dellist:
        bot.send_message(ids['id'], 'Вы сдохли. Вас убил '+ids['killer'])
        me=ids
        text='Итоговые статы:\n\n'
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        bot.send_message(ids['id'], text)
        fighters.remove(ids)
    global btimer
    t=threading.Timer(btimer, fight)
    t.start()
    
fight() 

def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)   

print('7777')
bot.polling(none_stop=True,timeout=600)


# -*- coding: utf-8 -*-
from LineAPI.linepy import *
from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit
from helper import helper
try:
    with open('token.txt','r') as lg:
        tkn = lg.read()
        client = LINE(tkn)
except:
    client = LINE()
    with open('token.txt','w') as lg:
        lg.write(client.authToken)
#=======[ BOTS START ]==========[ ARSYBAI ]=============
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
botStart = time.time()
msg_dict = {}
#=============[ DATA STREAM ]=====================================================================================
with open('settings.json','r') as stg:settings = json.load(stg)
bai={"changepicture":False}
def setback():                                                                                                   
    with open('settings.json','w') as sb:json.dump(settings, sb, sort_keys=True, indent=4, ensure_ascii=False)
try:                                                                                                             
    with open("Log_data.json","r",encoding="utf_8_sig") as f:                                                    
        msg_dict = json.loads(f.read())                                                                          
except:                                                                                                          
    print("Couldn't read Log data")                                                                              
#=================================================================================================================
profile = client.getContact(clientMid)
settings['myProfile']['displayName'] = profile.displayName
settings['myProfile']['pictureStatus'] = profile.pictureStatus
settings['myProfile']['statusMessage'] = profile.statusMessage
coverId = client.getProfileDetail()['result']['objectId']
settings['myProfile']['coverId'] = str(coverId)
setback()
def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))
def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')
def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
def command(text):
    cmd = text.lower()
    return cmd
def clientBot(op):
    try:
        if op.type == 0:return
        if op.type == 5 and settings["autoadd"]==True:client.findAndAddContactsByMid(op.param2);client.sendMentionV2(op.param2,'hi @!\n{}'.format(str(settings["addmsg"])))
#===================================================================[ ARSYBAI ]=============
        if op.type == 13 and settings["autojoin"]==True:client.acceptGroupInvitation(op.param1)
#===========================================================================================
        if op.type == 25:
            try:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:to = sender
                        else:to = receiver
                    elif msg.toType == 1:to = receiver
                    elif msg.toType == 2:to = receiver
                    if msg.contentType == 0:
                        if text is None:return
                        else:
                            cmd = command(text)#ThisMain
                            if cmd=='help':client.sendMessage(to,helper().mainHelp())
                            if cmd=='self':client.sendMessage(to,helper().selfHelp())
                            if cmd=='group':client.sendMessage(to,helper().groupHelp())
                            if cmd=='settings':client.sendMessage(to,helper().setHelp())
                            #[SELF MENU]
                            if cmd=='me':client.sendContact(to,sender);client.sendMessageMusic(to, title=client.getContact(sender).displayName, subText=str(client.getContact(sender).statusMessage), url='line.me/ti/p/~arsy22bai', iconurl="http://dl.profile.line-cdn.net/{}".format(client.getContact(sender).pictureStatus), contentMetadata={})
                            if cmd=='grouplist':
                                this_list = client.getGroupIdsJoined()
                                num = 0;ls_ = '[ GROUP LIST ]\n'
                                for this_gc in this_list:
                                    num += 1
                                    ls_ += '\n{}. {}'.format(num, client.getGroup(this_gc).name)
                                client.sendMessage(to,str(ls_))
                            if cmd=='friendlist':
                                contactlist = client.getAllContactIds()
                                kontak = client.getContacts(contactlist)
                                num=0
                                msgs="List Friend\n"
                                for ids in kontak:
                                    num+= 1
                                    msgs+="\n[%i] %s" % (num, ids.displayName)
                                msgs+="\n\nTotal Friend : %i" % len(kontak)
                                client.sendMessage(to,str(msgs))
                            if cmd.startswith('add'):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        try:
                                            client.findAndAddContactsByMid(ls)
                                        except:
                                            pass
                                    cnt = client.getContact(ls).displayName
                                    client.sendMessage(to,"Success add {} to friend".format(str(cnt)))
                            if cmd.startswith('clone'):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        client.cloneProfile(ls)
                                        client.sendReplyMessage(msg_id,to,'Success Clone {}'.format(str(client.getContact(ls).displayName)))
                            if cmd=='restore':
                                profile = client.getProfile()
                                profile.displayName = settings['myProfile']['displayName']
                                profile.statusMessage = settings['myProfile']['statusMessage']
                                client.updateProfile(profile)
                                if settings['myProfile']['pictureStatus']:
                                    pict = client.downloadFileURL('http://dl.profile.line-cdn.net/' + settings['myProfile']['pictureStatus'])
                                    client.updateProfilePicture(pict)
                                coverId = settings['myProfile']['coverId']
                                client.updateProfileCoverById(coverId)
                                client.sendReplyMessage(msg_id,to,'Success restored Profile')
                            #[GROUPHELP]
                            if cmd.startswith('reinvite'):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        client.inviteIntoGroup(msg.to,[ls])
                            if cmd=='ginfo':
                                group = client.getGroup(to)
                                try:gCreator = group.creator.displayName
                                except:gCreator = "Not Found"
                                if group.invitee is None:gPending = "0"
                                else:gPending = str(len(group.invitee))
                                if group.preventedJoinByTicket == True:gQr = "Close";gTicket = "None"
                                else:gQr = "Open";gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
                                ret_ = "[ Group Info ]"
                                ret_ += "\nGroup Name : {}".format(str(group.name))
                                ret_ += "\nGroup ID : {}".format(group.id)
                                ret_ += "\nCreator : {}".format(str(gCreator))
                                ret_ += "\nMembers count : {}".format(str(len(group.members)))
                                ret_ += "\nPending Members : {}".format(gPending)
                                ret_ += "\nGroup Qr : {}".format(gQr)
                                client.sendMessage(to,str(ret_))
                            if cmd=='gmember':
                                group = client.getGroup(to)
                                ret_ = "[ Member List ]"
                                no = 0 + 1
                                for mem in group.members:
                                    ret_ += "\n{}. {}".format(str(no), str(mem.displayName))
                                    no += 1
                                ret_ += "\n[ Total {} ]".format(str(len(group.members)))
                                client.sendMessage(to, str(ret_))
                            if cmd=='tagall':
                                group = client.getGroup(to)
                                midMembers = [contact.mid for contact in group.members]
                                midSelect = len(midMembers)//20
                                for mentionMembers in range(midSelect+1):
                                    no = 0
                                    ret_ = "[ Mention Members ]"
                                    dataMid = []
                                    for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                        dataMid.append(dataMention.mid)
                                        no += 1
                                        ret_ += "\n {}. @!".format(str(no))
                                    client.sendMentionV2(to, ret_, dataMid)
                            if cmd.startswith('kick'):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        client.kickoutFromGroup(msg.to,[ls])
                            #[SETTINGS]
                            if cmd=='speedcheck':client.speedCheck(to)
                            if cmd=='autolike on':settings["autolike"]=True;setback();client.sendMessage(to,"Autolike turned on!")
                            if cmd=='autolike off':settings["autolike"]=False;setback();client.sendMessage(to,"Autolike turned off!")
                            if cmd=='autoadd on':settings["autoadd"]=True;setback();client.sendMessage(to,'Autoadd Turned ON')
                            if cmd=='autoadd off':settings["autoadd"]=False;setback();client.sendMessage(to,'Autoadd Turned OFF')
                            if cmd=='autojoin on':settings["autojoin"] = True;setback();client.sendMessage(to,"Auto join turned on")
                            if cmd=='autojoin off':settings["autojoin"] = False;setback();client.sendMessage(to,"Auto join turned off")
                            if cmd=='restart':client.sendMessage(to,'Restarting...');restartBot()
                            if cmd=='shutdown':client.sendMessage(to,'shutting down...');sys.exit('bye')
                            if cmd == "changepicture":bai["changepicture"] = True;client.sendMessage(to,"Send a picture!")
#================================================================================================================================================================
                    elif msg.contentType == 1: #poto
                        if bai["changepicture"] == True:
                            path = client.downloadObjectMsg(msg_id)
                            bai["changepicture"] = False
                            client.updateProfilePicture(path)
                            client.sendMessage(to, "Succes updated profile picture :D")
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
        if op.type == 26:
            try:
                #print ("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.contentType == 16:
                        if settings["autolike"]==True:
                            url_post = msg.contentMetadata['postEndUrl']
                            pliter = url_post.replace('line://home/post?userMid=','')
                            pliter = pliter.split('&postId=')
                            client.likePost(mid=pliter[0],postId=pliter[1])
                            client.createComment(mid=pliter[0],postId=pliter[1],text=settings["comment"])
                            client.sendMessage(to,'Like Success')
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)
while True:
    try:
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)

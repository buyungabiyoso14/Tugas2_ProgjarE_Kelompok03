#python version: Python 3.5 for Windows
import os
import socket
import sys
from thread import *

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_address=('10.151.36.250',10030)
online_list={}
group_list={}
#def send_to_all_klien(message):
#    for koneksi in online_list.itervalues():
#        koneksi.sendall(message.encode('utf-8'))

def SIGNUP(uName, uPass):
    check = uName.isalnum()
    check2 = uPass.isalnum()
    if not check :
        return 103
    elif not check2:
        return 103
    f = open('daftarAnggota.txt', 'r')
    data = f.read()
    temp = data.split('\n')
    length = len(temp)
    for x in range(0, length-1):
        temp[x] = temp[x].split(' ')
    for y in range(0, length-1):
        if temp[y][0]==uName: 
	    return 102
    f.close()
    f = open('daftarAnggota.txt', 'a+')
    ID = "%s %s\n" % (uName, uPass)
    f.write(ID)
    f.close()
    return 101

def MASUK(uName, uPass):
    f = open('daftarAnggota.txt', 'r')
    data = f.read()
    temp = data.split('\n')
    length = len(temp)
    for x in range(0, length-1):
        temp[x] = temp[x].split(' ')
    for y in range(0, length-1):
        if temp[y][0] == uName:
            if temp[y][1] == uPass:
                return 201
    f.close()
    return 202
    #return 202
def check_nonexist(uName):
    f = open('daftarAnggota.txt', 'r')
    data = f.read()
    temp = data.split('\n')
    length = len(temp)
    for x in range(0, length - 1):
        temp[x] = temp[x].split(' ')
    for y in range(0,length-1):
        if temp[y][0]==uName:
            return False
    f.close()
    return True
def check_this_client_online(conn):
    for con in online_list.itervalues():
        if(conn == con):
            return True
    return False
def check_group_member(grup,conn):
    nama = username(conn)
    for user in group_list[grup]:
        if user == nama:
            return True
    return False
def username(conn):
    for user, con in online_list.iteritems():
        if con == conn:
            return user
#def BUATGGroup():

#def JOINGGroup():

#def chatGroup():

#def KELUARGroup():

#def DAFTARUSer():

#def DAFTARGRoup():

def perintah(command,conn):
    temp=command.strip().split()
    if (check_this_client_online(conn)):
        if temp[0]=='SEND':
            if len(temp) < 3:
                message="803\n"
                conn.sendall(message.encode('utf-8'))
            else:
                if temp[1]=='PUBLIC':
                    nama = username(conn)
                    for koneksi in online_list.itervalues():
                        i = 2
                        koneksi.send('BC('+nama+'): ')
                        while i <= len(temp) - 1:
                            koneksi.send(temp[i] + ' ')
                            i += 1
                        koneksi.send('\n')
                    message = "801\n"
                    conn.sendall(message.encode('utf-8'))
                    print "801 BC BY "+nama+" SENT\n"
                else:
                    message="001\n"
                    conn.sendall(message.encode('utf-8'))
        elif temp[0]=='SEND':
            nama=username(conn)
            if (len(temp) < 3):
                conn.sendall('304\n')
            elif (check_nonexist(temp[1])):
                conn.sendall('302\n')
            elif(temp[1] not in online_list):
                conn.sendall('303\n')
            else:
                i=2
                nama = username(conn)
                online_list[temp[1]].send(nama+":")
                while i <=len(temp)-1:
                   online_list[temp[1]].send(temp[i]+' ')
                   i+=1
                online_list[temp[1]].send("\n")
                print '301 SEND '+nama+' OK\n'
                conn.sendall('301\n')
        elif temp[0]=='LOGOUT':
            conn.sendall('203\n')
            nama = username(conn)
            del online_list[nama]
            print '203 ' + nama + ' LOGOUT\n'
            conn.close()
        elif temp[0]=='DAFTARUS':
            message = "003\n"
            conn.sendall(message.encode('utf-8'))
            for user in online_list.iterkeys():
                conn.sendall(user+"\n")
        elif temp[0]=='BUATG':
            check = temp[1].isalnum()
            if len(temp)<2:
                message = "001\n"
                conn.sendall(message.encode('utf-8'))
            elif temp[1] in group_list:
                message = "402\n"
                conn.sendall(message.encode('utf-8'))
            elif not check:
                message = "403\n"
                conn.sendall(message.encode('utf-8'))
            else:
                nmGroup = temp[1]
                nama = username(conn)
                group_list[nmGroup]=[nama,]
                print "401 "+temp[1]+" BY "+nama+" BUATGD\n"
                message = "401\n"
                conn.sendall(message.encode('utf-8'))
        elif temp[0]=='JOING':
            nama = username(conn)
            if len(temp) < 2:
                message = "001\n"
                conn.sendall(message.encode('utf-8'))
            elif temp[1] not in group_list:
                message = "502\n"
                conn.sendall(message.encode('utf-8'))
            elif nama in group_list[temp[1]]:
                message = "503\n"
                conn.sendall(message.encode('utf-8'))
            else:
                group_list[temp[1]].append(nama)
                message = "501\n"
                print "501 "+nama+" JOING "+temp[1]+"\n"
                conn.sendall(message.encode('utf-8'))
        elif temp[0] == 'DAFTARGR':
            message = "004\n"
            conn.sendall(message.encode('utf-8'))
            for group_name in group_list.iterkeys():
                conn.sendall(group_name+" \n")

        elif temp[0] == 'SENDG':
            if len(temp) < 3:
                message = "703\n"
                conn.sendall(message.encode('utf-8'))
            elif temp[1] not in group_list:
                message = "702\n"
                conn.sendall(message.encode('utf-8'))
            elif check_group_member(temp[1],conn)==False:
                message = "704\n"
                conn.sendall(message.encode('utf-8'))
            else:
                nama = username(conn)
                for user in group_list[temp[1]]:
                    i=2
                    online_list[user].send(temp[1]+'('+nama+'):')
                    while i <=len(temp)-1:
                        online_list[user].send(temp[i]+' ')
                        i+=1
                    online_list[user].send('\n')
                conn.sendall('701\n')
                print "701 "+temp[1]+" "+nama+" OK\n"
        elif temp[0] == 'KELUAR':
            if len(temp) < 2:
                message = "001\n"
                conn.sendall(message.encode('utf-8'))
            elif temp[1] not in group_list:
                message = "603\n"
                conn.sendall(message.encode('utf-8'))
            elif check_group_member(temp[1],conn)==False:
                message = "602\n"
                conn.sendall(message.encode('utf-8'))
            else:
                nama = username(conn)
                for user in group_list[temp[1]]:
                    if nama == user:
                        group_list[temp[1]].remove(nama)
                conn.sendall('601\n')
                print '601 '+nama+' KELUAR '+temp[1]+'\n'
        elif temp[0]=='SIGNU' or temp[0]=='MASUK':
            message = "003\n"
            conn.sendall(message.encode('utf-8'))
        else:
            message="001\n"
            conn.sendall(message.encode('utf-8'))
    elif temp[0] == 'SIGNU':
        if len(temp) < 3:
            message = "001\n"
            conn.sendall(message.encode('utf-8'))
        else:
            SIGNU = SIGNUP(temp[1], temp[2])
            if SIGNU == 103:
                message = "103\n"
                conn.sendall(message.encode('utf-8'))
            elif SIGNU == 102:
                message = "102\n"
                conn.sendall(message.encode('utf-8'))
            elif SIGNU == 101:
                message = "101\n"
                print "101 SIGNUP "+temp[1]+" OK\n"
                conn.sendall(message.encode('utf-8'))
    elif temp[0] == 'MASUK':
        if len(temp) < 3:
            message = "001\n"
            conn.sendall(message.encode('utf-8'))
        else:
            MASUKn = MASUK(temp[1], temp[2])
            if MASUKn == 201:
                uName = temp[1]
                message = "201\n"
                print "201 MASUK " + temp[1] + " OK\n"
                conn.sendall(message.encode('utf-8'))
                online_list[uName] = conn
                # disini kirim data status MASUK, nama usernya ke list online
            elif MASUKn == 202:
                message = "202\n"
                conn.sendall(message.encode('utf-8'))
    elif not check_this_client_online(conn):
        message = "002\n"
        conn.sendall(message.encode('utf-8'))
    else:
        message = "001\n"
        conn.sendall(message.encode('utf-8'))
    
def klien(conn):
    while True:
        try:
            data = conn.recv(1024)
            if data:
                perintah(data.decode('utf-8'),conn)
            else:
                break
        except:
            conn.close()
            break
            
sock.bind(server_address)
sock.listen(1)


while True:
    koneksi,addr=sock.accept()
    #client_list.append(koneksi)
    start_new_thread(klien,(koneksi,))

koneksi.close()
sock.close()

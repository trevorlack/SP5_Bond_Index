import sys 
import win32com.client
import os
import glob
import pandas as pd
import xlsxwriter
from datetime import datetime
from FTP_Credentials import FTP_Auth

def ftp_main():
    '''Check if it is the weekend'''
    d=datetime.now()
    if d.isoweekday() in range(6,8):
        sys.exit()

    Host, Login, Password = FTP_Auth()
    os.chdir('-:/-/-/-')
    DateList = []

    for file in list(glob.glob("*SP5MAIG*.S*")):
        DateList.append(file[0:8])

    Max_Date = int(max(DateList))

    MySite = win32com.client.Dispatch('CuteFTPPro.TEConnection')

    MySite.Protocol = 'FTP'
    MySite.Host = Host
    MySite.Login = Login
    MySite.Password = Password
    #MySite.UseProxy = 'BOTH'
    MySite.Connect()

    if not MySite.IsConnected:
        print('Could not connect to: %s Aborting!' % MySite.Host)
        sys.exit(1)
    else:
        print('You are now connected to: %s' % MySite.Host)

    MySite.LocalFolder = '-:/-/-/-'
    MySite.RemoteFolder = '/Inbox'
    MySite.RemoteFilterInclude = '*SP5MAIG*;'
    #MySite.Download('*SP5MAIG*')
    #Result = MySite.GetList (MySite.RemoteFolder, "-:/-/-/ftplist.txt", "*SP5*")
    Result = MySite.GetList("/Inbox","C:/temp_list.txt","%NAME")
    FileLister = MySite.GetResult
    FTP_list = pd.read_table('C:/temp_list.txt', header=None, names='p')
    FTP_list = pd.DataFrame(FTP_list)
    FTP_list['date'] = FTP_list['p'].str[0:8]
    #FTP_list = FTP_list.rename(columns={'':'path'})
    counter = 0
    prior = 0
    CLS_Convert_List = []
    for i in range(0, len(FTP_list)):
        checker = int(FTP_list['date'].iloc[i])
        file = FTP_list['p'].iloc[i]
        if checker > Max_Date:
            MySite.Download(file)
            if checker != prior:
                counter = counter + 1
            CLS_Convert_List.append(str(checker))
            prior = checker
    if counter == 0:
        print('No new Investment Grade Index Files')
    else:
        for i in range(0,len(CLS_Convert_List)-1):
            index = pd.read_csv('-:/-/-/-/'+CLS_Convert_List[i]+'_SP5MAIG_CLS.SPFIC', sep='\t')
            writer = pd.ExcelWriter('-:/-/-/-/'+CLS_Convert_List[i]+'_SP5MAIG_CLS.xlsx')
            index.to_excel(writer, 'SP5MAIG_CLS', index=False)
            writer.save()
        print(counter, 'Day(s) of Index Files Saved Down')

    MySite.Disconnect()
    MySite.TECommand('exit')
    print(MySite.Status)


def FTP_Auth():
    Host = None
    Login = None
    Password = None

    with open("FTP_Host.txt") as I:
        Host = I.read().strip()
    with open("FTP_Login.txt") as I:
        Login = I.read().strip()
    with open("FTP_Password.txt") as I:
        Password = I.read().strip()

    return Host, Login, Password

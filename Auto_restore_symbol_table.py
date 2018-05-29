#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import zipfile
import subprocess
import commands
import tempfile

reload(sys)
sys.setdefaultencoding('utf8')

original_ipaPath = input("Please input Ipa Path : ") #原始ipa文件所在的位置
original_path_List = original_ipaPath.split('/') 
ipaAllName = original_path_List[-1] 
ipaName = ipaAllName[:-4] 
symbolIpaAllName = 'symbol_' + ipaAllName;  #打包ipa文件后的名称带ipa扩展名
PayloadSign = 'Payload'
blockJsonName = 'block_symbol.json'


ipa_dir = original_ipaPath[:-(len(ipaAllName) + 1)] #获取当前ipa文件所在的目录

project_dir = os.path.dirname(os.path.realpath(__file__)) #获取当前项目路径

restore_symbol_file_path = os.path.join(project_dir, 'restore-symbol') #restore-symbol文件所在位置

unzipFilePath = os.path.join(ipa_dir, ipaName) #解压ipa文件后得到的文件路径

symbolIpaPath = os.path.join(ipa_dir, symbolIpaAllName) #生成恢复好符号表的ipa文件的路径

block_json_path = os.path.join(ipa_dir, blockJsonName) #block结构体的文件所在的路径


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(unzipFilePath):
        pass
    else:
        os.mkdir(unzipFilePath)
    for names in zip_file.namelist():
        zip_file.extract(names,unzipFilePath)
    zip_file.close()

un_zip(original_ipaPath)  #解压ipa文件

un_zip_ipa_Payload_path = unzipFilePath + '/' + PayloadSign


def listdir(path, list_name): 
	for file in os.listdir(path):
		file_path = os.path.join(path,file)
        list_name.append(file_path)


listname = []
listdir(un_zip_ipa_Payload_path, listname)
installPackagePath = listname[0]   #得到xxx.app的路径
pathList = installPackagePath.split('/') 
installPackageName = pathList[-1] #获取xxx.app的名称
binaryName = installPackageName[:-4] 
binaryPath = installPackagePath + '/' + binaryName  #得到二进制文件的路径


symbol_binary_path = ipa_dir + '/' + binaryName

if os.path.exists(block_json_path):
	chmod_args = (restore_symbol_file_path, binaryPath, "-o", symbol_binary_path, "-j", block_json_path)
else:
    chmod_args = (restore_symbol_file_path, binaryPath, "-o", symbol_binary_path)

try:
    subprocess.check_call(chmod_args)
except subprocess.CalledProcessError as err:
    print err



cmd_mv = ('mv', symbol_binary_path, binaryPath)
try:
    subprocess.check_call(cmd_mv)
except subprocess.CalledProcessError as err:
    print err

targetDir = './' + PayloadSign
cmd_zip = ('zip', '-qr', os.path.join(os.getcwd(), symbolIpaPath), targetDir)
subprocess.check_call(cmd_zip, cwd=unzipFilePath)


cmd_rm = ('rm', '-rf', unzipFilePath)
try:
    subprocess.check_call(cmd_rm)
except subprocess.CalledProcessError as err:
    print err




























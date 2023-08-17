# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 09:32:25 2023

@author: 86130
"""

import time
import schedule
import atexit
import glob
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
import selenium.webdriver.support.ui as ui
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
optsEdge = webdriver.EdgeOptions()
import json
from tkinter import *
import traceback

from selenium.webdriver.common.keys import Keys

# 定义日志文件的句柄
log_file = None;
propertydata = None;
wait = None;

def auto_web_glados_sign_in(url):
    global wait;

    datetimelog = time.strftime("%Y{0}%m{0}%d{0}%H{0}%M{0}%S".format('_'), time.localtime(time.time())) + '\n\n开启今日签到任务\n\n';
    print(datetimelog,file=log_file);
    #edgedriver = "C:\Program Files (x86)\Microsoft\Edge\Application"
    #os.environ["webdriver.ie.driver"] = chromedriver

    #driver = webdriver.Edge(executable_path='msedge.exe')  # 选择Chrome浏览器
    driver = webdriver.Edge(options=optsEdge);   
    driver.minimize_window() # 最小化浏览器
    #driver.maximize_window()  # 最大化谷歌浏览器
    time.sleep(1)
    
    # 页面等待加载---超时时间设定为180s
    timeout = propertydata['timeout'];
    wait = ui.WebDriverWait(driver,timeout);        
    
    if login_cookie(driver, url): 
        print("登录成功\n\n",file=log_file);
    else:
        login_glados_user(driver,url);
   
    
    print("自动签到已完成\n\n\n",file=log_file);
    
    # 数据刷入硬盘
    log_file.flush();
    return 0

def login_glados_user(driver,url):  # 登录方法分装
    
    driver.get(url);  # 重新登录    

    # 等待加载网页相关资源    
    # 等待加载首页登录按钮
    wait.until(lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div/div/div[2]/a'))
    
    # 点击登录，跳转登录界面
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div/div/div[2]/a').click()  # 点击登录按钮
    
    '''第二个页面数据'''
    
    # 等待加载邮箱
    wait.until(lambda driver: driver.find_element(By.ID,'email'))
    # 等待加载验证码---按钮
    wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[2]/div/form/div[2]/label/button'))
    # 等待加载验证码---文本框
    wait.until(lambda driver: driver.find_element(By.ID,'mailcode'))
    # 等待加载登录按钮
    wait.until(lambda driver: driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/form/div[3]/span/button"))

    # 点击输入邮箱
    useremail = propertydata['email'];
    driver.find_element(By.ID,'email').click()  # 点击用户名输入框
    driver.find_element(By.ID,'email').clear()  # 清空输入框
    driver.find_element(By.ID,'email').send_keys(useremail)  # 自动敲入用户名
    time.sleep(1)
    
    # 点击发送验证码
    driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[2]/div/form/div[2]/label/button').click();

    '''界面展示'''

    window = Tk()
    window.title("glados邮箱验证码")
    window.geometry('300x100')

    code_input = Text(window,width='20',height='2')		# width宽 height高
    code_input.pack()

    def verifyCode():
        # 输入验证码
        usercode = str(code_input.get('1.0','1.20')).strip();
        driver.find_element(By.ID,'mailcode').click()  # 点击密码输入框
        driver.find_element(By.ID,'mailcode').clear()  # 清空输入框
        driver.find_element(By.ID,'mailcode').send_keys(usercode)  # 自动敲入密码

        # 销毁窗口
        window.destroy();
                                                        # 其中第一个参数是起始位置，'1.1'就是从第一行第一列后，到第一行第五列后
    btn = Button(window,text='确认',command=verifyCode)
    btn.pack()

    window.mainloop()

    '''界面展示结束'''

    # 点击登录按钮，提交登录
    driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/form/div[3]/span/button").click(); 
   
    # 延时1s等待
    time.sleep(3)
    # 保存本次的cookies
    cookies = driver.get_cookies()
    with open('config/cookies.json', 'w') as f:
        json.dump(cookies, f)
        
    # 签到
    sign_in(driver);
    
    # 数据刷入硬盘
    log_file.flush();
     
    
def sign_in(driver):
    #wait = ui.WebDriverWait(driver,3);      
    # 等待页面加载完成
    if wait is not None:
        # 点击-会员签到       
        try:
            # 等待---会员签到按钮       
            wait.until(lambda driver: driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div'))
            driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div').click(); 
        except Exception as e:
            s = traceback.format_exc()
            print(s,file=log_file);
            log_file.flush();  
    
        print("点击签到等待3s\n",file=log_file)
        time.sleep(3);
        print("点击签到\n",file=log_file)
        # 点击-签到        
        try:
            # 等待---签到按钮
            wait.until(lambda driver: driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/div/div[2]/button'))
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/div/div[2]/button').click();
        except Exception:
            s = traceback.format_exc()
            print(s,file=log_file);
            log_file.flush();  
    
         
        # 等待延时加载浏览页面  
        time.sleep(3);
    
    # 退出
    driver.quit();
    
    # 数据刷入硬盘
    log_file.flush();
    
def login_cookie(driver,url):
    if os.path.exists("config/cookies.json"):  # 判断这个文件是否存在

        # 登录前先获取链接
        driver.get(url)  # 这个是再次刷新这不不可少    
    
        with open('config/cookies.json', 'r') as f:
            cookies = json.load(f)
            
        driver.delete_all_cookies();
        
        # 添加本地cookies到driver对象中
        for cookie in cookies:            
            try:
                driver.add_cookie(cookie);
            except Exception as e:                
                s = traceback.format_exc()
                print(s,file=log_file);
                log_file.flush();  
                
            
        driver.get(url)  # 这个是再次刷新这不不可少
        
        # 延时等待加载
        time.sleep(3);
        try:
            # 判断登录是否存在，若存在则cookie超时，需要重新点击登录，跳转登录界面     
            if driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div/div/div/div/div[2]/a'):
               print('cooking失效重新登录\n',file=log_file)
               login_glados_user(driver,url);
        except:
            print('使用cooking登录成功\n',file=log_file)
            # 点击签到
            sign_in(driver);

        # 数据刷入硬盘
        log_file.flush();
        return True
    else:
        return False
   

# python的垃圾回收机制，程序终止后，会执行
@atexit.register
def clean():
    print('-'*100 + "\n",file=log_file)
    print('clean up the environment ...\n',file=log_file)
    schedule.clear('daily-tasks-sign-in-glados');
    print("python程序终止代码-----\n\n\n\n\n",file=log_file)
    
    log_file.flush();
    # 关闭终端文件流
    try:
       if log_file is not None:
            log_file.close(); 
    except Exception as e:
        s = traceback.format_exc()
        print(s,file=log_file);
        log_file.flush();
       
    
def star_task():
    global log_file;
    global propertydata;
    
    # 创建日志文件句柄
    try:
        log_file = open("logs/"+time.strftime("%Y{0}%m{0}%d{0}%H{0}%M{0}%S".format('_'), time.localtime(time.time())) + '.log', 'w');
    except Exception as e:
        s = traceback.format_exc()
        print(s,file=log_file);
        log_file.flush();
        try:
            if log_file is not None:
                log_file.close(); 
        except Exception as e:
            s = traceback.format_exc()
            print(s,file=log_file);
            log_file.flush();
        exit(0);
         
    # 加载json配置文件，读取用户属性配置
    with open('config/property.json', 'r') as f:
        propertydata = json.load(f);
        if (len(propertydata['url'])==0) or (len(propertydata['email'])==0) or (len(propertydata['time'])==0):
            print("请在‘config/property.json’文件中配置相关信息\n",file=log_file);
            log_file.flush();
            try:
                if log_file is not None:
                    log_file.close();
            except Exception as e:
                s = traceback.format_exc()
                print(s,file=log_file);
                log_file.flush();
            exit(0);
            
    # 获取客户配置的url路径
    url = propertydata['url'];
    
    # 设置定时任务
    timestr = propertydata['time'];
    schedule.every().day.at(timestr).do(auto_web_glados_sign_in,url).tag('daily-tasks-sign-in-glados');

    # 启动定时任务
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
            #print("wait...\n",file=log_file);
            log_file.flush();
    except Exception as e:        
        s = traceback.format_exc()
        print(s,file=log_file);
        log_file.flush();
    finally:
        print("程序手动终止\n",file=log_file);
        schedule.clear('daily-tasks-sign-in-glados');
        log_file.flush();
        # 关闭终端文件流
        try:
            if log_file is not None:
                log_file.close();
        except Exception as e:            
            s = traceback.format_exc()
            print(s,file=log_file);
            log_file.flush();
            
if __name__ == "__main__":
    star_task();
    
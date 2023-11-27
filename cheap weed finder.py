#Purpose: To scrape data and find cheapest weed from the two closest dispos
#Version: 0.4
#Date of Update: 1/11/23

import os
import time
from time import sleep
from re import S
from tracemalloc import start
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#function to clear conle
def clearconsole():
    os.system("cls" if os.name == "nt" else 'clear')
    return

#function for MaryJ
def maryj():
    driver = webdriver.Chrome()
    url = "https://shop.maryjcannabis.ca/embed/stores/3217/menu?filters%5Broot_types%5D%5B%5D=flower"
    driver.get(url)
    wait = WebDriverWait(driver, 30) 

#press load more button to get full selection
    try:
#try to find load more button
        loadmore = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1yyfdow")))
        loadmore.click()
    except Exception as e:
#iff it cant fin the button it continues onward
        pass
    
    budsInfo = []
    
#wait for Collection of Type
    time.sleep(1)
    budsType = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1lekzkb"))) 
    budsType = [bud.text for bud in budsType]
    
#wait for Collection of Name
    budsName = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1q20gjz"))) 
    budsName = [bud.text for bud in budsName]  # extract text here
    
#wait for Collection of THC%
    budsTHC = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-eucfza")))  # Note: using find_elements (not through wait) to get all elements without waiting
    budsTHC = [bud.text for bud in budsTHC]
    
#put type, name and THC% into var then append var for every bud found
    for bud in range(len(budsName)):
     budInfo = [budsType[bud], budsName[bud], budsTHC[bud],]
     budsInfo.append(budInfo)
   
#find all buttons that reveal all weight options and then click every button found
    bclick = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1c1y81h")))
    for b in range(len(bclick)):
     bclick[b].click()
     
#wait for collection of weight and price
    budsCost = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1qo8ip7")))
    budsCost = [bud.text for bud in budsCost]
        

#remove $ and g then split weight and price
    for bud in range(len(budsCost)):
     budsCost[bud] = budsCost[bud].replace("$", "",)
     budsCost[bud] = budsCost[bud].replace("g", "",)
     budsCost[bud] = budsCost[bud].split("\n")
     temp_list = []
#find dollars per gram using every 2 indicies
     for element in range(0, len(budsCost[bud]), 2):
      weight = budsCost[bud][element]
      dpg = round((float(budsCost[bud][element + 1])/float(weight))*discount, 2)
      temp_list.append([dpg, weight])
#sort weight options by cheapest
     temp_list.sort(key = lambda x: x[0])
     budsInfo[bud].extend(temp_list)
     
    budsInfo.sort(key = lambda x: x[3][0])
    driver.close()
    return budsInfo

#function for Inspired Cannabis 
def inspired():
    driver = webdriver.Chrome()
    url = "https://www.iheartjane.com/embed/stores/4556/menu?filters%5Broot_types%5D%5B%5D=flower"
    driver.get(url)
    wait = WebDriverWait(driver, 30) 
    clearconsole()
    
#press load more button to get full selection
    try:
#try to find load more button
        loadmore = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1o17xan")))
        loadmore.click()
    except Exception as e:
#iff it cant fin the button it continues onward
        pass
    
    budsInfo = []
#wait for Collection of Type
    time.sleep(1)
    budsType = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1lekzkb"))) 
    budsType = [bud.text for bud in budsType]
    
#wait for Collection of Name
    budsName = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1q20gjz"))) 
    budsName = [bud.text for bud in budsName]  # extract text here
    
#put type, name and THC% into var then append var for every bud found
    for bud in range(len(budsName)):
     budInfo = [budsType[bud], budsName[bud]]
     budsInfo.append(budInfo)
   
#find all buttons that reveal all weight options and then click every button found
    bclick = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1gndn79")))
    for b in range(len(bclick)):
     bclick[b].click()
     
#wait for collection of weight and price
    budsCost = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1qo8ip7")))
    budsCost = [bud.text for bud in budsCost]
        

#remove $ and g then split weight and price
    for bud in range(len(budsCost)):
     budsCost[bud] = budsCost[bud].replace("$", "",)
     budsCost[bud] = budsCost[bud].replace("g", "",)
     budsCost[bud] = budsCost[bud].split("\n")
     temp_list = []
#find dollars per gram using every 2 indicies
     for element in range(0, len(budsCost[bud]), 2):
      weight = budsCost[bud][element]
      
#some silly little man messed up inputing info and put the string "each" where 7g should be for one of the strains
      try:
        weight = float(weight)
      except:
        weight = 7
   
      dpg = round((float(budsCost[bud][element + 1])/weight)*0.85, 2) 
      temp_list.append([dpg, weight])
      
#sort weight options by cheapest
     temp_list.sort(key = lambda x: x[0])
     budsInfo[bud].extend(temp_list)

#sort entire list by cheaptest dpg
    budsInfo.sort(key = lambda x: x[2][0])
    driver.close()
    return budsInfo
   
#calling both functions and saving their values
askdiscount = input("Do you have a discount for MaryJ? (y/n): ")
if askdiscount == "y" or "Y":
    inputdiscount = input(f"What is your discount? (eg. 10 is 10% off): ")

    try:
        inputdiscount = float(inputdiscount)
    except ValueError:
        print("Invalid input.")
        input("Press anything to continue...")
        exit()
clearconsole()

#save starting time
start_time = time.time()

discount = 1 - (inputdiscount/100)
MaryJ = maryj()
Inspired = inspired()

#clear console and print outcome
clearconsole()
print("Inspired Cannabis' Cheapest 5:")
for bud in range(5):
  print(Inspired[bud])

print()
print("MaryJ's Cheapest 5:")
for bud in range(5):
  print(MaryJ[bud])

print()
end_time = time.time()
time = end_time - start_time
print(f"Completed in {time: .2f} seconds.")
input("Press anything to continue...")
exit()
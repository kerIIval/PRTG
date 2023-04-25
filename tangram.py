from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import numpy as np
import os
import time 
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
# a lot of imports :P

def driver(res, automatic):
    options = ChromeOptions()

    if automatic: chromeHeight = chromeWidth = res

    else: 
        chromeHeight = res + 16
        chromeWidth = res + 88
    
    options.add_experimental_option("excludeSwitches", ['enable-automation']) # removes the warning about automation

    # depending on if the browser is started headless or not, its resolution is different. The if statement above calculates the relevent dimensions

    
    prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": rf"{path_to_download_folder}", # sets the download directory to add on directory
            "directory_upgrade": True,
            "prompt_for_download": False
            }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--window-size="+str(chromeHeight)+','+str(chromeWidth)) # sets the dimensions of chrome to allow for correct resolution heightmaps
    options.add_argument("disable-infobars")

    options.add_experimental_option("excludeSwitches", ['enable-automation']) # removes the warning about automation


    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

    # starts up chrome with the custom options
    return driver

def tangram(lat, long, scale, res, manual, interplvl = 0, exp = False, min = 0, max = 8848, ocean = False):
    link = "https://tangrams.github.io/heightmapper/#"+str(scale)+'/'+str(lat) +'/'+str(long)


    
    render = 1
    a = res
    if a > 100:
        while a > 900: 
            render += 1
            a = res / render
    render = str(render)
    # the purpose of this while loop is to reduce the size of the browser window, instead increase the render scale to get the desired resolution heightmap

    a = int(a)
    

    if manual:
        wd = driver(a, False)
    else:  
        wd = driver(a, True)

    # calls a function which starts up the webdriver


    wd.get(link)
    # opens tangram website
     
    render_setter(wd, render) # sets the render scale

    if not exp:
        customHeights(wd, max, min) # sets custom heights if wanted
    if ocean: 
        oceanData(wd) # enables ocean data if wanted
    if manual:
        manual_exec(wd, render, interplvl, res) # calls manual execution
    else:
        automatic_exec(wd, render, interplvl, res) # otherwise does it automatically
         
def render_setter(wd, render):
    el = WebDriverWait(wd, timeout=3).until(lambda d: d.find_element(By.XPATH,"/html/body/div[5]/div/ul/li[9]/div/div/div[1]/input")) # WebDriverWait is used to allow the website to load before scraping
    # the comments here are backup code
    el.clear()
    # el.send_keys('1')
    # el.send_keys(Keys.ENTER)

    # while el.get_attribute("value") == '1':
    #     time.sleep(1)
    # el.send_keys(Keys.BACK_SPACE)
    el.send_keys(render)
    el.send_keys(Keys.ENTER)

def customHeights(wd, max, min):
    # as the website has already loaded webdriverwait isn't needed anymore
    checkbox = wd.find_element(By.XPATH, "/html/body/div[5]/div/ul/li[4]/div/div/input")
    checkbox.send_keys(Keys.SPACE) # unchecks auto exposure allowing for custom max and min heights

    el = wd.find_element(By.XPATH,"//html//body//div[5]//div//ul//li[2]//div//div//div[1]//input")

    # erases the field so that the minimum wanted height can be inputted
    el.clear()

    el.send_keys(str(min))
    # set and confirm the minimum elevation
    el.send_keys(Keys.ENTER)

    # the following statements repeat the same instruction but for the max elevation
    el = wd.find_element(By.XPATH,"/html/body/div[5]/div/ul/li[1]/div/div/div[1]/input")

    el.clear()

    el.send_keys(str(max))

    el.send_keys(Keys.ENTER)

def oceanData(wd): # if the user has wanted ocean data as well, it will toggle it 
    checkbox = wd.find_element(By.XPATH, "/html/body/div[5]/div/ul/li[5]/div/div/input")
    checkbox.send_keys(Keys.SPACE)
        
def manual_exec(wd, render, interplvl, res): # if the user has chosen manual execution the map can be adjusted before rendering, it allows the user to move around in the website, more precisely choose their wanted region and then render

    el = wd.find_element(By.XPATH,"/html/body/div[5]/div/ul/li[9]/div/div/div[1]/input")
    for i in range(2):
        j = True
    # a for loop is used to wait and handle the alerts
    # it uses a range of 2 as the website will output 2 alerts 
    # the first iteration waits for the user to press render and to confirm the alert allowing the render to start
    # the second iteration waits for the second alert which confirms the render to be complete, the while loop is used again to wait for the user to accept it

        while j == True and i == 0: # halts the program until alert is handled           
            # the render scale is reentered here as the website will put the default value of 2. It depends on the speed of the website so this while loop is not alwayds neede
            if el.get_attribute('value') != render:
                el.clear()
                el.send_keys(render)
                el.send_keys(Keys.ENTER)
            time.sleep(1)

            if EC.alert_is_present()(wd): # once the alert is found we can exit the while loop
                j = False

        if i == 1:
            WebDriverWait(wd, timeout=2300).until(EC.alert_is_present()) # waits for the second alert
        
        j = True
        while j: # halts the program until alert is handled

            if not EC.alert_is_present()(wd):
                j = False           

        # the webscraping is complete, scalls the returnHeightmap function to get the downloaded image and shut down the driver
    returnHeightmap(interplvl, res, wd)

def automatic_exec(wd, render, interplvl, res):
    # if the user has chosen automatic execution the image is rendered automatically

    time.sleep(0.5) # this wait is there to ensure the render scale dooesn't get overriden by the website
    action = ActionChains(wd)
    el = wd.find_element(By.XPATH,"/html/body/div[5]/div/ul/li[9]/div/div/div[1]/input")
    el.clear()
    el.send_keys(render)
    el.send_keys(Keys.ENTER)

    el = wd.find_element(By.XPATH,"/html/body/div[5]/div/ul/li[11]/div/span")
    action.click(el).perform() # presses render

    WebDriverWait(wd, timeout=234).until(EC.alert_is_present())
    
    alert = wd.switch_to.alert
    alert.accept() # these 3 lines wait for the confirmation to come up and accept it

    WebDriverWait(wd, timeout=234).until(EC.alert_is_present())

    alert = wd.switch_to.alert
    alert.accept() # these 3 lines allow the code to know that the image has been rendered and downloaded, then it accepts that alert

    # the webscraping is complete, scalls the returnHeightmap function to get the downloaded image and shut down the driver
    returnHeightmap(interplvl, res, wd)
   
def returnHeightmap(interplvl, res, wd): # this function is used to return the downloaded heightmap to the generator or the interpolator depending on interplvl

    def latest_download_file(): # this function returns the latest modified file in the directory
        
        path = rf"{path_to_download_folder}"
        
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]

        return newest

    fileends = "crdownload"
    while "crdownload" == fileends: # this while loop halts the program until the image is fully downloaded (unfinished downloads have an extension of crdownload)
        time.sleep(1)
        newest_file = latest_download_file()
        if "crdownload" in newest_file:
            fileends = "crdownload"
        else:
            fileends = "none"
    wd.quit()

    # as the heightmap always is named render we can just add the name to the rest of the path string
    heightmap = path_to_download_folder + '\\' + "render.png"

    im = Image.open(str(heightmap)).convert('L') # saves the image as a variable

    os.remove(heightmap) # since the image is now saved as a variable the code removes the file, as it is no longer needed

    im = np.array(im)

    # the if statement calls the interpolate function if the heightmap needs to be interpolated, if not it ust calls the generator
    if interplvl > 0: 
        from .interpolation import interpolate
        interpolate(im, res, interplvl)

    else:
        from .generator import createGrid
        createGrid(res, im)
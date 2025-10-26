from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
from dotenv import dotenv_values
import mtranslate as mt

env_vars = dotenv_values(".env")
Inputlanguage = env_vars.get("Inputlanguage")

Htmlcode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

Htmlcode = str(Htmlcode).replace("recognition.lang = '';",f"recognition.lang = '{Inputlanguage}' ;")

with open(r"Data\voice.html", "w") as f:
    f.write(Htmlcode)   

current_dir = os.getcwd()    
link = os.path.join(current_dir, "Data", "voice.html").replace("\\", "/")

chrome_options = Options()
use_agent = "mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={use_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-str")
chrome_options.add_argument("--headless=new")

Service = Service(ChromeDriverManager().install())
driver =webdriver.Chrome(service=Service, options= chrome_options)

    
tempditpath = (rf"{current_dir}\frontend\files")

def setAssistantStatus(Status):
    with open(rf"{tempditpath}\Status.data", "w",encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query =Query.lower().strip()
    query_words = new_query.split()
    question_words =  ["how","what","who","where","when","why","which","whose","whom","can you","what's","how's","can'you"]

    if any (word  + " " in new_query for word in question_words):
         if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
         else:
             new_query +="?"
    else:

        if query_words[-1][-1] in ['.','?','!']:   
                new_query = new_query[:-1] + " "
        else:
             new_query +=" "
    return new_query.capitalize()

def Universaltran(Text):
     english_trans = mt.translate(Text,"hi","auto")   
     return english_trans.capitalize() 

def SpeechRecognition():
     driver.get("file:///" + link)
     driver.find_element(by=By.ID,value="start").click()
      
     while True:
         try:
             Text = driver.find_element(by=By.ID,value="output").text

             if Text:
                 driver.find_element(by=By.ID,value="end").click() 

                 if Inputlanguage.lower() =="en" or "en" in Inputlanguage.lower():

                  return QueryModifier(Text)
             else :

                  setAssistantStatus("Translating.....")
                  return QueryModifier(Universaltran(Text))
         except Exception as e :
            pass


        
if __name__=="__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)  



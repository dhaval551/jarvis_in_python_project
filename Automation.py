from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKEY = env_vars.get("GroqAPIKEY")

classs = ["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvwSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta","IZ6rdc","05uR6d LTKOO","vlzY6d","webanswers-webanswers_table_webanswers-table","dDoNo ikb4Bb gsrt","sXLaOe","LWkfke","VQF4g","qv3Wpe","kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'


client = Groq(api_key=GroqAPIKEY)



professional_response = [

    "your satisfaction is my top priority ; feel free to reach out if ther's anything else i can help you with",
    "i'am at your service for any additional questions or support you may need-don't hesitate to ask",
] 

messages = []
SystemChatBot = [{"role": "system", "content": f"hello, i am {os.environ['username']}, you're a content writer. you have to write content like letter"}]

def GoogleSearch(Topic):
    search(Topic)
    return True




def Content(Topic): 
    
    

    def OpenNotepad(File):
        defult_text_editor = "notepad.exe"
        subprocess.Popen([defult_text_editor, File])

    def ContentWriter(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) 

        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages= SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream= True,
            stop= None
        )
        Answer = ""

        for chunk in completion:
           if chunk.choices[0].delta.content: 
            Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic : str = Topic.replace("Content ", "")
    ContentByAI = ContentWriter(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True


def YouTube(Topic):
   Url4search = f"https://www.youtube.com/results?search_query={Topic}"
   webbrowser.open(Url4search)
   return True

def PlayYouTube(query):
    playonyt(query)
    return True

def OpenApp(app,sess = requests.Session()):
   
   try:
      appopen(app,match_closest=True,output = True , throw_error = True)
      return True

   except:
      def extract_link(html): 
         if html is None:
             return []
         soup = BeautifulSoup(html, "html.parser")
         links = soup.find_all('a', {'jsname': 'UWckNb'})
         return [link.get('href') for link in links]
      
      def search_google(query):
          url = f"https://www.google.com/search?q={query}"
          headers = {'User-Agent': useragent}
          response = sess.get(url, headers=headers)

          if response.status_code == 200:
              return response.text
          else:
              print("field to fetch google search results")
              return None
          
      html = search_google(app)

      if html:
            link = extract_link(html)[0]
            webopen(link)
      return True

def CloseApp(app):
    try:
        # Agar "chrome" ya "close chrome" command hai, toh "chrome" close karo
        if "chrome" in app.lower():
            close("chrome", match_closest=True, output=True, throw_error=True)
        else:
            close(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error closing {app}: {e}")
        return False
       
def System(command):

    def  mute():
        keyboard.press_and_release("volume mute")
    
    def unmute():
        keyboard.press_and_release("volume mute")
  
    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
        return True
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()   
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands: list[str]):

    funcs=[]
    for command in  commands:
         command = command.strip().rstrip(".") 
         if command.startswith("open "):
              
              if"open it" in command:
                  pass
              if "open file" == command:
                  pass
              else:
                  fun = asyncio.to_thread(OpenApp,command.removeprefix("open "))
                  funcs.append(fun)
       
         elif command.startswith("general "):
             pass
         elif command.startswith("realtime "):
             pass
         elif command.startswith("close "):
             fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
             funcs.append(fun)

         elif command.startswith("play "):
             fun = asyncio.to_thread(PlayYouTube,command.removeprefix("play "))
             funcs.append(fun)  
         
         elif command.startswith("content "):
             fun = asyncio.to_thread(Content, command.removeprefix("content "))
             funcs.append(fun)

         elif command.startswith("google search "):
            fun = asyncio.to_thread( GoogleSearch, command.removeprefix("google search ") )
            funcs.append(fun)

         elif command.startswith("youtube search "):
              fun = asyncio.to_thread(YouTube,command.removeprefix("youtube search ") )
              funcs.append(fun)

         elif command.startswith("system ")  :
             fun = asyncio.to_thread(System,command.removeprefix("system "))              
             funcs.append(fun)
         else :
             print(f"no Function found. for {command}")

    results  = await asyncio.gather(*funcs)     
    for result in results :
         if isinstance(result,str) :
             yield result
         else:
             yield result

async def Automationn(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass
   
    return True


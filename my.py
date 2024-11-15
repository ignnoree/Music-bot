import telegram
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup
import requests
import time
from apis import chat_id,token_







async def main():
    while True:
        music_path= r'E:\1file\mp3s\\'
        dawnloaded_links_file='dawnloadedlinks.txt'

        with open(dawnloaded_links_file, 'r') as file:
            downloaded_links = set(line.strip() for line in file)
    
        
        
        bot=telegram.Bot(token=token_)
        page_to_scrape = requests.get('https://mrtehran.app/')
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
        tracks = soup.findAll('div', attrs={'class': "track-box"})
        newesttrack = tracks[0]
        

        
        artistname=newesttrack.find('div',attrs={'class':'text2'})
    
        musicname=newesttrack.find('div',attrs={'class':'text1'})
   
        url = newesttrack.find('a', href=True)['href']

        songurl=f'https://mrtehran.app{url}'


        trackscrape=requests.get(songurl,verify=False)
        secsoup=BeautifulSoup(trackscrape.text,'html.parser')
        infoget=secsoup.find('div',attrs={'class':'detailes m-top-1'})
        caption=infoget.text
        trackpage=secsoup.findAll('script')
        mp3_url_string = str(trackpage)

        start_index = mp3_url_string.find("mp3s/")

        end_index = mp3_url_string.find(".mp3", start_index) + len(".mp3")


        mp3_part = mp3_url_string[start_index:end_index]

        ii=mp3_part.split(',')[2]

        cleaned_output = ii.replace("mp3s/01/", "").replace(".mp3", "").replace(".jpg", "").replace('\\"','').replace('track_audio:','')

        finallink=f'https://cdnmrtehran.ir/media/mp3s/01/{cleaned_output}.mp3'
        if finallink not in downloaded_links:

            doc = requests.get(finallink,verify=True)
            with open(f'{music_path}{musicname.text}.mp3', 'wb') as f:
                    f.write(doc.content)
                    print(f'{musicname.text} from {artistname.text} dawnloaded !' )

            with open(f'{music_path}{musicname.text}.mp3', 'rb') as sendf:
                await bot.send_audio(chat_id=chat_id, audio=sendf, caption=caption)
                print('music sended!')

            with open (dawnloaded_links_file,'a')as file:
                 file.write(f'{finallink}\n')
                 print('dawnloaded_links_file updated')

                 
        else:
            print('music already dawnloaded!')
        print('cheking in 10 min')
        await asyncio.sleep(600)  

        
asyncio.run(main())
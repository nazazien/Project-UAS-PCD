from keperluan_modul import *

def menyapa_user():    
    pesan = st.toast('Knock.. Knock..')
    time.sleep(2)
    pesan.toast('🚪 Open the door...')
    time.sleep(2)
    pesan.toast('😄 WELCOME TO Gemilang`S WEB APP! 😄', icon = "🎉")

def ucapan():
    st.balloons()
    pesan = st.toast('Hello! How Are You?', icon = '😊')    
    time.sleep(1)
    pesan.toast('Gwenchana-yo?', icon = "🤕")    
    time.sleep(1)
    pesan.toast('Have a nice day', icon='😇')    
    time.sleep(1)
    pesan.toast('😄 ENJOY WITH OUR APP! 😄', icon = "🎉")

def sukses():    
    st.balloons()
    pesan = st.toast('BIG THANKS!', icon='🥰') 
    time.sleep(1)
    pesan.toast('Thank you for using our App', icon='🤗')    

def profil():
    st.snow()
    time.sleep(2)
    pesan = st.toast('Hallo!', icon='🤗')    
    time.sleep(1)
    pesan.toast('We are behind the scene of', icon='😇')
    time.sleep(1)
    pesan.toast('😄 Gemilang! 😄', icon = "🎉")


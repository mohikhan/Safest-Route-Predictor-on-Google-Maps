import speech_recognition as speech

from tkinter import *
import time
from selenium import  webdriver
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from selenium.webdriver.common.keys import Keys



a = Tk()
a.title('SAFEST ROUTE PREDICTOR')
a.geometry('1440x900+300+100')
a.configure(background='powder blue')

""" --- Using Google Speech to Text to take input from the user through microphone ---"""

def voice1():
    b = speech.Recognizer()
    with speech.Microphone() as source:
        audio = b.listen(source)
    try:
        text = b.recognize_google(audio)
        name1.set(text)
    except:
        print('error')
def voice2():
    b = speech.Recognizer()
    with speech.Microphone() as source:
        audio = b.listen(source)
    try:
        text = b.recognize_google(audio)
        name2.set(text)
    except:
        print('error')

background_image = PhotoImage(file='images/big_map.gif')
background_label = Label(a,image=background_image)
background_label.place(x=0,y=0,relwidth=1,relheight=1)
label0 = Label(text='SAFEST ROUTE PREDICTOR',width=30,font=("bold",34),background='white')
label0.place(x=400,y=25)
label1 = Label(text='SOURCE',font=35)
label1.place(x=480,y=150)
name1 = StringVar()
text1 = Entry(textvariable=name1,width=25,font=20)
text1.place(x=650,y=150)
label2 = Label(text='DESTINATION',font=35)
label2.place(x=480,y=205)
name2 = StringVar()
text2 = Entry(textvariable=name2,width=25,font=20)
text2.place(x=650,y=205)

def conf(event):
    src = str(name1.get())
    dest = str(name2.get())
    
    # selenium webdriver path in your system...
    driver = webdriver.Chrome('')

    driver.get('https://www.google.com/maps/dir///@27.9107022,78.0760799,15z/data=!4m2!4m1!3e0')

    driver.set_window_size(1024,600)
    driver.maximize_window()

    time.sleep(5)


    dataset1 = pd.read_csv('crime.csv')
    X = dataset1.drop('Crime value', axis=1)
    y = dataset1['Crime value']

    #from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)

    driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input').send_keys(src)
    driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(dest)
    driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(Keys.RETURN)

    time.sleep(5)

    road_xpath = '//h1[@class="section-directions-trip-title"]/span'

    roads = driver.find_elements_by_xpath(road_xpath)

    list_of_via_roads_final1 = [None,]
    list_of_via_roads_final2 = []

    for road in roads:
        road_name = road.text
        # print(road_name)
        list_of_via_roads_final2.append(road_name)
        check_for_and = "and" in road_name
        check_for_slash = "/" in road_name



        if check_for_and == True:

            road_name_final1 = road_name.split('and')[0].strip()
            road_name_final2 = road_name.split('and')[1].strip()
            # list_of_via_roads_final1.append(road_name_final1)
            for items in range(len(list_of_via_roads_final1)):
                if list_of_via_roads_final1[items] == road_name_final1:
                    # road_name_final2 = road_name.split('and')[1].strip()
                    # list_of_via_roads_final1.insert(items,road_name_final1)
                    list_of_via_roads_final1.append(road_name_final2)
                    # print("If block of and")
                else:
                    list_of_via_roads_final1.append(road_name_final1)
                    # print("Else block of and")


            # road_name_final1 = road_name.split('and')[0].strip()
            # list_of_via_roads_final1.append(road_name_final1)

        elif check_for_slash == True:

            road_name_final1 = road_name.split('/')[0].strip()
            list_of_via_roads_final1.append(road_name_final1)

        else:
            road_name_final1 = road_name
            list_of_via_roads_final1.append(road_name_final1)

    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    # Remove duplicates from this list.
    values = list_of_via_roads_final1
    result = remove_duplicates(values)

    list_of_via_roads_final1 = result

    # print(list_of_via_roads_final1)

    clean = [x for x in list_of_via_roads_final1 if x != None]

    # print(clean)

    b = 0
    c = 0
    A = [None] * 5
    for i in range(len(clean)):
        # name_of_road = list_of_via_roads_final1[i]
        csv_file = csv.reader(open('roads.csv', 'r', encoding='utf-8'))
        # print(name_of_road)

        for row in csv_file:
            if clean[i] == row[0]:
                # print(row)
                row.pop(0)
                # print(row)
                # print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                A[i] = regressor.predict([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]])

                # print(A[i])
                b = b + 1

    m = A[0]
    # print(A)
    for i in range(b):
       if int(m)> int(A[i]):
           m = A[i]
           c = i

    # print(m)
    # print(c)


    time.sleep(1)
    clicking_path = f'//*[@id="section-directions-trip-{c}"]/div[2]'
    driver.find_element_by_xpath(clicking_path).click()
    try:
        driver.find_element_by_xpath(clicking_path).click()
    except:
        pass

    print("Safest route will be via " + list_of_via_roads_final2[c])
    final_result = "Safest route will be via " + list_of_via_roads_final2[c]


    time.sleep(5)

    url_current = driver.current_url
    print(url_current)


    label3 = Label(text = final_result,font= 50)
    label3.place(x=400,y=380)

    from twilio.rest import Client

    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        # body="Safest route between " + src + " and " + dest + " will be via " + list_of_via_roads_final2[c],
        body=url_current,
        
        # your twilio number
        from_='whatsapp:',
        
        # user's whatsapp number..
        to='whatsapp:'
    )

    print(message.sid)


a.bind('<Return>',conf)




## Button for getting route (not configured as of now)
button1 = Button(a,text='GET ROUTE',fg='black',width=15,font=15,background='white')
button1.bind('<Button-1>',conf)
button1.place(x=650,y=280)
img = PhotoImage(file='images/voice_btn.gif')


## Button for taking source input
button2 = Button(a,text='voice',fg='black',width=40,height=30,font=5,background='black',command=voice1,image=img)
button2.place(x=920,y=145)

## Button for taking destination input
button3 = Button(a,text='voice',fg='black',width=40,height=30,font=5,background='black',command=voice2,image=img)
button3.place(x=920,y=200)



a.mainloop()

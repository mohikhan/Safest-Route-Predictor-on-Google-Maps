
# Download the helper library from https://www.twilio.com/docs/python/install
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from twilio.rest import Client
from tkinter import *
import time
from selenium import webdriver
import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from selenium.webdriver.common.keys import Keys
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""

    body = request.values.get('Body', None)

    # Start our response
    resp = MessagingResponse()



    test = body

    source = test.split('and')[0]
    des = test.split('and')[1].strip()

    print("Source is : ", source)
    print("Destination is : ", des)

    print(source)
    print(des)

    if body == 'Start' or body == 'START' or body == 'start':
        resp.message("Enter Source and Destination ")


    elif body == 'bye':
        resp.message("Goodbye")

    # return str(resp)




    from selenium import webdriver
    
    # selenium webdriver path in your system
    driver = webdriver.Chrome('')
    
    driver.get('https://www.google.com/maps/dir///@27.9107022,78.0760799,15z/data=!4m2!4m1!3e0')

    time.sleep(5)


    dataset1 = pd.read_csv('crime.csv')
    X = dataset1.drop('Crime value', axis=1)
    y = dataset1['Crime value']

        # from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)

        # driver.find_element_by_id('sb_ifc51').send_keys('Aligarh')
    driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input').send_keys(source)
    driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(des)
    driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(Keys.RETURN)
        # driver.fifind_element_by_class_name('tactile-searchbox-input').send_keys('Aligarh')
        # driver.find_element_by_class_name('tactile-searchbox-input').send_keys('Aligarh')

        # //*[@id="sb_ifc51"]/input
    time.sleep(4)
        # via_road = driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div[2]/div[1]/div[2]/h1[1]/span')
        # via_road2 = driver.find_element_by_xpath('//*[@id="section-directions-trip-1"]/div[2]/div[1]/div[2]/h1[1]/span')
        # via_road3 = driver.find_element_by_xpath('//*[@id="section-directions-trip-2"]/div[2]/div[1]/div[2]/h1[1]/span')

    road_xpath = '//h1[@class="section-directions-trip-title"]/span'

    roads = driver.find_elements_by_xpath(road_xpath)

    list_of_via_roads_final1 = [None, ]
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
        if int(m) > int(A[i]):
            m = A[i]
            c = i

        # print(m)
    print(c)

    time.sleep(1)
    clicking_path = f'//*[@id="section-directions-trip-{c}"]/div[2]'
    driver.find_element_by_xpath(clicking_path).click()
    try:
        driver.find_element_by_xpath(clicking_path).click()
    except:
        pass

    print("Safest route will be via " + list_of_via_roads_final2[c])

    time.sleep(3)

    url_current = driver.current_url
    # print(url_current)

    # your twilio auth_token and account_sid...
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Safest route between " +source + " and " +des + " will be via " +list_of_via_roads_final2[c] + "\n" +"The url is: " + url_current,
        
        # your twilio number...
        from_='whatsapp:',
        
        # user's whatsapp number...
        to='whatsapp:'
    )

    # return list_of_via_roads_final2[c]


    # Add a message
    # resp.message("Ahoy! Thanks so much for your message.")
    resp.message("Ahoy")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

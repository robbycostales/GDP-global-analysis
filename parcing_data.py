import xlrd
import os
import requests

file = "GDP_data.xls"

sheet = xlrd.open_workbook(file)
sheet0 = sheet.sheet_by_index(0)
country_names = sheet0.col_values(colx=0)
country_names = country_names[1:]
sheet_length = len(country_names)
sheet_width = len(sheet0.row_values(rowx=0))
dates = (sheet0.row_values(rowx=0))

# print(sheet_width)
# print(dates)
# dates = dates[2:]
# print(sheet_length)

# This generates an nxm array
def make_matrix(n,m,array_names,dates,sheet):
    data = []
    for i in range(n):
        temp = [array_names[i]]
        for j in range(m):
            gdp = sheet.cell(i+1,j+2)
            gdp = str(gdp)
            gdp = gdp.split(":")
            gdp = gdp[1:]
            gdp = ("").join(gdp)
            if(len(gdp)>2):
                gdp = float(gdp)
            else:
                gdp = 0
            temp.append(((dates[j+2]),gdp))
        data.append(temp)
    return data


data = make_matrix(sheet_length,sheet_width-2,country_names,dates,sheet0)

# for i in range(sheet_length):
#     print("\n")
#     for j in range(sheet_width -2):
#         print(data[i][j],end=" , ")


def out_put_text(lst):
    default = ": { fillKey: \"authorHasTravledTo},"
    for i in lst:
        str = ""
        str+= i+default
        myfile.write(str)
        myfile.write("\n")
# myfile.write(str(dates[2:]))
# out_put_text(country_names)



# gets longitude and latitude for countries from web
url = "http://www.newstrackindia.com/information/worldinfo/Latitude-and-Longitude-of-Countries.html"
resp = requests.get(url)
html_text = resp.content
html = str(html_text)

lats_and_longs = []
def long_lad_scraper(str):
    for i in country_names:
        print(i)
        if(i == "United States"):
            lat = 38.0
            long = -97.0
            lats_and_longs.append((float(lat),float(long)))
            print(lat)
            print(long)
            continue

        index = str.find(i+"<")
        lat = ""
        long = ""

        if(index == -1):
            lat = "e"
            long = "e"
            # print(lat)
            # print(long)
            lats_and_longs.append((lat,long))
            continue
        index += (len(i)+15)

        while str[index] != "<":
            lat += str[index]
            index += 1

        index += 15

        while str[index] != "<":
            long += str[index]
            index += 1

        if("null" not in lat and "null" not in long):

            float(lat)
            float(long)
            # print(lat)
            # print(long)
            lats_and_longs.append((lat,long))
        else:
            lat = "e"
            long = "e"
            lats_and_longs.append((lat,long))
            continue
long_lad_scraper(html)


# FINDS MAXIMUM VALUE FOR GDP
def max_gdp():
    max = 0
    for i in range(sheet_width-2):
        for j in range(sheet_length):
            (date,gdp) = data[j][i+1]
            if gdp > max:
                max = gdp
    return max


# WRITES JSON FILE FOR RAW DATA

def raw_json():
    destination = "./raw.json"
    myfile = open(destination, "w")
    myfile.write("[")
    for i in range(sheet_width-2):
        myfile.write("[")
        myfile.write('"'+str(dates[i+2])+'"'+","+"[")

        for j in range(sheet_length):
            print(j)
            (lat, long) = lats_and_longs[j]
            if(lat and long == "e"):
                continue
            (date,gdp) = data[j][i+1]

            myfile.write(str(lat))
            myfile.write(",")
            myfile.write(str(long))
            myfile.write(",")
            myfile.write(str(gdp))
            if(j < sheet_length-2):
                myfile.write(",")
        myfile.write("]")
        if(i < sheet_width -3):
            myfile.write("],")
        else:
             myfile.write("]]")
raw_json()


# WRITES JSON FILE FOR SCALED DATA

def scaled_json():
    destination = "./scaled.json"
    myfile = open(destination,"w")
    myfile.write("[")
    max = max_gdp()
    for i in range(sheet_width-2):
        myfile.write("[")
        myfile.write('"'+str(dates[i+2])+'"'+","+"[")

        for j in range(sheet_length):
            (lat, long) = lats_and_longs[j]
            if(lat and long == "e"):
                continue
            (date,gdp) = data[j][i+1]

            myfile.write(str(lat))
            myfile.write(",")
            myfile.write(str(long))
            myfile.write(",")
            myfile.write(str(float(20*(gdp/max))))
            if(j < sheet_length-2):
                myfile.write(",")
        myfile.write("]")
        if(i < sheet_width -3):
            myfile.write("],")
        else:
             myfile.write("]]")

scaled_json()


# WRITES JSON FILE FOR SCALED DATA

def diff_json():
    destination = "./diff.json"
    myfile = open(destination,"w")
    myfile.write("[")
    max = max_gdp()
    for i in range(sheet_width-2):
        # brackets and country
        myfile.write("[")
        myfile.write('"'+str(dates[i+2])+'"'+","+"[")

        for j in range(sheet_length):
            (lat, long) = lats_and_longs[j]
            if(lat and long == "e"):
                continue
            (date,gdp) = data[j][i+1]

            if i==0:
                diff_gdp = 0
            else:
                # = current - past
                # increase is positive
                # decrease is negative
                (past_date,past_gdp) = data[j-1][i+1]
                diff_gdp = gdp/max - past_gdp/max

            # writes longitude and latitude
            myfile.write(str(lat))
            myfile.write(",")
            myfile.write(str(long))
            myfile.write(",")

            # writes value
            myfile.write(str(float(20*(diff_gdp))))
            if(j < sheet_length-2):
                myfile.write(",")
        myfile.write("]")
        if(i < sheet_width -3):
            myfile.write("],")
        else:
             myfile.write("]]")

diff_json()

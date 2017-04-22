import xlrd
import os
import requests

file = "GDP_data.xls"
destination = "gdp.json"

myfile = open(destination, "w")



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

def make_matrix(n,m,array_names,dates,sheet): # This generates an nxm array
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

for i in range(sheet_length):
    print("\n")
    for j in range(sheet_width -2):
        print(data[i][j],end=" , ")


def out_put_text(lst):
    default = ": { fillKey: \"authorHasTravledTo},"

    for i in lst:
        str = ""
        str+= i+default
        print(str)

        myfile.write(str)
        myfile.write("\n")


# myfile.write(str(dates[2:]))
# out_put_text(country_names)





url = "http://www.newstrackindia.com/information/worldinfo/Latitude-and-Longitude-of-Countries.html"

resp = requests.get(url)
html_text = resp.content
html = str(html_text)

lats_and_longs = []


def long_lad_scraper(str):
    for i in country_names:

        index = str.find(i+"<")
        # print(i)
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
        if(lat and long != "null"):

            float(lat)
            float(long)
        else:
            long = "e"
            lat = "e"
        # print(lat)
        # print(long)
        lats_and_longs.append((lat,long))

long_lad_scraper(html)

# print(lats_and_longs)
# print(country_names)

myfile.write("[")

def max_gdp():
    max = 0
    for i in range(sheet_width-2):
        for j in range(sheet_length):
            (date,gdp) = data[j][i+1]
            if gdp > max:
                max = gdp
    return max


def raw_json():
    for i in range(sheet_width-2):
        myfile.write("[")
        myfile.write('"'+str(dates[i+2])+'"'+","+"[")

        for j in range(sheet_length):
            # if len(data[j][i+1]) != 2:
            #      print(len(data[j][i+1]), data[j][i+1])
            (lat, long) = lats_and_longs[j]
            if(lat and long == "e"):
                continue
            (date,gdp) = data[j][i+1]

            myfile.write(lat)
            myfile.write(",")
            myfile.write(long)
            myfile.write(",")
            myfile.write(str(gdp))
            if(j < sheet_length-2):
                myfile.write(",")

        myfile.write("]")
        if(i < sheet_width -3):
            myfile.write("],")
        else:
             myfile.write("]]")

destination = "gdp_scaled.json"

myfile = open(destination,"w")

def scaled_json():
    max = max_gdp()
    for i in range(sheet_width-2):
        myfile.write("[")
        myfile.write('"'+str(dates[i+2])+'"'+","+"[")

        for j in range(sheet_length):
            # if len(data[j][i+1]) != 2:
            #      print(len(data[j][i+1]), data[j][i+1])
            (lat, long) = lats_and_longs[j]
            if(lat and long == "e"):
                continue
            (date,gdp) = data[j][i+1]

            myfile.write(lat)
            myfile.write(",")
            myfile.write(long)
            myfile.write(",")
            myfile.write(str(gdp//max))
            if(j < sheet_length-2):
                myfile.write(",")

        myfile.write("]")
        if(i < sheet_width -3):
            myfile.write("],")
        else:
             myfile.write("]]")



scaled_json()





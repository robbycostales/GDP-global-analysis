import xlrd
file = "GDP_data.xls"


sheet = xlrd.open_workbook(file)

sheet0 = sheet.sheet_by_index(0)
country_names = sheet0.col_values(colx=1)
country_names = country_names[1:]

sheet_length = len(country_names)

sheet_width = len(sheet0.row_values(rowx=0))

dates = (sheet0.row_values(rowx=0))

print(sheet_width)

print(dates)

# dates = dates[2:]
print(sheet_length)

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








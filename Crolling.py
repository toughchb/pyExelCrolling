import openpyxl

fr = open( "TableList.txt",'r', encoding='UTF8')
fw = open("Create.sql",'w', encoding='UTF8')
tableList = []
while True:
    r_line = fr.readline()
    if not r_line: break
    r_line.strip()
    tableList.append(r_line)
fr.close()
for tableName in tableList:
    print(tableName)
print(len(tableList))
# 엑셀파일 열기

excel_file = openpyxl.load_workbook('Input.xlsx')

excel_sheet = excel_file.get_sheet_by_name('Sheet1')

for row in excel_sheet.rows:
    if str(row[0].value) == str(tableList[0]):
        outline = row[1].value + row[2].value
        print(type(outline))
        fw.write(outline)


    #print(row[0].row)
    #print(row[1].value)
    #print(row[2].value)

    #excel_sheet.cell(row=row[0].row, column=3).value = 10

# 엑셀 파일 저장
#excel_file.save("03_data/sample2.xlsx")
fw.close()
excel_file.close()
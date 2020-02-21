import openpyxl

fr = open( "TableList.txt",'r', encoding='UTF8')
fw = open("Create1.sql",'w', encoding='UTF8')
tableList = []
while True:
    r_line = fr.readline()
    if not r_line: break
    r_line.strip()
    tableList.append(r_line)
fr.close()

print(len(tableList))

# 엑셀파일 열기
excel_file = openpyxl.load_workbook('Input.xlsx')

#excel_sheet1 = excel_file.get_sheet_by_name('Sheet1')
excel_sheet1 = excel_file['Sheet1']

#excel_sheet2 = excel_file.get_sheet_by_name('Sheet2')
excel_sheet2 = excel_file['Sheet2']

PrimaryKeys = []
pKey = ''
try:
    for i in range(0, len(tableList)):
        if len(PrimaryKeys) != 0:
            PrimaryKeys = []
            pKey = ''
        for row2 in excel_sheet2.rows:
            if str(row2[0].value) == tableList[i]:
                PrimaryKeys.append(row2[1].value)
                pKey = ",".join(PrimaryKeys)
                print ('pKey = ' + pKey)
            for row in excel_sheet1.rows:
                if str(row[0].value) == tableList[i]:
                    outline = row[1].value + row[2].value + '\n'
                    if outline.find('CREATE') != -1: #첫째 줄
                        loc = outline.find('CREATE')
                        outline = outline[loc:]
                    if outline.find(');') != -1: #마지막 줄
                        if outline.find('ETL_DEL_YN CHAR(1),') != -1:
                            outline = outline.replace('ETL_DEL_YN CHAR(1),', 'ETL_DEL_YN CHAR(1) DEFAULT ‘N’ NOT NULL, ')
                        if outline.find('ETL_LOAD_DT DATETIME') != -1:
                            outline = outline.replace('ETL_LOAD_DT DATETIME);', 'ETL_LOAD_DT DATETIME DEFAULT CURRENT TIMESTAMP NOT NULL, ')
                            outline = outline + "PRIMARY KEY(" + pKey + ',ETL_DEL_YN,ETL_LOAD_DT);\n);'
                        outline = outline.replace(', ', ",\n") # 컴마뒤에 개행 추가
                    print(outline)
                    fw.write(outline)
except Exception as ex:
    print("ERROR RAISE: ", ex)


fw.close()
excel_file.close()
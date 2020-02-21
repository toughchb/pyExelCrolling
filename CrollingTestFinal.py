import openpyxl


def main():

    table_list = []
    with open("TargetTables.txt", 'r', encoding='UTF8') as fr:#, open("Create.sql", 'w', encoding='UTF8') as fw:
        for r_line in fr:
            table_list.append(r_line.strip())
    print(len(table_list))
    print(table_list)

    # 엑셀파일 열기
    excel_file = openpyxl.load_workbook('Input.xlsx')

    excel_sheet1 = excel_file['Sheet1']

    excel_sheet2 = excel_file['Sheet2']

    primary_keys = {}
    no_primary_keys = []
    fw = open("Create.sql", 'w', encoding='UTF8')

    for line in excel_sheet2.rows:
        t_key = line[0].value
        if t_key in table_list:
            primary_keys[t_key] = primary_keys.get(t_key, []) + [line[1].value]

    for line2 in excel_sheet1.rows:
        t_key = line2[0].value
        if t_key in table_list:
            pKey = ''
            outline = line2[1].value + line2[2].value + '\n'

            if 'CREATE' in outline:  # 첫째 줄
                loc = outline.find('CREATE')
                outline = outline[loc:]
                outline = outline.replace('(','(\n',1)

            if ');' in outline:  # 마지막 줄
                if outline.find('ETL_DEL_YN CHAR(1),') != -1:
                    outline = outline.replace('ETL_DEL_YN CHAR(1),', 'ETL_DEL_YN CHAR(1) DEFAULT ‘N’ NOT NULL, ')
                if outline.find('ETL_LOAD_DT DATETIME') != -1:
                    outline = (outline.replace('ETL_LOAD_DT DATETIME);',
                                               'ETL_LOAD_DT DATETIME DEFAULT CURRENT TIMESTAMP NOT NULL, ')).lstrip()
                    if t_key in primary_keys:
                        pKey = ','.join(primary_keys[t_key])
                    else:
                        no_primary_keys.append(t_key)
                    if len(pKey) != 0:
                        outline = outline + 'PRIMARY KEY(' + pKey + ',ETL_DEL_YN,ETL_LOAD_DT);\n);'
                    else:
                        outline = outline + 'PRIMARY KEY(ETL_DEL_YN,ETL_LOAD_DT);\n);'
                outline = outline.replace(', ', ",\n") # 컴마뒤에 개행 추가
                outline = outline + '\n'
            #print(outline)
            fw.write(outline)

    fw.close()


    excel_file.close()
    print(primary_keys)
    print(len(primary_keys))
    print('no PK tables :')
    print(no_primary_keys)


if __name__ == "__main__":
    main()



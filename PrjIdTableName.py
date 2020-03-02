import openpyxl

def main():
    # 엑셀파일 열기
    excel_file = openpyxl.load_workbook('prjInput.xlsx')

    excel_sheet1 = excel_file['Sheet1']

    excel_sheet2 = excel_file['Sheet2']
    fw = open("result.txt", 'w', encoding='UTF8')
    prj_id_list = {}
    for line in excel_sheet1:
        t_key = line[1].value
        prj_id_list[t_key] = [line[0].value]

    print('prj_id_list: {}'.format(prj_id_list))
    print('prj_id_list lenth: {}'.format(len(prj_id_list)))

    table_name = []
    for line2 in excel_sheet2:
        t_key = line2[0].value
        table_name.append(t_key)

    print('table_name: {}'.format(table_name))
    print('table_name lenth: {}'.format(len(table_name)))

    for s_name in table_name:
        if s_name in prj_id_list:
            #print('{} : {}'.format(s_name,prj_id_list[s_name]))
            outline = s_name + ' ' + str(prj_id_list[s_name][0]) + '\n'

            fw.write(outline)
        else:
            outline = s_name + ' ' + 'empty' + '\n'
            fw.write(outline)

    fw.close()
if __name__ == "__main__":
    main()

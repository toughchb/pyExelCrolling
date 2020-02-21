import pandas as pd

fr = open( "TableList.txt",'r', encoding='UTF8')
fw = open("Create2.sql",'w', encoding='UTF8')
tableList = []
while True:
    r_line = fr.readline()
    if not r_line: break
    r_line.strip()
    tableList.append(r_line)
fr.close()
df1 = pd.read_excel('Input2.xlsx',sheet_name='Sheet1')
df2 = pd.read_excel('Input2.xlsx',sheet_name='Sheet2')

print(df1)
print(df2)
print('-----------')
#df1[df1.tablename == tableList[0]].iloc[:, 1]

df1['result'] = df1[df1.tablename == tableList[0]]['create1'] + df1[df1.tablename == tableList[0]]['create2']
print(df1)
df1['result'].to_csv('Create2.sql', index=False, header=False)
'''
print(df1[df1.tablename == tableList[0]].iloc[:, 1:])
outline.to_csv('Create2.sql', index=False)
# while True:
#     if df1['tablename']. == tableList[0]:
'''


#print(df1['tablename'])

fw.close()
def OrderedSet(list):
    my_set = set()
    res = []
    for e in list:
        if e not in my_set:
            res.append(e)
            my_set.add(e)

    return res

def main():
    table_list = []
    with open("TableList.txt", 'r', encoding='UTF8') as fr, open("RemoveDup.txt",'w',encoding='UTF-8') as fw:
        for r_line in fr:
            table_list.append(r_line.strip())

        result_list = OrderedSet(table_list)
        #result_list = list(set(table_list))

        for w_line in result_list:
            fw.write(w_line + '\n')

if __name__ == "__main__":
    main()
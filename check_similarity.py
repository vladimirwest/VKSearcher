def check_similarity(list1, list2):
    returnlist = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                returnlist.append(item1)
    return(returnlist)
#JoinSequence tutorial
#(C)2008 Robin Wellner (gvx): I placed this in Public Domain
#Level: 2 (Medium)

#This script defines one function,
#which takes a string argument and
#gives a string back.
#The goal is to join sequences of
#numbers together:
#JoinSeq('1,2,3,5,6,8,9') returns '1-3,5-6,8-9'

#Define the JoinSeq function, which takes one argument (strArg)
def JoinSeq(strArg):
#Split the string in a list: '1,3,4,6' becomes ['1', '3', '4', '6']
    ListArg = strArg.split(',')
#strOut is set to the first item of the list. In our example: '1'
    strOut = ListArg[0]
#Check if the next item follows the first directly (REF:1)
    if int(ListArg[0]) == int(ListArg[1]) - 1:
        strOut += '-'
    else:
        strOut += ','
#Note the next item is not directly added
    for I in range(1, len(ListArg)-1):
#If strOut ends with '-' (for example: '1-' or '1-3,6-')
        if strOut[-1] == '-':
#And the next item does not continue
            if int(ListArg[I]) != int(ListArg[I+1]) - 1:
#End the series with the current item and a comma.
                strOut += ListArg[I] + ','
#If there is no series, add the current item
        elif strOut[-1] == ',':
            strOut += ListArg[I]
#The same as REF:1
            if int(ListArg[I]) == int(ListArg[I+1]) - 1:
                strOut += '-'
            else:
                strOut += ','
#Return strOut plus the last item (which was not added before)
    return strOut + ListArg[-1]

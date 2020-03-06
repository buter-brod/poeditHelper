import sys
import re

filename = sys.argv[1]
file = open(filename, 'r', encoding='utf8')
filestr = file.read()
rRus = re.compile("[а-яА-Я]+")
rEng = re.compile(".*?([a-zA-Z]{2,}).*")

#msgid "Религиозные законы"
#msgstr ""

def isRus(l):
    return rRus.match(l)

def isSpace(l):
    return l == " "

def isSpaceBetweenRus(fullstr, ind):
    l = fullstr[ind]

    if not isSpace(l): 
        return False

    size = len(fullstr)

    if ind > 0 and isRus(fullstr[ind-1]): 
        return True

    if ind < size - 1 and isRus(fullstr[ind+1]): 
        return True

def removeComments(s):
    allLines = s.split('\n')
    allLinesNoComment = []

    for line in allLines:
        if len(line) == 0 or line[0] == "#":
            continue
        allLinesNoComment.append(line)
       
    noCommentStr = ''.join(allLinesNoComment)
    return noCommentStr

def rusFilter(s):
    
    length = len(s)
    filtered = ""

    for i in range(length):
        l = s[i]
        if isRus(l) or isSpaceBetweenRus(s, i):
            filtered = filtered + l
    
    return filtered

def countAllRus():

    onlyrusWithSpace = ""
    
    allText = ""
    allHasTranslation = ""
    allNoTranslation = ""

    allTextFiltered = ""
    allHasTranslationFiltered = ""
    allNoTranslationFiltered = ""

    noCommentStr = removeComments(filestr)

    allMessages = noCommentStr.split('msgid')
    allMessagesCount = len(allMessages)

    for messageStrInd in range(allMessagesCount):
        msgStr = allMessages[messageStrInd]

        translToken = "msgstr"
        whereTokenStart = msgStr.find(translToken)
        whereTokenEnd = whereTokenStart + len(translToken)

        translStr = msgStr[whereTokenEnd + 1:]

        matchTrans = rEng.match(translStr)
        hasTranslation = False

        if matchTrans:
            g0 = matchTrans.group(0)
            g1 = matchTrans.group(1)

            hasTranslation = len(g1) > 1

        allText = allText + msgStr

        if hasTranslation:
            allHasTranslation = allHasTranslation + msgStr
        else:
            allNoTranslation = allNoTranslation + msgStr

        
    allTextFiltered = rusFilter(allText)
    allHasTranslationFiltered = rusFilter(allHasTranslation)
    allNoTranslationFiltered = rusFilter(allNoTranslation)

    allLen = len(allTextFiltered)
    allTranslLen = len(allHasTranslationFiltered)
    allNoTransLen = len(allNoTranslationFiltered)

    divideUnstranslatedInd = int(allNoTransLen / 2)

    howManySymbolsShowForWorker2 = 100
    whereToStart2ndWorker = allNoTranslationFiltered[divideUnstranslatedInd:divideUnstranslatedInd + howManySymbolsShowForWorker2]

    print("your ALL russian text length with spaces:" + str(allLen))

    print("your TRANSLATED russian text length with spaces:" + str(allTranslLen))

    print("your NOT TRANSLATED russian text length with spaces:" + str(allNoTransLen))

    print("where should worker-2 start translating: " + whereToStart2ndWorker)

    print("your russian-only text (with spaces): ")
    print(allTextFiltered)

    print("your NOT TRANSLATED text: ")
    print(allNoTranslationFiltered)

    input("Press Enter to continue...")










countAllRus()




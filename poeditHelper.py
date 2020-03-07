import sys
import re

rQuotes = re.compile("\\\"(.*?)\\\"")
msgIdToken = "msgid"
msgStrToken = "msgstr"

class Entry:
    def __init__(self):
        self.key = ""
        self.trans = ""

file1Entries = []
file2Entries = []

filename1 = sys.argv[1]
filename2 = sys.argv[2] if len(sys.argv) > 3 else ""

file1 = open(filename1, 'r', encoding='utf8')
file2 = None
if filename2: file2 = open(filename2, 'r', encoding='utf8')

file1Str = file1.read()
file2Str = file2.read() if file2 else ""

file1Lines = file1Str.splitlines()

entry = None

msgIdCapture = False

for line in file1Lines:

    if len(line) == 0 or line[0] == "~": continue

    iskey1stLine = (line.find(msgIdToken) == 0)
    istrans1stLine = (line.find(msgStrToken) == 0)

    if iskey1stLine: 
        
        if entry and len(entry.key) > 0 : file1Entries.append(entry)
        
        entry = Entry()
        msgIdCapture = True

    elif istrans1stLine:
        msgIdCapture = False

    m = rQuotes.match(line)
    strInQuotes = m.group(1) if m else ""

    if len(strInQuotes) > 0:
        if msgIdCapture:
            entry.key = entry.key + strInQuotes
        else:
            entry.trans = entry.trans + strInQuotes


rusTranslatedLen = 0
rusNonTranslatedLen = 0

translatedList = []
nonTranslatedList = []

for entry in file1Entries:

    (translatedList if len(entry.trans) > 0 else nonTranslatedList).append(entry)

    #if len(entry.trans) > 0:
     #   translatedList.append(entry)
    #else:
    #    nonTranslatedList.append(entry)

rusTranslatedList = [entry.key for entry in translatedList]
rusNonTranslatedList = [entry.key for entry in nonTranslatedList]

allRusTextList  = [entry.key for entry in file1Entries]
allEngTextList  = [entry.trans for entry in file1Entries]

allRusText = ' '.join(allRusTextList)
allEngText = ' '.join(allEngTextList)

translatedRusText = ' '.join(rusTranslatedList)
untranslatedRusText = ' '.join(rusNonTranslatedList)

rusTranslatedLen = len(translatedRusText)
rusNonTranslatedLen = len(untranslatedRusText)

allRusLen = len(allRusText)
allEngLen = len(allEngText)

outputStr = ""

outputStr += "all russian text length: " + str(allRusLen) + "\n"
outputStr += "all english text length: " + str(allEngLen) + "\n"

outputStr += "russian text, that is already translated, length: " + str(rusTranslatedLen) + "\n"
outputStr += "russian text, that isn't translated yet, length: " + str(rusNonTranslatedLen) + "\n"

outputStr += "All russian text: \n" + allRusText
outputStr += "\n--------------------\nAll english text: \n--------------------\n" + allEngText
outputStr += "\n--------------------\nAll untranslated russian text: \n--------------------\n" + untranslatedRusText

print(outputStr)

output = open(filename1 + "_output", 'w')
output.write(outputStr)
output.close()

input("Press Enter to exit...")






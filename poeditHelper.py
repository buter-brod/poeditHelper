import sys
import re

strInQuotesExp = ".*?\\\"(.*?)\\\""
msgIdToken = "msgid"
msgStrToken = "msgstr"

class Entry:
    def __init__(self):
        self.key = ""
        self.trans = ""

def parseEntries(fileStr):
    
    entries = []
    entry = None
    msgIdCapture = False
    file1Lines = fileStr.splitlines()

    for line in file1Lines:

        if len(line) == 0 or line[0] == "~": continue

        iskey1stLine   = (line.find(msgIdToken)  == 0)
        istrans1stLine = (line.find(msgStrToken) == 0)

        if iskey1stLine: 
        
            if entry and len(entry.key) > 0 : entries.append(entry)
        
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

    return entries


filename1 = sys.argv[1]
filename2 = sys.argv[2] if len(sys.argv) > 2 else ""

rQuotes = re.compile(strInQuotesExp)

file1 = open(filename1, 'r', encoding='utf8')
file2 = None
if filename2: file2 = open(filename2, 'r', encoding='utf8')

file1Str = file1.read()
file2Str = file2.read() if file2 else ""

file1Entries = parseEntries(file1Str)
file2Entries = parseEntries(file2Str) if file2Str and len(file2Str) > 0 else []

def mainReport(entries):

    translatedList = []
    nonTranslatedList = []

    for entry in file1Entries:
        (translatedList if len(entry.trans) > 0 else nonTranslatedList).append(entry)

    allRusText =          ' '.join([entry.key   for entry in file1Entries])
    allEngText =          ' '.join([entry.trans for entry in file1Entries])
    translatedRusText =   ' '.join([entry.key   for entry in translatedList])
    untranslatedRusText = ' '.join([entry.key   for entry in nonTranslatedList])

    rusTranslatedLen    = len(translatedRusText)
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

    return outputStr

def diffReport(entries1, entries2):

    dict1 = {}

    for entry in entries1:
        dict1[entry.key] = entry

    entriesThatDiffer = []

    for entry in entries2:

        if entry.key not in dict1: return "error, entry '" + entry.key + "' not found in 1st file"

        corrEntry = dict1[entry.key]

        if corrEntry.trans != entry.trans:
            entriesThatDiffer.append(entry)

    allDiffersRusText = ' '.join([entry.key for entry in entriesThatDiffer])
    allDiffersRusTextLen = len(allDiffersRusText)

    outputStr = ""
    outputStr += "russian text, translation for which differs, length: " + str(allDiffersRusTextLen) + "\n"
    outputStr += "Text itself: \n" + allDiffersRusText

    return outputStr


outputStr = mainReport(file1Entries) if len(file2Entries) == 0 else diffReport(file1Entries, file2Entries)

print(outputStr)

output = open(filename1 + "_output", 'w', encoding='utf-8')
output.write(outputStr)
output.close()

input("Press Enter to exit...")

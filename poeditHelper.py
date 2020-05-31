import sys
import re

strInTag         = "\\<.*?\\>"
strInQuotesExp   = ".*?\\\"(.*?)\\\""
transPluralIdExp = "msgstr\[(\d)\].*"

msgIdToken       = "msgid"
msgIdPluralToken = "msgid_plural"
msgStrToken      = "msgstr"

rQuotes   = re.compile(strInQuotesExp)
rPluralId = re.compile(transPluralIdExp)

class Entry:
    def __init__(self):
        self.key = ""
        self.pluralKey = ""
        self.trans = {}

def parseEntries(fileStr):
    
    entries = []
    entry = None
    capture = ""
    plural_ind = -1
    
    file1Lines = fileStr.splitlines()

    for line in file1Lines:

        if len(line) == 0 or line[0] == "#": 
            continue

        iskey1stLine       = line.startswith(msgIdToken)
        isPluralkey1stLine = line.startswith(msgIdPluralToken)
        istrans1stLine     = line.startswith(msgStrToken)

        strInQuotes = ""
        quotesMatch = rQuotes.match(line)
        strInQuotes = quotesMatch.group(1) if quotesMatch else ""

        if removeTags:
            strInQuotes = re.sub(strInTag, '', strInQuotes)

        if isPluralkey1stLine:
            capture = "key_plural"
        elif iskey1stLine:
            # found a key of next entry - let's save current entry as complete
            if entry and len(entry.key) > 0 : entries.append(entry)
            entry = Entry()
            capture = "key"
        elif istrans1stLine:
            capture = "trans"

        if capture == "key_plural":
            entry.pluralKey = entry.pluralKey + strInQuotes
        elif capture == "key":
            entry.key = entry.key + strInQuotes
        elif capture == "trans" and len(entry.key) > 0:
            pluralIdMatch = rPluralId.match(line)
            plural_ind = int(pluralIdMatch.group(1)) if pluralIdMatch else 0
            transStr = entry.trans[plural_ind] if plural_ind in entry.trans else ""
            entry.trans[plural_ind] = transStr + strInQuotes
        
    if entry and len(entry.key) > 0: entries.append(entry)
    return entries


filename1 = sys.argv[1]
filename2 = None
removeTags = True

if len(sys.argv) > 2:
    arg2 = sys.argv[2]
    if arg2 == '-noremovetags':
        removeTags = False
    else:
        filename2 = arg2


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
        list = translatedList
        for pluralInd, pluralStr in entry.trans.items():
            if not pluralStr: 
                list = nonTranslatedList
                break

        list.append(entry)

    allRusText          = ' '.join([entry.key      for entry in file1Entries])
    allEngText          = ' '.join([entry.trans[0] for entry in file1Entries])
    translatedRusText   = ' '.join([entry.key      for entry in translatedList])
    untranslatedRusText = ' '.join([entry.key      for entry in nonTranslatedList])

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

import re
# setting a threshold for approximation
afDecimalthreshold=0.5
# regex to get an integer defined below
# has any numbers divided by dots and a single optional dash at the end
integersRegex=re.compile(r"\b\d+(\.?\d+)*(,\d+)?\b")
# to get only the percentage same as numbers but end in prozent
percentRegex=re.compile(r"\b\d+(\.?\d+)*(,\d+)? Prozent\b")
# to get any number ending with the Grad Celsius 
tempRegex=re.compile(r"\b\d+(\.?\d+)*(,\d+)* Grad Celsius\b")
# to get years or months
yearsormonthsRegex=re.compile(r"\b(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|Jahr) \d+(\.?\d+)*(,\d+)*\b")
def approx(number,isNegative:bool=False)->str:
    """
    this function takes as an input any number found by regex and return the approximation of this number
    the approximation is done by checking an threshold define above in various regions
    """
    spbydash=number.split(',')
    addition = 0
    signedNo= -1 if isNegative else 1
    if len(spbydash)>1:
        # dash approximation
        afterDecimalthreshold = afDecimalthreshold * (10**len(spbydash[1]))
        addition = signedNo if int(spbydash[1]) > afterDecimalthreshold else 0
    decimalpointsplit = spbydash[0].split('.')
    number = int(decimalpointsplit[0]) 
    tmp = 0 
    if len(decimalpointsplit)>1:
        lendecimalsplits=len(decimalpointsplit)-1
        while(lendecimalsplits>0):
            # dot approximation
            if int(decimalpointsplit[lendecimalsplits])+addition>(afDecimalthreshold * (10**len(decimalpointsplit[lendecimalsplits]))):
                addition = 1
            else:
                addition = 0 
            decimalpointsplit[lendecimalsplits] = len(decimalpointsplit[lendecimalsplits])*'0'
            lendecimalsplits-=1
    decimalpointsplit[0]= str(number+addition)
    addition=0
    stri=''
    # number approximation
    for i in range(len(decimalpointsplit[0])-1,0,-1):
        if int(decimalpointsplit[0][i])+addition > 10*afDecimalthreshold:
            addition = 1
        else:
            addition = 0
        stri+='0'  
    stri+=str(int(decimalpointsplit[0][0])+addition)

    decimalpointsplit[0]=stri[::-1]
    return '.'.join(decimalpointsplit) 
def approxMatch(match):
    """
    wrapper for the approximation
    """
    number = match.group()
    approximation = approx(number)
    return "etwa "+approximation
def approxCelsiusMatch(match):
    number = match.group()
    number = number.replace(" Grad Celsius","")
    return "etwa "+approx(number)+" Grad Celsius"

def convertToInt(number:str):
    splitByDot = number.split('.')
    prod = 1
    for _ in range(len(splitByDot)-1,0,-1):
        prod*=1000
    return int(splitByDot[0])*prod


def parsePercent(match)->str:
    percentage = match.group()
    percentage = percentage.replace(" Prozent",'')
    percentage = approx(percentage)
    percentage = convertToInt(percentage)
    if percentage < 25:
        return "wenige"
    elif percentage == 25:
        return "jeder Vierte"
    elif percentage < 50:
        return "wenige"
    elif percentage == 50:
        return "die Hälfte"
    elif percentage < 75:
        return "mehr als die hälfte"
    elif percentage == 75:
        return "drei von vier"
    elif percentage < 100:
        return "fast alle"
    else:
        return "mehr als hundert Prozent"
monthyearstack=[]
def denymatch(match):
    monthyear=match.group()
    # global monthyearstack
    monthyearstack.append(monthyear)
    return "*"*11
def PutbackYearMonth(raw_text:str)->str:
    # global monthyearstack
    for i in range(len(monthyearstack)):
        raw_text=raw_text.replace("*"*11,monthyearstack[i],1)
    return raw_text
def simplify_numbers(raw_text:str):
    raw_text = re.sub(percentRegex, parsePercent, raw_text)
    raw_text = re.sub(tempRegex,approxCelsiusMatch, raw_text)
    raw_text = re.sub(yearsormonthsRegex,denymatch, raw_text)
    raw_text = re.sub(integersRegex, approxMatch, raw_text)
    raw_text = PutbackYearMonth(raw_text)
    global monthyearstack
    monthyearstack = []
    return raw_text
test_cases = [
"324.620,22 Euro wurden gespendet.",
"1.897 Menschen nahmen teil.",
"25 Prozent der Bevölkerung sind betroffen.",
"90 Prozent stimmten zu.",
"14 Prozent lehnten ab.",
"Bei 38,7 Grad Celsius ist es sehr heiß.",
"denn die Rente steigt um 4,57 Prozent.",
"Im Jahr 2024 gab es 1.234 Ereignisse.",
"Am 1. Januar 2024 waren es 5.678 Teilnehmer.",
"Im Jahr 2025 gab es 2018 Ereignisse."
]
for i in test_cases:
    print(simplify_numbers(i))
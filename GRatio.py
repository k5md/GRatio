# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog as tkFileDialog
from math import floor, ceil
import re


FLOOR = 1
ROUND = 2
CEIL = 3


def SaveResults():
    fn = tkFileDialog.SaveAs(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn+=".txt"
    open(fn, 'wt').write(resultBox.get('1.0', 'end'))


def LoadText():
    fn = tkFileDialog.Open(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    data = open(fn, 'rt').read()
    textBox.delete('1.0', 'end') 
    textBox.insert('1.0', data)


def LoadStoptokens():
    fn = tkFileDialog.Open(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    data = open(fn, 'rt').read()
    stoptextEntryText.set(data)
    

def SaveStoptokens():
    fn = tkFileDialog.SaveAs(root, filetypes = [('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn+=".txt"
    open(fn, 'wt').write(stoptextEntryText.get())


def ProcessText(multiplier):
    global hType
    inputText = textBox.get('1.0', 'end')
    stopTokens = stoptextEntryText.get()

    sentenses = re.split("\n+|\.+|\?+|!+", inputText)
    stopTokens = re.split(",", stopTokens)
    stopTokens = [i.strip() for i in stopTokens]
    if '' in stopTokens:
        stopTokens.remove('')
    print(len(stopTokens))
    
    print("Stop tokens: ", stopTokens)
    print("Multiplier: ", multiplier)

    allTokens = []

    for s in sentenses:
        tokens = re.split("[^а-яА-ЯёЁa-zA-Z0-9-]+", s)
        tokens = [i.strip() for i in tokens]
        if '' in tokens:
            tokens.remove('')
        tokens = [i for i in tokens if i not in stopTokens]

        if len(tokens) == 0:
            continue

        allTokens += tokens
        
        print("Sentense: ", s, "\nTokens: ", tokens, " Length: ", len(tokens))

        harmonicCenterRaw = len(tokens) * multiplier
        
        print("Local harmonic center(raw):", harmonicCenterRaw)
        
        harmonicCenter = harmonicCenterRaw

        if hType.get() == FLOOR:
            harmonicCenter = floor(harmonicCenter)
        elif hType.get() == ROUND:
            harmonicCenter = round(harmonicCenter)
        elif hType.get() == CEIL:
            harmonicCenter = ceil(harmonicCenter)
        else:
            raise ValueError("checkbuttons values incorrect, only one should be in SELECTED state")
    
        resultBox.insert(END, "{0} {1} {2}\n".format(tokens[harmonicCenter-1], harmonicCenterRaw, harmonicCenter))

    if len(allTokens) == 0:
        return
    
    absHarmonicCenterRaw = len(allTokens) * multiplier
    print("Absolute harmonic center(raw):", absHarmonicCenterRaw)

    absHarmonicCenter = absHarmonicCenterRaw
    if hType.get() == FLOOR:
        absHarmonicCenter = floor(absHarmonicCenter)
    elif hType.get() == ROUND:
        absHarmonicCenter = round(absHarmonicCenter)
    elif hType.get() == CEIL:
        absHarmonicCenter = ceil(absHarmonicCenter)
    else:
        raise ValueError("checkbuttons values incorrect, only one should be in SELECTED state")
    resultBox.insert(END, "\n{0} {1} {2}\n".format(allTokens[absHarmonicCenter-1], absHarmonicCenterRaw, absHarmonicCenter))


def GetMultiplier():
    try:
        multiplier = float(multipliervalueEntryText.get())
        return multiplier
    except ValueError:
        raise ValueError("multiplier value is not a float")
    

def ProcessCenterPos():
    ProcessText(GetMultiplier())
    

def ProcessLeftPos():
    ProcessText(GetMultiplier()-0.236)


def ProcessRightPos():
    ProcessText(GetMultiplier()+0.236)

    
root = Tk()


### MENU

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open text for analysis", command=LoadText, accelerator="Ctrl+O")
filemenu.add_command(label="Save results", command=SaveResults, accelerator="Ctrl+S")
filemenu.add_command(label="Import stoptokens", command=LoadStoptokens)
filemenu.add_command(label="Export stoptokens", command=SaveStoptokens)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Get right position", command=ProcessRightPos, accelerator="Ctrl+T")
editmenu.add_command(label="Get center position", command=ProcessCenterPos, accelerator="Ctrl+G")
editmenu.add_command(label="Get left position", command=ProcessLeftPos, accelerator="Ctrl+B")

menubar.add_cascade(label="Process", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


### SHORTCUT BINDINGS

root.bind("<Control-o>", lambda x: LoadText())
root.bind("<Control-s>", lambda x: SaveResults())
root.bind("<Control-t>", lambda x: ProcessRightPos())
root.bind("<Control-g>", lambda x: ProcessCenterPos())
root.bind("<Control-b>", lambda x: ProcessLeftPos())


### FRAMES

rootFrame = Frame(root)

inputFrame = LabelFrame(rootFrame, text="Input")
outputFrame = LabelFrame(rootFrame, text="Output")

inputOptionsFrame = Frame(inputFrame)
outputOptionsFrame = Frame(outputFrame)

inputOptionsSMFrame = Frame(inputOptionsFrame)
inputOptionsStoptokensFrame = LabelFrame(inputOptionsSMFrame, text="Tokens to exclude")
inputOptionsMultiplierFrame = LabelFrame(inputOptionsSMFrame, text="Multiplier")
inputOptionsExecuteFrame = LabelFrame(inputOptionsFrame, text="Get AP")
inputOptionsRoundingFrame = LabelFrame(inputOptionsFrame, text="Rounding type")

outputOptionsFormatFrame = LabelFrame(outputOptionsFrame, text="Formatting options")
outputOptionsFormatIndex = Frame(outputOptionsFormatFrame)
outputOptionsFormatValue = Frame(outputOptionsFormatFrame)
outputOptionsFormatToken = Frame(outputOptionsFormatFrame)
outputOptionsFormatTotal = Frame(outputOptionsFormatFrame)


### FRAME PACKING

rootFrame.pack(fill=BOTH, expand=True)
inputFrame.pack(side=LEFT, fill="y")
outputFrame.pack(side=LEFT, fill="y")


### TEXTS

textBox = Text(inputFrame, font='Arial 14', wrap='word')
resultBox = Text(outputFrame, font='Arial 14', wrap='word')


### ENTRIES & STRINGVARS DECLARATIONS

stoptextEntryText = StringVar()
stoptextEntry = Entry(inputOptionsStoptokensFrame, font='Arial 14', textvariable=stoptextEntryText)
multipliervalueEntryText = StringVar(value="0.618")
multipliervalueEntry = Entry(inputOptionsMultiplierFrame, font='Arial 14', textvariable=multipliervalueEntryText)


### BUTTONS

loadtextBtn = Button(inputFrame, text = 'Open document', command = LoadText)
loadstoptextBtn = Button(inputOptionsStoptokensFrame, text = 'Open', command = LoadStoptokens)
savestoptextBtn = Button(inputOptionsStoptokensFrame, text = 'Save', command = SaveStoptokens)
saveresultsBtn = Button(outputFrame, text = 'Save results', command = SaveResults)

leftPosBtn = Button(inputOptionsExecuteFrame, text = '-0.236', command = lambda: ProcessLeftPos())
centerPosBtn = Button(inputOptionsExecuteFrame, text = 'Process', command = lambda: ProcessCenterPos())
rightPosBtn = Button(inputOptionsExecuteFrame, text = '+0.236', command = lambda: ProcessRightPos())


### RADIOBUTTONS

hType = IntVar()

floorCheckBtn = Radiobutton(inputOptionsRoundingFrame, text="Floor", value=FLOOR, variable=hType)
roundCheckBtn = Radiobutton(inputOptionsRoundingFrame, text="Round", value=ROUND, variable=hType)
ceilCheckBtn = Radiobutton(inputOptionsRoundingFrame, text="Ceil", value=CEIL, variable=hType)

roundCheckBtn.select()


### CHECKBUTTONS

#outputOptionsFormatIndex
#outputOptionsFormatValue
#outputOptionsFormatToken
#outputOptionsFormatTotal


### INPUT FRAME ITEMS PACKING

loadtextBtn.pack(side=TOP, fill="x")
textBox.pack(side=TOP, fill="both", expand=True)

inputOptionsFrame.pack(side=LEFT)

inputOptionsSMFrame.pack(side=LEFT)

inputOptionsStoptokensFrame.pack(side=TOP, fill="x", expand=True)
stoptextEntry.pack(side=LEFT)
loadstoptextBtn.pack(side=LEFT)
savestoptextBtn.pack(side=LEFT)

inputOptionsMultiplierFrame.pack(side=TOP, fill="x")
multipliervalueEntry.pack(side=LEFT)

inputOptionsRoundingFrame.pack(side=LEFT, fill="y")
floorCheckBtn.pack(side=TOP, anchor=W)
roundCheckBtn.pack(side=TOP, anchor=W)
ceilCheckBtn.pack(side=TOP, anchor=W)

inputOptionsExecuteFrame.pack(side=LEFT, fill="y")
leftPosBtn.pack(side=TOP, fill="x")
centerPosBtn.pack(side=TOP, fill="x")
rightPosBtn.pack(side=TOP, fill="x")


### OUTPUT FRAME ITEMS PACKING

saveresultsBtn.pack(side=TOP, fill="x")
resultBox.pack(side=TOP, fill="y", expand=True)

outputOptionsFrame.pack(side=LEFT)

outputOptionsFormatFrame.pack(side=LEFT)


root.mainloop()


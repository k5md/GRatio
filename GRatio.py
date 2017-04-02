# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog as tkFileDialog
from math import floor, ceil
import re

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


def ProcessText():
    global hType
    inputText = textBox.get('1.0', 'end')
    stopTokens = stoptextEntryText.get()
    try:
        multiplier = float(multipliervalueEntryText.get())
    except ValueError:
        raise ValueError("multiplier value is not a float")

    sentenses = re.split("\n+|\.+|\?+|!+", inputText)
    stopTokens = re.split(",", stopTokens)
    stopTokens = [i.strip() for i in stopTokens]
    if '' in stopTokens:
        stopTokens.remove('')
    print(len(stopTokens))
    
    print("Stop tokens: ", stopTokens)
    print("Multiplier: ", multiplier)

    for s in sentenses:
        tokens = re.split("[^а-яА-ЯёЁa-zA-Z0-9-]+", s)
        tokens = [i.strip() for i in tokens]
        if '' in tokens:
            tokens.remove('')
        tokens = [i for i in tokens if i not in stopTokens]
        if len(tokens) == 0:
            continue
        
        print("Sentense: ", s, "\nTokens: ", tokens, " Length: ", len(tokens))

        harmonicCenterRaw = len(tokens) * multiplier

        print("Harmonic center(raw):", harmonicCenterRaw)

        harmonicCenter = harmonicCenterRaw

        if hType.get() == 1:
            harmonicCenter = floor(harmonicCenter)
            print("Harmonic center(floor):", harmonicCenter, "Word: ", tokens[harmonicCenter-1])
        elif hType.get() == 2:
            harmonicCenter = round(harmonicCenter)
            print("Harmonic center(round):", harmonicCenter, "Word: ", tokens[harmonicCenter-1])
        elif hType.get() == 3:
            harmonicCenter = ceil(harmonicCenter)
            print("Harmonic center(ceil):", harmonicCenter, "Word: ", tokens[harmonicCenter-1])
        else:
            raise ValueError("checkbuttons values incorrect, only one should be in SELECTED state")
    
        resultBox.insert(END, "\n{0} {1} {2}".format(tokens[harmonicCenter-1], harmonicCenterRaw, harmonicCenter))
        

root = Tk()


### FRAMES

rootFrame = Frame(root)
inputFrame = LabelFrame(rootFrame, text="Input")
outputFrame = LabelFrame(rootFrame, text="Output")


### FRAME PACKING

rootFrame.pack(fill=BOTH, expand=True)
inputFrame.pack(side=LEFT, fill="y")
outputFrame.pack(side=LEFT, fill="y")


### TEXTS

textBox = Text(inputFrame, font='Arial 14', wrap='word')
resultBox = Text(outputFrame, font='Arial 14', wrap='word')


### LABELS

stoptextLabel = Label(inputFrame, text="Tokens to exclude:")
multipliervalueLabel = Label(inputFrame, text="Multiplier:")


### ENTRIES & STRINGVARS DECLARATIONS

stoptextEntryText = StringVar()
stoptextEntry = Entry(inputFrame, font='Arial 14', textvariable=stoptextEntryText)
multipliervalueEntryText = StringVar(value="0.618")
multipliervalueEntry = Entry(inputFrame, font='Arial 14', textvariable=multipliervalueEntryText)


### BUTTONS

loadtextBtn = Button(inputFrame, text = 'Open document', command = LoadText)
loadstoptextBtn = Button(inputFrame, text = 'Open', command = LoadStoptokens)
savestoptextBtn = Button(inputFrame, text = 'Save', command = SaveStoptokens)
saveresultsBtn = Button(outputFrame, text = 'Save results', command = SaveResults)
processtextBtn = Button(inputFrame, text = 'Process', command = ProcessText)


### CHECKBOXES

hType = IntVar()

floorCheckBtn = Checkbutton(inputFrame, text="Floor", variable=hType, onvalue=1, offvalue=hType.get(), command=lambda i=hType: print("Operation type now:", i.get()))
roundCheckBtn = Checkbutton(inputFrame, text="Round", variable=hType, onvalue=2, offvalue=hType.get(), command=lambda i=hType: print("Operation type now:", i.get()))
ceilCheckBtn = Checkbutton(inputFrame, text="Ceil", variable=hType, onvalue=3, offvalue=hType.get(), command=lambda i=hType: print("Operation type now:", i.get()))

roundCheckBtn.select()


### INPUT FRAME ITEMS PACKING

loadtextBtn.pack(side=TOP, fill="x")
textBox.pack(side=TOP, fill="y", expand=True)
stoptextLabel.pack(side=LEFT)
stoptextEntry.pack(side=LEFT)
loadstoptextBtn.pack(side=LEFT)
savestoptextBtn.pack(side=LEFT)
multipliervalueLabel.pack(side=LEFT)
multipliervalueEntry.pack(side=LEFT)
processtextBtn.pack(side=LEFT)
floorCheckBtn.pack(side=LEFT)
roundCheckBtn.pack(side=LEFT)
ceilCheckBtn.pack(side=LEFT)

### OUTPUT FIELD ITEMS PACKING

saveresultsBtn.pack(side=TOP, fill="x")
resultBox.pack(side=TOP, fill="y", expand=True)


root.mainloop()


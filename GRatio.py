# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog as tkFileDialog
from math import floor, ceil
import re
from tkinter.scrolledtext import ScrolledText

FLOOR = 1
ROUND = 2
CEIL = 3

RUSSIAN = {
    "d_open_text" : "Открыть текст для анализа",
    "d_save_results" : "Сохранить результаты",
    "d_import_stop_tokens" : "Импортировать исключения",
    "d_save_stop_tokens" : "Экспортировать исключения",
    "d_exit": "Выйти",
    "d_file": "Файл",
    "d_process": "Обработать",
    "d_get_left": "АСП2",
    "d_get_center": "Гармонический центр",
    "d_get_right": "АСП1",
    "d_help" : "Помощь",
    "d_about": "О программе",
    "d_input": "Исходные данные:",
    "d_tokens_to_exclude": "Токены-исключения",
    "d_open": "Открыть",
    "d_save": "Сохранить",
    "d_use_stop_tokens": "Использовать исключения",
    "d_multiplier": "Множитель",
    "d_rounding_type": "Тип округления",
    "d_floor": "К меньшему",
    "d_ceil": "К большему",
    "d_round": "К ближайшему",
    "d_get_ap": "Обработать",
    "d_center": "Центр",
    "d_center_abbr": "Ц",
    "d_output": "Результаты",
    "d_formatting_options": "Настройки вывода",
    "d_index": "Позиция (в тексте БЕЗ токенов-исключений)",
    "d_local_position_value": "Выводить значение позиции (предложение)",
    "d_token": "Токен",
    "d_sentence": "Предложение",
    "d_absolute_position_value": "Выводить значение позиции (текст)",
    "d_append_separator": "Добавить разделитель",
    "o_absolute_beginning": "Абсолютное начало",
    "o_beginning": "Зачин",
    "o_harmonic_center_beginning": "Гармонический центр зоны начала",
    "o_absolute_weak_position_1": "АСП1",
    "o_harmonic_center": "Гармонический центр",
    "o_absolute_weak_position_2": "АСП2",
    "o_absolute_end": "Абсолютный конец",
    "o_absolute_values_full_text": "Абсолютные значения (текст)",
    "p_tokens": "Токены",
    "p_stop_tokens": "Токены-исключения",
    "p_multiplier": "Множитель",
    "p_sentence": "Предложение",
    "p_tokens_length": "Число токенов",
    "p_local_harmonic_center_raw": "Локальный гармонический центр (без окр.)",
    "p_absolute_harmonic_center_raw": "Абсолютный гармонический центр (без окр.)",
}

ENGLISH = {
    "d_open_text" : "Open text",
    "d_save_results" : "Save analysis results",
    "d_import_stop_tokens" : "Import stop-tokens from file",
    "d_save_stop_tokens" : "Export stop-tokens to file",
    "d_exit": "Exit",
    "d_file": "File",
    "d_process": "Process",
    "d_get_left": "AWP2",
    "d_get_center": "Harmonic center",
    "d_get_right": "AWP1",
    "d_help" : "Help",
    "d_about": "About",
    "d_input": "Input:",
    "d_tokens_to_exclude": "Tokens to exclude",
    "d_open": "Open",
    "d_save": "Save",
    "d_use_stop_tokens": "Use stop-tokens",
    "d_multiplier": "Multiplier",
    "d_rounding_type": "Rounding type",
    "d_floor": "Floor",
    "d_ceil": "Ceil",
    "d_round": "Round",
    "d_get_ap": "Get AP",
    "d_center": "Center",
    "d_center_abbr": "C",
    "d_output": "Output",
    "d_formatting_options": "Formatting options",
    "d_index": "Position (with stop-tokens EXCLUDED)",
    "d_local_position_value": "Show position value (sentence)",
    "d_token": "Token",
    "d_sentence": "Sentence",
    "d_absolute_position_value": "Show position value (text)",
    "d_append_separator": "Append separator",
    "o_absolute_beginning": "Absolute beginning",
    "o_beginning": "Beginning",
    "o_harmonic_center_beginning": "Harmonic center (beginning)",
    "o_absolute_weak_position_1": "AWP1",
    "o_harmonic_center": "Harmonic center",
    "o_absolute_weak_position_2": "AWP2",
    "o_absolute_end": "Absolute end",
    "o_absolute_values_full_text": "Absolute values (text)",
    "p_tokens": "Tokens",
    "p_stop_tokens": "Stop-tokens",
    "p_multiplier": "Multiplier",
    "p_sentence": "Sentence",
    "p_tokens_length": "Tokens length",
    "p_local_harmonic_center_raw": "Local harmonic center (raw)",
    "p_absolute_harmonic_center_raw": "Absolute harmonic center (raw)",
}

LOCAL = ENGLISH


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

    stopTokens = ""

    if useStoptokensValue.get():
        stopTokens = stoptextEntryText.get()
    
    sentenses = re.split("\n+|\.+|\?+|!+", inputText)

    stopTokens = re.split(",", stopTokens)
    stopTokens = [i.strip() for i in stopTokens]
    if '' in stopTokens:
        stopTokens.remove('')
    
    print("{}:".format(LOCAL["p_stop_tokens"]), stopTokens)
    print("{}:".format(LOCAL["p_multiplier"]), multiplier)

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
        
        print("{}: {}\n{}: {} {}: {}".format(LOCAL["p_sentence"], s, LOCAL["p_tokens"], tokens, LOCAL["p_tokens_length"], len(tokens)))

        harmonicCenterRaw = (len(tokens) - 1) * multiplier
        
        print("{}:".format(LOCAL["p_local_harmonic_center_raw"]), harmonicCenterRaw)
        
        harmonicCenter = harmonicCenterRaw

        if hType.get() == FLOOR:
            harmonicCenter = floor(harmonicCenter)
        elif hType.get() == ROUND:
            harmonicCenter = round(harmonicCenter)
        elif hType.get() == CEIL:
            harmonicCenter = ceil(harmonicCenter)
        else:
            raise ValueError("checkbuttons values incorrect, only one should be in SELECTED state")
    
        resultBox.insert(END, FormatOutput(s, tokens[harmonicCenter], harmonicCenter, harmonicCenterRaw, harmonicCenter))
        
                                
    if len(allTokens) == 0:
        return
    
    if includeTotal.get():
    
        absHarmonicCenterRaw = (len(allTokens) - 1) * multiplier
        print("{}:".format(LOCAL["p_absolute_harmonic_center_raw"]), absHarmonicCenterRaw)

        absHarmonicCenter = absHarmonicCenterRaw
        if hType.get() == FLOOR:
            absHarmonicCenter = floor(absHarmonicCenter)
        elif hType.get() == ROUND:
            absHarmonicCenter = round(absHarmonicCenter)
        elif hType.get() == CEIL:
            absHarmonicCenter = ceil(absHarmonicCenter)
        else:
            raise ValueError("checkbuttons values incorrect, only one should be in SELECTED state")
        resultBox.insert(END, "{}:\n".format(LOCAL["o_absolute_values_full_text"]))
        resultBox.insert(END, FormatOutput("", allTokens[absHarmonicCenter], absHarmonicCenter, absHarmonicCenterRaw, absHarmonicCenter))
        

        if includeSeparator.get():
            resultBox.insert(END, "############\n")


def GetMultiplier():
    try:
        multiplier = float(multipliervalueEntryText.get())
        return multiplier
    except ValueError:
        raise ValueError("multiplier value is not a float")
    

def ProcessZeroPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_absolute_beginning"]))
    ProcessText(0)
    

def ProcessIntroPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_beginning"]))
    ProcessText(0.146)


def ProcessHCIntroPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_harmonic_center_beginning"]))
    ProcessText(0.236)
    

def ProcessLeftPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_absolute_weak_position_1"]))
    ProcessText(GetMultiplier()-0.236)


def ProcessCenterPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_harmonic_center"]))
    ProcessText(GetMultiplier())

    
def ProcessRightPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_absolute_weak_position_2"]))
    ProcessText(GetMultiplier()+0.236)


def ProcessEndPos():
    resultBox.insert(END, "{}:\n".format(LOCAL["o_absolute_end"]))
    ProcessText(1)

    
def FormatOutput(sentence, token, index, valueRaw, value):
    flags = [flag.get() for flag in [includeSentence,
                                     includeLPValue,
                                     includeToken,
                                     includeIndex]
             ]

    items = [str(item) for (item, mask) in zip([sentence, value, token, index],flags) if mask]
    return "\t".join(items) + "\n"


root = Tk()

root.minsize(1280,800)

root.title("GRatio")


### MENU

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label=LOCAL["d_open_text"], command=LoadText, accelerator="Ctrl+O")
filemenu.add_command(label=LOCAL["d_save_results"], command=SaveResults, accelerator="Ctrl+S")
filemenu.add_command(label=LOCAL["d_import_stop_tokens"], command=LoadStoptokens)
filemenu.add_command(label=LOCAL["d_save_stop_tokens"], command=SaveStoptokens)
filemenu.add_separator()
filemenu.add_command(label=LOCAL["d_exit"], command=root.quit)
menubar.add_cascade(label=LOCAL["d_file"], menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label=LOCAL["d_get_right"], command=ProcessRightPos, accelerator="Ctrl+T")
editmenu.add_command(label=LOCAL["d_get_center"], command=ProcessCenterPos, accelerator="Ctrl+G")
editmenu.add_command(label=LOCAL["d_get_left"], command=ProcessLeftPos, accelerator="Ctrl+B")

menubar.add_cascade(label=LOCAL["d_process"], menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label=LOCAL["d_about"])
menubar.add_cascade(label=LOCAL["d_help"], menu=helpmenu)

root.config(menu=menubar)


### SHORTCUT BINDINGS

root.bind("<Control-o>", lambda x: LoadText())
root.bind("<Control-s>", lambda x: SaveResults())
root.bind("<Control-t>", lambda x: ProcessRightPos())
root.bind("<Control-g>", lambda x: ProcessCenterPos())
root.bind("<Control-b>", lambda x: ProcessLeftPos())


### FRAMES

rootFrame = Frame(root)

inputFrame = LabelFrame(rootFrame, text=LOCAL["d_input"])
outputFrame = LabelFrame(rootFrame, text=LOCAL["d_output"])

inputOptionsFrame = Frame(inputFrame)
outputOptionsFrame = Frame(outputFrame)

inputOptionsSMFrame = Frame(inputOptionsFrame)
inputOptionsStoptokensFrame = LabelFrame(inputOptionsSMFrame, text=LOCAL["d_tokens_to_exclude"])
inputOptionsMultiplierFrame = LabelFrame(inputOptionsSMFrame, text=LOCAL["d_multiplier"])
inputOptionsExecuteFrame = LabelFrame(inputOptionsFrame, text=LOCAL["d_get_ap"])
inputOptionsRoundingFrame = LabelFrame(inputOptionsFrame, text=LOCAL["d_rounding_type"])

outputOptionsFormatFrame = LabelFrame(outputOptionsFrame, text=LOCAL["d_formatting_options"])


### FRAME PACKING

rootFrame.grid(row=0, column=0, sticky="wens")
inputFrame.grid(row=0, column=0, sticky="wens")
outputFrame.grid(row=0, column=1, sticky="wens")


### TEXTS

textBox = ScrolledText(inputFrame, font='Verdana 12', wrap='word')
resultBox = ScrolledText(outputFrame, font='Verdana 12', wrap='word')


### ENTRIES & STRINGVARS DECLARATIONS

stoptextEntryText = StringVar()
stoptextEntry = Entry(inputOptionsStoptokensFrame, font='Verdana 14', textvariable=stoptextEntryText)
multipliervalueEntryText = StringVar(value="0.618")
multipliervalueEntry = Entry(inputOptionsMultiplierFrame, font='Verdana 14', textvariable=multipliervalueEntryText)


### BUTTONS

loadtextBtn = Button(inputFrame, text = LOCAL["d_open_text"], command = LoadText)
loadstoptextBtn = Button(inputOptionsStoptokensFrame, text = LOCAL["d_import_stop_tokens"], command = LoadStoptokens)
savestoptextBtn = Button(inputOptionsStoptokensFrame, text = LOCAL["d_save_stop_tokens"], command = SaveStoptokens)
saveresultsBtn = Button(outputFrame, text = LOCAL["d_save_results"], command = SaveResults)


zeroPosBtn = Button(inputOptionsExecuteFrame, text = '0', command = lambda: ProcessZeroPos())
introPosBtn = Button(inputOptionsExecuteFrame, text = '0.146', command = lambda: ProcessIntroPos())
hCIntroPosBtn = Button(inputOptionsExecuteFrame, text = '0.236', command = lambda: ProcessHCIntroPos())
leftPosBtn = Button(inputOptionsExecuteFrame, text = '{}-0.236'.format(LOCAL["d_center_abbr"]), command = lambda: ProcessLeftPos())
centerPosBtn = Button(inputOptionsExecuteFrame, text = LOCAL["d_center"], command = lambda: ProcessCenterPos())
rightPosBtn = Button(inputOptionsExecuteFrame, text = '{}+0.236'.format(LOCAL["d_center_abbr"]), command = lambda: ProcessRightPos())
endPosBtn = Button(inputOptionsExecuteFrame, text = '1', command = lambda: ProcessEndPos())

### RADIOBUTTONS

hType = IntVar()

floorRadioBtn = Radiobutton(inputOptionsRoundingFrame, text=LOCAL["d_floor"], value=FLOOR, variable=hType)
roundRadioBtn = Radiobutton(inputOptionsRoundingFrame, text=LOCAL["d_round"], value=ROUND, variable=hType)
ceilRadioBtn = Radiobutton(inputOptionsRoundingFrame, text=LOCAL["d_ceil"], value=CEIL, variable=hType)

roundRadioBtn.select()


### CHECKBUTTONS

useStoptokensValue = IntVar()

includeLPValue = IntVar()
includeSentence = IntVar()
includeToken = IntVar()
includeIndex = IntVar()
includeTotal = IntVar()
includeSeparator = IntVar()

useStoptokensCheckBtn = Checkbutton(inputOptionsStoptokensFrame, text=LOCAL["d_use_stop_tokens"], variable=useStoptokensValue, onvalue=1, offvalue=0)

includeLPValueCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_local_position_value"], variable=includeLPValue, onvalue=1, offvalue=0)
includeTokenCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_token"], variable=includeToken, onvalue=1, offvalue=0)
includeSentenceCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_sentence"], variable=includeSentence, onvalue=1, offvalue=0)
includeIndexCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_index"], variable=includeIndex, onvalue=1, offvalue=0)
includeTotalCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_absolute_position_value"], variable=includeTotal, onvalue=1, offvalue=0)
includeSeparatorCheckBtn = Checkbutton(outputOptionsFormatFrame, text=LOCAL["d_append_separator"], variable=includeSeparator, onvalue=1, offvalue=0)

useStoptokensCheckBtn.select()

includeLPValueCheckBtn.select()
includeTokenCheckBtn.select()
includeIndexCheckBtn.select()
includeTotalCheckBtn.select()
includeSeparatorCheckBtn.select()


### INPUT FRAME ITEMS PACKING

loadtextBtn.grid(row=0, column=0, sticky="wens")
textBox.grid(row=1, column=0, sticky="wens")

inputOptionsFrame.grid(row=2, column=0, sticky="wens")

inputOptionsSMFrame.pack(side=LEFT)

inputOptionsStoptokensFrame.pack(side=TOP, fill="x", expand=True)
stoptextEntry.pack(side=LEFT)
loadstoptextBtn.pack(side=LEFT)
savestoptextBtn.pack(side=LEFT)

inputOptionsMultiplierFrame.pack(side=TOP, fill="x")
multipliervalueEntry.pack(side=LEFT)
useStoptokensCheckBtn.pack(side=LEFT)

inputOptionsRoundingFrame.pack(side=LEFT, fill="y")
floorRadioBtn.pack(side=TOP, anchor=W)
roundRadioBtn.pack(side=TOP, anchor=W)
ceilRadioBtn.pack(side=TOP, anchor=W)

inputOptionsExecuteFrame.pack(side=LEFT, fill="y")
zeroPosBtn.pack(side=LEFT, fill="x")
introPosBtn.pack(side=LEFT, fill="x")
hCIntroPosBtn.pack(side=LEFT, fill="x")
leftPosBtn.pack(side=LEFT, fill="x")
centerPosBtn.pack(side=LEFT, fill="x")
rightPosBtn.pack(side=LEFT, fill="x")
endPosBtn.pack(side=LEFT, fill="x")


### OUTPUT FRAME ITEMS PACKING

saveresultsBtn.grid(row=0, column=0, sticky="wens")
resultBox.grid(row=1, column=0, sticky="wens")

outputOptionsFrame.grid(row=2, column=0, sticky="wens")

outputOptionsFormatFrame.pack(side=LEFT, fill="both", expand=True)

includeIndexCheckBtn.grid(row = 0, column = 0, sticky="w")
includeLPValueCheckBtn.grid(row = 1, column = 0, sticky="w")
includeTokenCheckBtn.grid(row = 0, column = 1, sticky="w")
includeSentenceCheckBtn.grid(row = 1, column = 1, sticky="w")
includeTotalCheckBtn.grid(row = 0, column = 2, sticky="w")
includeSeparatorCheckBtn.grid(row = 1, column = 2, sticky="w")


### GRID ITEMS CONFIGURATING

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

Grid.rowconfigure(rootFrame, 0, weight=1)
Grid.columnconfigure(rootFrame, 0, weight=1)
Grid.columnconfigure(rootFrame, 1, weight=1)

Grid.rowconfigure(inputFrame, 1, weight=1)

Grid.columnconfigure(inputFrame, 0, weight=1)
Grid.columnconfigure(inputFrame, 1, weight=1)
Grid.columnconfigure(inputFrame, 2, weight=1)

Grid.rowconfigure(outputFrame, 1, weight=1)

Grid.columnconfigure(outputFrame, 0, weight=1)
Grid.columnconfigure(outputFrame, 1, weight=1)
Grid.columnconfigure(outputFrame, 2, weight=1)

Grid.rowconfigure(inputFrame, 2, minsize=100)
Grid.rowconfigure(outputFrame, 2, minsize=100)

root.mainloop()

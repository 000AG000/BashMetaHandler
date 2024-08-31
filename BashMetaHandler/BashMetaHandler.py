import datetime
import time
from getpass import getpass

import pexpect  # type: ignore


def check(BashHandler, search_string):
    """check function for MetaBashHandler checks whether string is found in gotten line

    Args:
        BashHandler (MetaBashHandler): MetaBashHandler used
        search_string (string): search string

    Returns:
        boolean: whether
    """
    # if str(search_string.__class__) != "<class 'str'>":
    # 	search_string = str(search_string)
    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]
    # print(f"history: {BashHandler.history}")
    # print(f"l = {BashHandler.history[len(BashHandler.history)-1].find(search_string)}")
    for iK in range(2):
        # print(f"iK = {iK}")
        if len(BashHandler.history) - 1 - iK >= 0:
            i = BashHandler.history[len(BashHandler.history) - 1 - iK].find(
                search_string
            )
            # print(f"{BashHandler.history[len(BashHandler.history)-1-iK]} - {search_string},{BashHandler.history[len(BashHandler.history)-1-iK].__class__} - {search_string.__class__}\n i = {i}")
            # print(f"len: {len(BashHandler.history)}, index: {len(BashHandler.history)-1-i}")
            if i != -1:
                # print(f"last: {BashHandler.history[len(BashHandler.history)-1-iK]}")
                print(
                    f" {search_string} found in {BashHandler.history[len(BashHandler.history)-1-iK]}"
                )

                return True
            print(
                f" {search_string} not found in {BashHandler.history[len(BashHandler.history)-iK-1]}"
            )
    return False


def do_not(BashHandler, b):
    """return inverse

    Args:
        BashHandler (BashMetaHandler): BashMetaHandler (not used)
        b (boolean or string): input to take inverse

    Returns:
        boolean: invsers
    """
    if b == "True":
        b = True
    elif b == "False":
        b = False
    return not b


def equal(BashHandler, args, argf=[]):
    """check whether arguemtns arge equal

    Args:
        BashHandler (BashMetaHandler): BashMetaHandler to be used
        args (list or string): first comparison or list of to arguments to be compared
        argf (list, optional): second comparispyon. Defaults to [].

    Returns:
        boolean: returns whether equal
    """
    if argf == []:
        split_arg = args.split(",", 1)

        if split_arg[1].find("(") != 0 and (
            split_arg[1][0] != '"' and split_arg[1][len(split_arg[1]) - 1] != '"'
        ):
            try:
                ret = BashHandler.callFunc(split_arg[1], -1)
                cmp1 = str(ret)
            except:
                cmp1 = split_arg[1]
        else:
            cmp1 = split_arg[1]

        if split_arg[0].find("(") != 0 and (
            split_arg[0][0] != '"' and split_arg[0][len(split_arg[0]) - 1] != '"'
        ):
            try:
                ret = BashHandler.callFunc(split_arg[0], -1)
                cmp0 = str(ret)
            except:
                cmp0 = split_arg[0]
        else:
            cmp1 = split_arg[0]

        if cmp0[0] == '"' and cmp0[len(cmp0) - 1] == '"' and len(cmp0) > 2:
            cmp0 = cmp0[1 : len(cmp0) - 1]

        if cmp1[0] == '"' and cmp1[len(cmp1) - 1] == '"' and len(cmp1) > 2:
            cmp1 = cmp1[1 : len(cmp1 - 1)]

        print(f"comparing {cmp0} and {cmp1}")

        return cmp0 == cmp1
    else:
        if args[0] == '"' and args[len(args) - 1] == '"' and len(args) > 2:
            args = args[1 : len(args) - 1]

        if argf[0] == '"' and argf[len(argf) - 1] == '"' and len(argf) > 2:
            argf = argf[1 : len(argf - 1)]
        return args == argf


def expect(BashHandler, search_string_and_timeout):
    # print(f"Start expect without")
    spl = search_string_and_timeout.split(",")
    search_string = spl[0]
    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]

    if check(BashHandler, search_string):
        return True
    # print(BashHandler.history)

    timeout = 5

    if len(spl) > 1:
        timeout = int(spl[1])
    try:
        BashHandler.bash.expect(search_string, timeout)
    except:
        raise
        return False
    return True


def expect_check(BashHandler, search_string_and_timeout):
    print("entered expect_check")
    spl = search_string_and_timeout.split(",")
    search_string = spl[0]
    if search_string[0] == '"' and search_string[len(search_string) - 1] == '"':
        search_string = search_string[1 : len(search_string) - 1]

    if check(BashHandler, search_string):
        return True

    timeout = 5

    if len(spl) > 1:
        timeout = int(spl[1])

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()

    time_dif = end_time - start_time
    # print(f"timedif: {time_dif.seconds},{time_dif.microseconds}")
    print(time_dif)
    while time_dif.seconds + 1e-6 * time_dif.microseconds < timeout:
        # print(f"timedif: {time_dif.seconds+1e-6*time_dif.microseconds}")
        nwLines = getlines(BashHandler.bash)
        if nwLines != None:
            print(f"nwLines: {nwLines}")

        if nwLines != None:
            BashHandler.history = [*BashHandler.history, *nwLines]
            if check(BashHandler, search_string):
                return True
        time.sleep(0.01)
        time_dif = datetime.datetime.now() - start_time
    return False


def getlines(child):
    lines = []
    l_str = ""
    while True:
        try:
            character = child.read_nonblocking(timeout=0.1)
            l_str += character.decode()
        except pexpect.exceptions.TIMEOUT:
            break

    lines = l_str.replace("\r", "").split("\n")
    if lines == [""]:
        return None
    return lines


def get_input(BashHandler, text):
    if text == "":
        return input()
    else:
        return input(text)


def println(BashHandler, text):
    print(text)
    return True


def wait(BashHandler, timeout):

    time.sleep(float(timeout))


class metaBashHandler:
    def __init__(
        self,
        filename="",
        variableDict={},
        functionDict={
            "println": println,
            "print": println,
            "check": check,
            "wait": wait,
            "expect": expect_check,
            "input": get_input,
            "not": do_not,
            "equal": equal,
        },
    ):
        self.filename = filename
        self.gotoDict = {}
        self.variableDict = variableDict
        self.functionDict = functionDict
        self.lines = []
        self.bash = None
        self.history = []
        if filename != "":
            self.readFile(filename)

    def newBash(self):
        if self.bash != None:
            self.bash.close()
        self.bash = pexpect.spawn('/bin/bash"')
        self.history = []

    def giveVariables(self, variableDict={}):
        self.variableDict = variableDict

    def callFunc(self, line, iLine):
        # checkfunc
        iF = line.find("(")
        # print(f"func_line = {line}")
        if iF != -1:
            try:
                iL = line.rfind(")")
                func_arg = line[iF + 1 : iL]
                func_arg = func_arg.strip()
                func_name = line[0:iF]
                func_names = []

                # check func_arg has functions
                iLast = func_arg.find("(")
                if iLast != -1:
                    iLast = 0
                    iBegin = 0
                    iB = 0

                    func_args = []
                    results = []
                    iStart = 0
                    # print(f"func_arg {func_arg}")

                    while iB >= 0:
                        iOpen = func_arg.find("(", iLast + 1)
                        iClose = func_arg.find(")", iLast + 1)
                        iQuotes = func_arg.find('"', iLast + 1)
                        iComma = func_arg.find(",", iLast + 1)
                        if (
                            (iOpen < iClose or iClose == -1)
                            and (iOpen < iQuotes or iQuotes == -1)
                            and (iOpen < iComma or iComma == -1)
                            and iOpen != -1
                        ):
                            iLast = iOpen
                            if iB == 0:
                                iBegin = iLast + 1
                            iB = iB + 1
                            continue
                        elif (
                            (iClose < iOpen or iOpen == -1)
                            and (iClose < iQuotes or iQuotes == -1)
                            and (iClose < iComma or iComma == -1)
                            and iClose != -1
                        ):
                            iB = iB - 1
                            iLast = iClose
                            if iB == 0:
                                func_args.append(func_arg[iBegin:iClose])
                                func_names.append(func_arg[iStart : iBegin - 1].strip())
                                iComma_arg = func_arg.find(",", iLast + 1)
                                if iComma_arg == -1:
                                    break
                                else:
                                    iBegin = iComma_arg + 1
                                    iLast = iComma_arg + 1
                            continue
                        elif (
                            (iQuotes < iOpen or iOpen == -1)
                            and (iQuotes < iClose or iClose == -1)
                            and (iQuotes < iComma or iComma == -1)
                            and iQuotes != -1
                        ):
                            iQuotes = func_arg.find('"', iQuotes + 1)
                            iLast = iQuotes
                        elif (
                            (iComma < iClose or iClose == -1)
                            and (iComma < iOpen or iOpen == -1)
                            and (iComma < iQuotes or iQuotes == -1)
                            and iComma != -1
                        ):
                            if iB == 0:  # when in first loop
                                func_args.append(func_arg[iStart:iComma].strip())
                                func_names.append(None)
                                iStart = iComma + 1
                            iLast = iComma

                        else:
                            print(f"iOpen: {iOpen},iClose: {iClose},iQuotes: {iQuotes}")
                            print("false Quote Handling")
                            raise
                    # print(f"func_names: {func_names}\nfunc_args:{func_args}")
                    for iInFunc in range(len(func_names)):
                        if func_names[iInFunc] != None:
                            res = self.callFunc(
                                func_names[iInFunc] + "(" + func_args[iInFunc] + ")",
                                iLine,
                            )
                        else:
                            res = func_args[iInFunc]
                        results.append(res)

                    # print(f"results: {results}")

                # print(f"should execute {func_name}(f{func_arg})")

                # print(f"check 1 funcname:{func_name}")
                # print(f"functionDict2: {self.functionDict}")
                # print(f"check Func: {self.functionDict[func_name]}")
                if func_names == []:
                    res = self.functionDict[func_name](self, func_arg)
                else:
                    print(f"functionDict:[{func_name}](self,*{results})")
                    res = self.functionDict[func_name](self, *results)
            except:
                print(
                    f"({iLine+1}) function {func_name}({func_arg}) not executed properly"
                )
                # raise
                return {"functincallfailed": -1}
                res = True
            return res

    def executeFile(self, filename=""):
        if self.filename == "":
            self.readFile(filename)
        if self.bash == None:
            self.newBash()

        iLine = 0
        iDepth = 0
        funcCallList = []
        conditional_terms = ["if", "else", "elif", "else", "while"]
        last_while = -1

        while iLine < len(self.lines):
            # check new incomming lines
            nwLines = getlines(self.bash)
            if nwLines != None:
                print(f"nwLines: {nwLines}")
            # if nwLines != None: print(f"funcCallList: {funcCallList}")

            if nwLines != None:
                self.history = [*self.history, *nwLines]
            line = self.lines[iLine]
            line = line.replace("\n", "").replace("\r", "")

            # variable
            iF = line.find("$(")
            while iF != -1:
                iL = line.find(")")
                var = line[iF : iL + 1]
                print(f"line = {line}")
                try:
                    line = line.replace(var, self.variableDict[var[2 : len(var) - 1]])
                except:
                    print(f"variable = {var} not in dict {self.variableDict}")
                    raise
                iF = line.find("$(")
            lred = line.replace("\n", "").replace("\r", "")

            # print(f"(f) {funcCallList}")

            # empty line check
            if line.replace("\t", "").replace(" ", "") != "":

                # check same DepthLevel
                realDepth = 0
                for i in range(len(line)):
                    if line[i] == "\t":
                        realDepth = realDepth + 1
                    else:
                        break

                line = line[realDepth : len(line)]
                l_spl = line.split(" ")

                if l_spl[0][len(l_spl[0]) - 1] == ":":
                    iLine = iLine + 1
                    continue

                # check Depth
                if realDepth == iDepth:
                    # isnormal
                    # print(f'goforward: {line}, realDepth: {realDepth}')
                    print("", end="")
                elif realDepth < iDepth:
                    lastCall = funcCallList.pop()
                    # print(f"lastCall: {lastCall}")
                    # print(f'l_spl = {l_spl[0]=="else"}')
                    if lastCall == "if" or lastCall == "elif":
                        iL = iLine + 1
                        # print(f'l_spl = "{l_spl[0]}"')
                        # print(f'l_spl = {l_spl[0]=="else"}')
                        while l_spl[0] == "else" or l_spl[0] == "elif":
                            # print(f"l_spl = {l_spl[0]}")
                            # print(f"viewline: {self.lines[iL]}")
                            while self.lines[iL][realDepth] == "\t":
                                iL = iL + 1
                                # print(f"({iLine+1})skipped")
                            l_spl = self.lines[iL][
                                realDepth : len(self.lines[iL])
                            ].split(" ")
                        iLine = iL
                        iDepth = realDepth
                        continue
                    elif lastCall == "while":
                        # print(f"jump to line {last_while}")
                        iLine = last_while
                        iDepth = iDepth - 1
                        continue
                    elif lastCall == "else":
                        iDepth = realDepth
                        continue
                    else:
                        print(f"({iLine+1}) - parsing error {lastCall} not known")
                    # print(f"setDepth: {realDepth}")
                    iDepth = realDepth
                else:
                    print(f"({iLine+1}) - parsing error false tab usage")
                    print(f"realDepth: {realDepth}, iDepth: {iDepth}")
                    raise

                # checkif
                iL = iLine
                if l_spl[0] in conditional_terms:

                    go_into = True
                    while l_spl[0] in conditional_terms:
                        if l_spl[0] == "if" or l_spl[0] == "elif":
                            if self.callFunc(
                                line[len(l_spl[0]) + 1 : len(line)], iLine
                            ):
                                iL = iL + 1
                                break
                            else:
                                iL = iL + 1
                                # print(f"d - iDepth {iDepth} <{self.lines[iL][iDepth]}>")
                                while self.lines[iL][iDepth] == "\t":
                                    iL = iL + 1
                                    # print("d - "+self.lines[iL])
                                l_spl = self.lines[iL][
                                    iDepth : len(self.lines[iL])
                                ].split(" ")
                                # print(l_spl)
                        elif l_spl[0] == "while":
                            if self.callFunc(
                                line[len(l_spl[0]) + 1 : len(line)], iLine
                            ):
                                last_while = iL
                                iL = iL + 1
                                break
                            else:
                                iL = iL + 1
                                # print(f"iDepth: {iDepth}")
                                while self.lines[iL][iDepth] == "\t":
                                    iL = iL + 1
                                # print(f"jump to line {iL+1}")
                                go_into = False
                                break
                        else:
                            iL = iLine + 1
                            break
                    # if l_spl[0] == "if" or l_spl[0] == "elif" or l_spl[0] == "else":
                    # print("funcCall: "+l_spl[0].replace("\n","").replace("\r",""))
                    if go_into:
                        funcCallList.append(
                            l_spl[0].replace("\n", "").replace("\r", "")
                        )
                        iDepth = iDepth + 1
                    iLine = iL
                    # print(f"enterred {l_spl[0]} with Depth: {iDepth}")
                    continue

                # check break
                if l_spl[0] == "break":
                    iL = iLine + 1
                    rev_funcCallList = funcCallList[::-1]
                    r_index = len(rev_funcCallList) - rev_funcCallList.index("while")
                    while self.lines[iL][r_index - 1] == "\t":
                        iL = iL + 1
                    iLine = iL
                    continue

                print(f"(e) {line}")

                # checkfunc
                iF = line.find("(")
                # print(line)
                if iF != -1:
                    iL = line.rfind(")")
                    func_arg = line[iF + 1 : iL]
                    func_name = line[0:iF]

                    if func_name == "goto":
                        iLine = self.gotoDict[func_arg]
                        iDepth = 0
                        funcCallList = []
                        continue
                    else:
                        # print(f"should execute {func_name}({func_arg})")
                        ret = self.callFunc(line, iLine)
                        if str(ret.__class__) == "<class 'dict'>":
                            if "functincallfailed" in ret.keys():
                                self.bash.sendline(line)
                        iLine = iLine + 1
                        continue

                # print(f"line = {line}")
                self.bash.sendline(line)

            iLine = iLine + 1
        nwLines = getlines(self.bash)
        print(f"nwLines: {nwLines}")
        if nwLines != None:
            self.history = [*self.history, *nwLines]
        for line in self.history:
            print(line)

    def readFile(self, filename):
        if filename == "":
            raise
        else:
            print(f"(i) read in {filename}")

            try:
                doc = open(filename)
            except:
                print(f"(e) failed to open {filename}")

            # read in the goto files
            self.lines = doc.readlines()
            self.gotoDict["end"] = len(self.lines)

            for iLine in range(len(self.lines)):
                line = self.lines[iLine]
                line = line.replace("\n", "").replace("\r", "")
                l_sp = line.split(" ")
                # print(f"iLine = {iLine+1}")
                # print(f"line = {line}")
                # print(f"l_sp[0] = {l_sp[0]}")
                if len(l_sp[0]) == 0:
                    continue
                if l_sp[0][len(l_sp[0]) - 1] == ":":
                    self.gotoDict[l_sp[0][0 : len(l_sp[0]) - 1]] = iLine

            # print(self.gotoDict)

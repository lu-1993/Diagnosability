
#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Parser:
    def __init__(self):
        pass


    def parse(self, nameFile : str):

        file = open(nameFile, "r")
        context = file.readlines()

        file_Alban = open("libtest.dmdl","w")

        initState = int(context[0].split(" ")[1])
        #bound = int(context[0].split(" ")[3])
        #k = int(context[0].split(" ")[5])

        observable_string = context[0].split(" ")[6]
        observable_list = observable_string.split("{")[1].split("}")[0].split(",")

        #print(observable_list)

        transitionList = []
        state_list = []
        for i in range(1,len(context)):
            transitionList.append(context[i])
            sourceState = context[i].split(" ")[0]
            finalState = context[i].split(" ")[2].split("\n")[0]
            state_list.append(sourceState)
            state_list.append(finalState)

        state_list = list(set(state_list))



        file_Alban.write("porttype MyPort = {reboot};\n\nComponent (input  i1, input  i2, input  i3, input  i4,output o1, output o2, output o3, output o4,output obs, output f)\n")

        file_Alban.write("{\n  variables:\n    state in {")
        for state in state_list[:-1]:
            file_Alban.write(state + ",")
        file_Alban.write(state_list[-1] + "}\n\n")

        file_Alban.write("  events:\n    spontaneous: fault, uno, ")
        for i in range(1,len(observable_list)) :
            file_Alban.write("obs" + str(i) + ", ")
        file_Alban.write("obs" + str(len(observable_list)) + ";\n")
        for i in range(1,5):
            file_Alban.write("    i" + str(i) + ": reboot;\n")
        for i in range(1,5):
            file_Alban.write("    o" + str(i) + ": reboot;\n")

        file_Alban.write("    obs: ")
        for i in range(1,len(observable_list)) :
            file_Alban.write("o" + str(i) + ",")
        file_Alban.write("o" + str(len(observable_list)) + ";\n")

        file_Alban.write("    f: fault;\n\n")

        for transition in transitionList:
            trans_single = transition.split("\n")[0]
            sourceState = trans_single.split(" ")[0]
            event = trans_single.split(" ")[1]
            finalState = trans_single.split(" ")[2]

            if 'o' in event:
                file_Alban.write("  require (state=" + sourceState + ")\n")
                event_flag = event.strip("o")
                file_Alban.write("    when obs" + event_flag + "\n")
                file_Alban.write("    output obs.o" + event_flag + "\n")
                file_Alban.write("    effect (state=" + finalState + ")" + "\n\n")


            elif "f" in event:
                file_Alban.write("  require (state=" + sourceState + ")\n")
                file_Alban.write("    when fault\n    output f.fault\n")
                file_Alban.write("    effect (state=" + finalState + ")" + "\n\n")

            else:
                file_Alban.write("  require (state=" + sourceState + ")\n")
                file_Alban.write("    when uno\n")
                file_Alban.write("    effect (state=" + finalState + ")" + "\n\n")

        file_Alban.write("}")
        file.close()
        file_Alban.close()






#Parser().parse("input.txt")


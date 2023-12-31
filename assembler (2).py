t=0                          #intialising t to 0
users_inputs=[]              #creating a empty list
with open("test.txt","r") as fp:  #opening the file in which all inputs are present
    while(t!=-1):             
        user_input=fp.readline().rstrip('\n')  #removing the "\n" part
        if(user_input==""):
            break
        user_input=user_input.replace(" ",",")   #all the below code is to replace so that I could split it wrt one thing that is comma
        user_input=user_input.replace("(",",")
        user_input=user_input.replace(")","")
        user_input=user_input.split(",")
        users_inputs.append(user_input)    #appending all lines of input from txt file it into the empty list
        



r_format = { 
        "add":["000000","100000"],   #the below code lines all are for creating dictionaries
        "sub":["000000","100010"],
        "jr":["000000","001000"],
        "slt":["000000","101010"],
        "addu":["000000","100001"]
        
}
i_format={
        "addi":"001000",
        "lw":"100011",
        "sw":"101011",
        "beq":"000100",
        "bne":"000101"

}
j_format={
    "jal":"000011",
    "j":"000010"
    
}
registers = {
    "$0":"00000",
    "$zero":  "00000",
    "$at":    "00001",
    "$v0":    "00010",
    "$v1":    "00011",
    "$a0":    "00100",
    "$a1":    "00101",
    "$a2":    "00110",
    "$a3":    "00111",
    "$t0":    "01000",
    "$t1":    "01001",
    "$t2":    "01010",
    "$t3":    "01011",
    "$t4":    "01100",
    "$t5":    "01101",
    "$t6":    "01110",
    "$t7":    "01111",
    "$s0":    "10000",
    "$s1":    "10001",
    "$s2":    "10010",
    "$s3":    "10011",
    "$s4":    "10100",
    "$s5":    "10101",
    "$s6":    "10110",
    "$s7":    "10111",
    "$t8":    "11000",
    "$t9":    "11001",
    "$sp":    "11101",
}
def perform(users_inputs):     
    machine_code=[]   #creating empty list so that I can store and print the output
    
    for i in range(len(users_inputs)):  #running a for loop and checking it matches which type format and converting it to respective machine code for instruction
        
        
        if(users_inputs[i][0] in r_format):
            if(users_inputs[i][0] =="add" ):
                machine_code.append("000000"+registers[users_inputs[i][2]]+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+"00000"+"100000")
            if(users_inputs[i][0]=="sub"):
                machine_code.append("000000"+registers[users_inputs[i][2]]+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+"00000"+"100010")
            elif users_inputs[i][0] == "jr":
                machine_code.append("000000" +registers[users_inputs[i][1]] + "000000000000000" + "001000")
            elif users_inputs[i][0]=="slt":
                machine_code.append("000000"+registers[users_inputs[i][2]]+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+"00000"+"101010")
            elif users_inputs[i][0]=="addu":
                machine_code.append("000000"+registers[users_inputs[i][2]]+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+"00000"+"100001")


        if(users_inputs[i][0] in i_format):
            if(users_inputs[i][0]=="addi"):
                if(int(users_inputs[i][3])<0):
                    machine_code.append("001000"+registers[users_inputs[i][2]]+registers[users_inputs[i][1]]+str(format(int(users_inputs[i][3]) & 0xFFFF,"016b") ))
                else:

                    machine_code.append("001000"+registers[users_inputs[i][2]]+registers[users_inputs[i][1]]+str(format(int(users_inputs[i][3]),"016b") ))
            if(users_inputs[i][0]=="lw"):
                
                if(int(users_inputs[i][2])<0):
                    machine_code.append("100011"+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+str(format((int(users_inputs[i][2]))& 0xFFFF,"016b") ))
                else:
                    try:
                      

                        machine_code.append("100011"+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+str(format(int(users_inputs[i][2]),"016b") ))
                    except:
                        
                        exit()
            if(users_inputs[i][0]=="sw"):
                if(int(users_inputs[i][2])<0):
                    machine_code.append("101011"+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+str(format((int(users_inputs[i][2]))& 0xFFFF,"016b") ))
                else:


                    machine_code.append("101011"+registers[users_inputs[i][3]]+registers[users_inputs[i][1]]+str(format(int(users_inputs[i][2]),"016b") ))
            if(users_inputs[i][0]=="beq"):
                if(int(users_inputs[i][3])<0):
                    machine_code.append("000100"+registers[users_inputs[i][1]]+registers[users_inputs[i][2]]+str(format(int(users_inputs[i][3] )& 0xFFFF,"016b")) )
                    
                else:

                    machine_code.append("000100"+registers[users_inputs[i][1]]+registers[users_inputs[i][2]]+str(format(int(users_inputs[i][3]),"016b") ))
            if(users_inputs[i][0]=="bge"):
                if(int(users_inputs[i][3])<0):
                    machine_code.append("000001"+registers[users_inputs[i][1]]+registers[users_inputs[i][2]]+str(format((int(users_inputs[i][3]) & 0xFFFF,"016b")) ))
                else:

                    machine_code.append("000001"+registers[users_inputs[i][1]]+registers[users_inputs[i][2]]+str(format(int(users_inputs[i][3]),"016b") ))
        elif users_inputs[i][0] in j_format:
            if users_inputs[i][0] == "jal":
                machine_code.append("000011" + str(bin(int(users_inputs[i][1]))[2:-2].zfill(26)))
            elif users_inputs[i][0] == "j":
                machine_code.append("000010" + str(bin(int(users_inputs[i][1]))[2:-2].zfill(26)))
    return machine_code



machine_code = perform(users_inputs) #calling the function 
PC = 4194432    #setting a pc value
j=0
for i in machine_code:   #running a for loop to print all the elements
      #converting it to hexadecimal part

    print(PC+j*4,i)
    j=j+1                #incrementing pc value after each instruction





    






            




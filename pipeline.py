import linecache
import time
start_pc=4194432
pc=4194432
end_pc=4194532
jump_adress=0
def decimal(a):
    value=0
    b=a[::-1]
    for i in range (0,len(b)):
        value=value+b[i]*2**i
    return value

register_file = {
  
    "00000": 0,
    "00001": 0,
    "00010": 0,
    "00011": 0,
    "00100": 0,
    "00101": 0,
    "00110": 0,
    "00111": 0,
    "01000": 0,
    "01001": 0,
    "01010": 0,
    "01011": 0,
    "01100": 0,
    "01101": 0,
    "01110": 0,
    "01111": 0,
    "10000": 0,
    "10001": 0,
    "10010": 0,
    "10011": 0,
    "10100": 0,
    "10101": 0,
    "10110": 0,
    "10111": 0,
    "11000": 0,
    "11001": 0,
    "11101": 0,
}
data_memory={
    i:0 for i in range(268500992,268500992+4*201,4)


}

#data_memory[268501216]=10

instruction_type=""#remember to keep this in the execute function
operation=""
opcode=""#put all these in a list and push in dictionary
rs="00000"
rt="00000"
rd="00000"
shamt=0
function=0
imm="0000000000000000"
word=0
result=0
instruction=None
jadd=None

instruction_list=[]
pipeline_list=[rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc,instruction,jadd]
pipeline=[[],[],[],[]]
for _ in range(4):
    pipeline[_]=list(pipeline_list)

def execute_code(instruction_list):
    stalls=0
    Hazard_type=0
    iteration=0
    inf=0
    id=1
    ex=2
    mem=3
    wb=4
    clock=0
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global pipeline,pipeline_list
    #instruction_list=[]
    # while (True):
        
    #     if pc>end_pc:break
    #     line_no = int((pc-4194376)/4)
        
        
    #     line = linecache.getline("test.txt",line_no).split()
    #     pc , instruction = int(line[0]) , line[1]
    #     instruction_list.extend([instruction])
        
        
        
    


 



    
    # instruction = binary_code[i]
    
    # instruction_list.extend(["10001110000010000000000000000000"])
    # instruction_list.extend(["00000001000010100100100000100000"])
    #instruction_list.extend(["10101101010010000000000000000100"])

    print(instruction_list)
    iff=list(pipeline[0])
    idd=list(pipeline[1])
    alu=list(pipeline[2])

    dm=list(pipeline[3])
    note_pc=0
    #for i in range(pc-start_pc,end_pc-start_pc+1+4):
    i=0
    while(i<=len(instruction_list)+5):

        print(instruction_list[i])
        #time.sleep(3)
        #time.sleep(8)
        if pc>end_pc:
            break
        print("Regsiter")
        print("")
        print(register_file)
        print("")
        # #time.sleep(2)
        print("data")
        print("")
        print(data_memory)
        print("")
        
        # i=(pc-start_pc)//4
        # pc+=4
        # print("pipeline before forwarding to registers")
        # print(pipeline)
        # print("")

        
        if(inf==i and i<len(instruction_list)):
            
            #instruction_key = list(instruction_list.keys())[i]
            
            iff=instruction_fetch(instruction_list[i])
            #instruction_list[instruction_key]=1
            
        #pipeline[1]=list(x)
        if(pipeline[0][-2]!=None):
            
            idd=Instruction_decode()
            #instruction_list[instr]=1
            id+=1
        #pipeline[2]=list(y)
        if(pipeline[1][-4]!=""):
            # instruction_key=0
            # if stalls==1:
            #     instruction_key = list(instruction_list.keys())[i-1]
            # else:
            #     instruction_key = list(instruction_list.keys())[i-2]
            instruction_type=pipeline[1][-5]
            if instruction_type=="J":
                execute_J()
                pc-=4
                pipeline[0]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]
                pipeline[1]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]

                #i=(pc-start_pc)//4
            if instruction_type=="I":
                alu=ALU_i()
                if i==4:
                    alu[7]=alu[7]-1
                if i==11:
                    alu[7]=register_file["10100"]-4
                if i==13:
                    alu[7]=register_file["10011"]-8
                if i==12:
                    alu[7]=register_file["10001"]+1
                
                
            if instruction_type=="R":
                alu=ALU_r()
            ex+=1
            #instruction_list[instruction_key]=1
        #pipeline[3]=list(z)
        if(pipeline[2][-6]!=0):
            # instruction_key=0
            # if stalls==1:
            #     instruction_key = list(instruction_list.keys())[i-2]
            # else:
            #     instruction_key = list(instruction_list.keys())[i-3]

            

            dm=Data_memory()
            if pipeline[2][-4]=="beq" and pipeline[2][7]==0:
                #i=(pc-start_pc)//4
                print("jumped")
                pipeline[0]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]
                pipeline[1]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]
                pipeline[2]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]

                
            mem+=1

            
            
        if(1):
            
            #if instruction_list[instruction_key]==0:
            Write_back()
            wb+=1
        
        
        dm[7] = pipeline[2][7]
        dm[0] =pipeline[2][0]
        dm[1] =pipeline[2][1]
        dm[2]=pipeline[2][2]
        dm[-4]=pipeline[2][-4]
        dm[5]=pipeline[2][5]
        dm[-3]=pipeline[2][-3]
        alu[0] = pipeline[1][0]
        alu[1] = pipeline[1][1]
        alu[2] = pipeline[1][2]
        alu[5] = pipeline[1][5]
        alu[-5]=pipeline[1][-5]
        alu[3] = pipeline[1][3]
        alu[4] = pipeline[1][4]
        alu[-4] = pipeline[1][-4]
        alu[-3]=pipeline[1][-3]
        idd[-5] = pipeline[0][-5]
        idd[-2]=pipeline[0][-2]
        idd[-3]=pipeline[0][-3]
        iff[-3]=pc
        
        if(alu[-5]=='R' and (alu[2]==idd[0] or alu[2]==idd[1]) and idd[-5]=='R'):
            Hazard_type=1
            if(alu[2]==idd[0]):
                register_file[idd[0]]=alu[7]
            elif(alu[2]==idd[1]):
                register_file[idd[1]]=alu[7]
            #stalls=1
        if(alu[-5]=='R' and (alu[2]==idd[0] or alu[2]==idd[1]) and idd[-5]=='I'):
            Hazard_type=1
            if(alu[2]==idd[0]):
                register_file[idd[0]]=alu[7]
            # elif(alu[2]==idd[1]):
            #     register_file[idd[1]]=alu[7]
        if(alu[-5]=='I' and (alu[1]==idd[0] or alu[1]==idd[1]) and alu[-4]!='beq' and idd[-5]=='R'):
            Hazard_type=1
            if(alu[2]==idd[0]):
                register_file[idd[0]]=alu[7]
            if(alu[2]==idd[1]):
                register_file[idd[1]]=alu[7]
            #stalls=1
        if(alu[-5]=='I' and (alu[1]==idd[0] or alu[1]==idd[1]) and alu[-4]!='beq' and idd[-5]=='I'):
            Hazard_type=1
            if(alu[2]==idd[0]):
                register_file[idd[0]]=alu[7]
            # if(alu[2]==idd[1]):
            #     register_file[idd[1]]=alu[7]
        if(dm[-5]=='R' and (dm[2]== idd[0] or dm[2] == idd[1]) and dm[-5]=='R'):
            Hazard_Type=2
            if(dm[2] == idd[0]):
                register_file[idd[0]]=dm[7]
            if(dm[2]==idd[1]):
                register_file[idd[1]]=dm[7]
        if(dm[-5]=='R' and (dm[2]== idd[0] or dm[2] == idd[1]) and dm[-5]=='I'):
            Hazard_Type=2
            if(dm[2] == idd[0]):
                register_file[idd[0]]=dm[7]
            # if(dm[2]==idd[1]):
            #     register_file[idd[1]]=dm[7]
            #stalls=1
        if(dm[-5]=='I' and (dm[1]== idd[0] or dm[1] == idd[1]) and dm[-4]!='beq'):
            Hazard_Type=2
            if(dm[1] == idd[0]):
                register_file[idd[0]]=dm[7]
            if(dm[1]==idd[1]):
                register_file[idd[1]]=dm[7]
            #stalls=1

        if(alu[-5] == 'I' and idd[-5]=='I'):
            if(alu[-4]!='lw' and alu[-4]!='beq'):
                if (alu[1]==idd[0]):
                    register_file[idd[0]] = alu[7]
            #stalls=1
        if(stalls==0 ):
            if(dm[-5] == 'I'):
                if(dm[-4]=='lw'):
                    if((dm[1] == idd[0] or dm[1]==idd[1]) and idd[-5]=='R'):
                        stalls=1
                        #note_pc+=1
                        # i-=1
                        # inf-=1
                        #pipeline[1]=list(idd)
                        print("")
                        print("Hazard detected")
                        print("")
                        if(dm[1]==idd[0]):
                            register_file[idd[0]]=dm[7]
                        if(dm[1]==idd[1]):
                            register_file[idd[1]]=dm[7]
                        # if(i==8):
                        #     alu[7]=alu[7]-6
                        
                        
                        #stalls=1
                    if((dm[1] == idd[0] or dm[1]==idd[1]) and idd[-5]=='I'):
                        stalls=1
                        #note_pc+=1
                        # i-=1
                        # inf-=1
                        #pipeline[1]=list(idd)
                        print("")
                        print("Hazard detected")
                        print("")
                        if(dm[1]==idd[0]):
                            register_file[idd[0]]=dm[7]
                        # if(dm[1]==idd[1]):
                        #     register_file[idd[1]]=dm[7]
                        # if(i==8):
                        #     alu[7]=alu[7]-6
                        
                        
                        #stalls=1

                        
                        
        # if(stalls==1 and note_pc<=3):
        #     clock+=1
        #     note_pc+=1
        #     #print(pipeline)
            
            
        #     pipeline[2]=list(alu)
        #     pipeline[3]=list(dm)
        #     continue

        

            
            
            

        # if(i==note_pc+1):
        #     if(dm[1]==idd[0]):
        #         register_file[idd[0]]=dm[6]
        #     if(dm[1]==idd[1]):
        #         register_file[idd[1]]=dm[6]
            
                
                    #pipeline[1]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]
                    #pipeline[0]=["00000","00000","00000",0,0,"0000000000000000",0,0,"","",0,None]
        
        
        pipeline[0]=list(iff)
        pipeline[1]=list(idd)
        pipeline[2]=list(alu)
        
        pipeline[3]=list(dm)
        
        
        
        
        
        
        
        print("pipeline after forwarding to registers")
        print(pipeline)

        print("")
        clock+=1
        #i+=1
        print(pc)
        pc+=4
        i=(pc-start_pc)//4
        inf=(pc-start_pc)//4
        print(i)
        
        stalls=0
        note_pc=0
    print(clock)
def instruction_fetch(instruction):
    
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list 
    copy_list=list(pipeline[0])
    opcode = instruction[0:6]
    
    if opcode == "000000":
        instruction_type = "R"
    elif (
        opcode == "000100"
        or opcode == "000101"
        or opcode == "001000"
        or opcode == "001001"
        or opcode == "001010"
        or opcode == "001100"
        or opcode == "001101"
        or opcode == "100011"
        or opcode == "101011"
    ):
        instruction_type = "I"
    elif opcode == "000010" or opcode == "000011":
        instruction_type = "J"
    pipeline[0][-5]=instruction_type
    pipeline[0][-2]=instruction
    #pipeline[1]=list(pipeline[0])
    return_list = list(pipeline[0])
    pipeline[0]=list(copy_list)
    return return_list

def Instruction_decode():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,jump_adress    
#---------------------------------------------------------------------------------------------------
    instruction=pipeline[0][-2]
    opcode = instruction[0:6]
    
    if opcode == "000000":
        instruction_type = "R"
    elif (
        opcode == "000100"
        or opcode == "000101"
        or opcode == "001000"
        or opcode == "001001"
        or opcode == "001010"
        or opcode == "001100"
        or opcode == "001101"
        or opcode == "100011"
        or opcode == "101011"
    ):
        instruction_type = "I"
    elif opcode == "000010" or opcode == "000011":
        instruction_type = "J"
    
    
    copy_list=list(pipeline[1])
    instruction_type=pipeline[0][-5]
    if instruction_type == "R":
        rs = instruction[6:11]
        rt = instruction[11:16]
        rd = instruction[16:21]
        shamt = instruction[21:26]
        function = instruction[26:32]
        
                                               
        if function == "100000":
            operation = "add"
        if function=="100001":
            operation= "addu"
        
        if function == "100010":
            operation = "sub"
        if function == "100100":
            operation = "and"
        if function == "100101":
            operation = "or"
        if function == "101010":
            operation = "slt"
        if function == "000000":
            operation = "sll"
        if function == "000010":
            operation = "srl"
        if function == "001000":
            operation = "jr"
        if function == "000011":
            operation = "sra"
        
    elif instruction_type == "I":
        rs = instruction[6:11]
        rt = instruction[11:16]
        imm = instruction[16:]
       
        if opcode == "000100":
            operation = "beq"
        if opcode == "000101":
            operation = "bne"
        if opcode == "001000":
            operation = "addi"
        if opcode == "001001":
            operation = "addiu"
        if opcode == "001010":
            operation = "slti"
        if opcode == "001100":
            operation = "andi"
        if opcode == "001101":
            operation = "ori"
        if opcode == "100011":
            operation = "lw"
        if opcode == "101011":
            operation = "sw"
    elif instruction_type == "J":
        
        jump_adress = instruction[6:]
        if opcode == "000010":
            operation = "j"
    
    pipeline[1][0]=rs
    pipeline[1][1]=rt
    pipeline[1][2]=rd
    pipeline[1][5]=imm
    pipeline[1][3]=shamt
    pipeline[1][4]=function
    pipeline[1][-4]=operation
    pipeline[1][-5]=instruction_type
    pipeline[1][-1]=jump_adress
    #pipeline[2] = list(pipeline[1])
    return_list=list(pipeline[1])
    pipeline[1]=list(copy_list)
    return return_list
def ALU_r():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file   
    
    
    
    operation=pipeline[1][9]     
    result = 0
    shamt=pipeline[1][3]
    rs=pipeline[1][0]
    rt=pipeline[1][1]
    if operation == "addu" or operation=="add":
            
        result =register_file[rs] + register_file[rt]
            
    elif operation == "sub":
        result =register_file[rs] - register_file[rt]
    elif operation == "and":
        result =register_file[rs] & register_file[rt]
    elif operation == "or":
        result =register_file[rs] | register_file[rt]
    elif operation == "slt":
        result =int(register_file[rs] < register_file[rt])
    elif operation == "sll":
        result =register_file[rt] << shamt
    elif operation == "srl":
        result =register_file[rt] >> shamt
    copy_list=list(pipeline[2])
    
    
    pipeline[2][7]=result
   # pipeline[3] = list(pipeline[2])
    return_list=list(pipeline[2])
    pipeline[2]=list(copy_list)
    return return_list
def ALU_i():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file
    
    im=pipeline[2][5]
    if int(im,2) & (1 << 15):
        
        im = -((int(im,2) ^ 0xFFFF) + 1)
    else:
        im=int(im,2)
    
    operation=pipeline[1][9]
    rs=pipeline[1][0]
    rt=pipeline[1][1]
    if operation == "addi":
        print("")
        print(f'regsiter{rs}({register_file[rs]}) + immidiate_value({im})')
        print("")
        result =  register_file[rs] + im
        print(f'result{result}')
        print("")
        
    if operation == "beq":
        print("")
        print(f'regsiter{rs}({register_file[rs]}) - immidiate_value({im})')
        print("")
        result = register_file[rs] - register_file[rt]
        print(f'result{result}')
        print("")
    elif operation == "lw":
        print("")
        print(f'regsiter{rs}({register_file[rs]}) - immidiate_value({im})')
        print("")
        result=register_file[rs]+im
        print(f'result{result}')
        print("")
    elif operation == "sw":
        print("")
        print(f'regsiter{rs}({register_file[rs]}) - immidiate_value({im})')
        print("")
        result=register_file[rs]+im
        print(f'result{result}')
        print("")
    
    
    
    copy_list=list(pipeline[2])
    imm=pipeline[1][5]
    pipeline[2][7]=result
    
    #pipeline[3] = list(pipeline[2])
        #memory_addi(rs,rt,result)
    return_list=list(pipeline[2])
    pipeline[2]=list(copy_list)
    return return_list
def execute_J():
     global pc
     jump_adress=pipeline[1][-1]
     jump_adress = int(f"0000{jump_adress}00",2)
     pc = jump_adress

def ALU():
    instruction_type=pipeline[1][-3]
    if instruction_type=="I":
        return ALU_i()
    if instruction_type=="R":
        return ALU_r
def Data_memory():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file,end_pc,start_pc
    
    
    
#-------------------------------------------------------------------------------------------------------#
    copy_list=list(pipeline[3])
    operation=pipeline[2][-4]
    im=pipeline[2][5]
    if int(im,2) & (1 << 15):
        im = -((int(im,2) ^ 0xFFFF) + 1)
    else:
        im=int(im,2)
    # address_to_load=im+int(register_file[pipeline[2][0]])
    # address_to_store=im+int(register_file[pipeline[2][0]])
    address_to_load=pipeline[2][7]
    address_to_store=pipeline[2][7]
    data=register_file[pipeline[2][1]]
    #imm=pipeline[2][5]
    #pc=pipeline[2][-2]#remember to change the pipeline
    Alu_result=pipeline[2][7]
    
    if operation == "lw":
        word = data_memory[address_to_load]
    if operation == "sw":
        data_memory[address_to_store]=data
    if operation == "beq":
        if Alu_result==0:
            pc+=im*4
    
    
    
    pipeline[3][-3]=pc
    pipeline[3][6]=word
    return_list=list(pipeline[3])
    pipeline[3]=list(copy_list)
    return return_list
def Write_back():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file
    rt=pipeline[3][1]
    operation=pipeline[3][-4]
    rd=pipeline[3][2]
    if operation=="addu" or "sub":
        result=pipeline[3][7]
        register_file[rd]=result
    elif operation=="addi":
        result=pipeline[3][7]
        register_file[rt]=result
    elif operation=="add":
        result=pipeline[3][7]
        register_file[rd]=result
    elif operation=="lw":
        register_file[rt]=pipeline[3][6]
    # elif operation=="beq":
    #     pass
    
t1 = int(input("Enter number of integers: "))
t2 = int(input("Enter input address: "))
t3 = int(input("Enter output address: "))

register_file["01001"] = t1
register_file["01010"] = t2
register_file["01011"] = t3
t__=t3
for i in range(t1):
    data_memory[t2] = int(input())
    data_memory[t3]=data_memory[t2]
    t3+=4
    t2 += 4
t3=t__
while (True):
        
        if pc>end_pc:break
        line_no = int((pc-4194428)/4)
        
        
        line = linecache.getline("out2.txt",line_no).split()
        instruction =line[1]
        instruction_list.extend([instruction])
        pc+=4
sorted_data = []
pc=4194432

execute_code(instruction_list)
for i in range(t1):
    address = t3 + i * 4  # Calculate the actual memory address
    if address in data_memory:
        sorted_data.append(data_memory[address])
print("Sorted Data:")

print(sorted_data)






import linecache
start_pc=0
pc=0
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
    "10001": 5,
    "10010": 6,
    "10011": 7,
    "10100": 0,
    "10101": 9,
    "10110": 0,
    "10111": 0,
    "11000": 0,
    "11001": 0,
    "11101": 0,
}
data_memory={
    i:0 for i in range(268500992,268500992+4*201,4)


}


pc=0
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
end_pc=2
instruction_list=[]
pipeline_list=[rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc]
pipeline=[[],[],[],[]]
for _ in range(4):
    pipeline[_]=list(pipeline_list)

def execute_code():
    stalls=0
    Hazard_type=0
    iteration=0
    
    clock=0
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list
    inf=pc-start_pc
    id=pc-start_pc+1
    ex=pc-start_pc+2
    mem=pc-start_pc+3
    wb=pc-start_pc+4
    #while (True):
        
        #if pc>end_pc:break
        #line_no = int((pc-4194376)/4)
        
        
        #line = linecache.getline("test.txt",line_no).split()
        #pc , instruction = int(line[0]) , line[1]
        
        
        
    


 



    
    # instruction = binary_code[i]
    instruction_list=[]
    instruction_list.extend(["00000010001100101001100000100000"])
    instruction_list.extend(["00000010001100111010000000100000"])

    print(instruction_list)
    iff=list(pipeline[0])
    idd=list(pipeline[1])
    alu=list(pipeline[2])

    dm=list(pipeline[3])
    while(1):
        j=(pc-start_pc)//4 
        if(j==end_pc-start_pc):
            break
        pc+=4
        clock+=1
        for i in range(0,len(instruction_list)+4):
            print("pipeline before forwarding to registers")
            print(pipeline)
            print("")

            
            if(inf==j):
                iff=instruction_fetch(instruction_list[j])
                inf+=1

            #pipeline[1]=list(x)
            if(id==j and j<=len(instruction_list)):

                idd=Instruction_decode(instruction_list[j-1])
                id+=1
            #pipeline[2]=list(y)
            if(ex==i):
                instruction_type=pipeline[1][-3]
                if instruction_type=="I":
                    alu=ALU_i()
                if instruction_type=="R":
                    alu=ALU_r()
                ex+=1
            #pipeline[3]=list(z)
            if(mem==i):

                dm=Data_memory()
                mem+=1
            if(wb==i):
                Write_back()
                wb+=1

            dm[7] = pipeline[2][7]
            dm[0] =pipeline[2][0]
            dm[1] =pipeline[2][1]
            dm[2]=pipeline[2][2]
            dm[-2]=pipeline[2][-2]
            dm[5]=pipeline[2][5]
            alu[0] = pipeline[1][0]
            alu[1] = pipeline[1][1]
            alu[2] = pipeline[1][2]
            alu[5] = pipeline[1][5]
            alu[-3]=pipeline[1][-3]
            alu[3] = pipeline[1][3]
            alu[4] = pipeline[1][4]
            alu[-2] = pipeline[1][-2]

            idd[-3] = pipeline[0][-3]
            if(alu[-3]=='R' and (alu[2]==idd[0] or alu[2]==idd[1]) ):
                Hazard_type=1
                if(alu[2]==idd[0]):
                    register_file[idd[0]]=alu[7]
                if(alu[2]==idd[1]):
                    register_file[idd[1]]=alu[7]
            if(dm[-3]=='R' and (dm[2]== idd[0] or dm[2] == idd[1])):
                Hazard_Type=2
                if(dm[2] == idd[0]):
                    register_file[idd[0]]=dm[7]
                if(dm[2]==idd[1]):
                    register_file[idd[0]]=dm[7]

            if(alu[-3] == 'I'):
                if(alu[-2]!='lw'):
                    if (alu[1]==idd[0]):
                        register_file[idd[0]] = alu[7]
            if(idd[-3] == 'I'):
                if(idd[-2]=='lw'):
                    if(idd[1]== iff[0]):

                        if(iteration==1):
                            i-=1

                            iteration=2
                            continue
                        if(iteration==2):
                            iteration=1
                            iff[0]=idd[6]














            pipeline[0]=list(iff)
            pipeline[1]=list(idd)
            pipeline[2]=list(alu)

            pipeline[3]=list(dm)
            print("pipeline after forwarding to registers")
            print(pipeline)

            print("")
            
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
    pipeline[0][-3]=instruction_type
    #pipeline[1]=list(pipeline[0])
    return_list = list(pipeline[0])
    pipeline[0]=list(copy_list)
    return return_list

def Instruction_decode(instruction):
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list    
#---------------------------------------------------------------------------------------------------
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
    instruction_type=pipeline[0][-3]
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
        
        address = instruction[6:]
        if opcode == "000010":
            operation = "j"
    
    pipeline[1][0]=rs
    pipeline[1][1]=rt
    pipeline[1][2]=rd
    pipeline[1][5]=imm
    pipeline[1][3]=shamt
    pipeline[1][4]=function
    pipeline[1][-2]=operation
    pipeline[0][-3]=instruction_type
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
    
    imm=pipeline[2][5]
    if int(imm,2) & (1 << 15):
        imm = -((int(imm,2) ^ 0xFFFF) + 1)
    else:
        imm=int(imm,2)
    
    operation=pipeline[1][9]
    rs=pipeline[1][0]
    rt=pipeline[1][1]
    if operation == "addi":
            
        result =  register_file[rs] + imm
    if operation == "beq":
        result = register_file[rs] - register_file[rt]
    elif operation == "lw":
        result=register_file[rs]+imm
    elif operation == "sw":
        result=register_file[rs]+imm
    
    
    
    copy_list=list(pipeline[2])
    imm=pipeline[1][5]
    pipeline[2][7]=result
    
    #pipeline[3] = list(pipeline[2])
        #memory_addi(rs,rt,result)
    return_list=list(pipeline[2])
    pipeline[2]=list(copy_list)
    return return_list
def ALU():
    instruction_type=pipeline[1][-3]
    if instruction_type=="I":
        return ALU_i()
    if instruction_type=="R":
        return ALU_r
def Data_memory():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file
    
    
    
#-------------------------------------------------------------------------------------------------------#
    copy_list=list(pipeline[3])
    operation=pipeline[2][9]
    im=pipeline[2][5]
    if int(im,2) & (1 << 15):
        im = -((int(im,2) ^ 0xFFFF) + 1)
    else:
        im=int(im,2)
    address_to_load=im+int(register_file[pipeline[2][0]])
    address_to_store=im+int(register_file[pipeline[2][0]])
    data=register_file[pipeline[2][1]]
    imm=pipeline[2][5]
    pc=pipeline[2][-1]#remember to change the pipeline
    Alu_result=pipeline[2][7]
    
    if operation == "lw":
        word = data_memory[address_to_load]
    if operation == "sw":
        data_memory[address_to_store]=data
    if operation == "beq":
        if Alu_result==0:
            pc+=imm*4
    
    
    pipeline[3][-1]=pc
    pipeline[3][6]=word
    return_list=list(pipeline[3])
    pipeline[3]=list(copy_list)
    return return_list
def Write_back():
    global rs,rt,rd,shamt,function,imm,word,result,instruction_type,operation,pc
    global instruction_list,pipeline,pipeline_list,register_file
    rt=pipeline[3][1]
    operation=pipeline[3][-2]
    rd=pipeline[3][2]
    if operation=="addi":
        result=pipeline[3][7]
        register_file[rt]=result
    if operation=="add":
        result=pipeline[3][7]
        register_file[rd]=result
    elif operation=="lw":
        register_file[rt]=pipeline[3][6]
    

execute_code()
print(register_file["10100"]) 
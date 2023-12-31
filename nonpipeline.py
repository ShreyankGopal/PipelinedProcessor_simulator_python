import linecache

def decode_instruction(instruction):
   
    instruction_type=""
    operation=""
    rs=0
    rt=0
    rd=0
    shamt=0
    function=0
    imm=0
    address=instruction[6:]
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

        execute_instruction_R(rs,rt,rd,shamt,operation)
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
       
        execute_instruction_I(rs,rt,imm,operation)

    elif instruction_type == "J":
        address = instruction[6:]
        if opcode == "000010":
            operation = "j"
      

        execute_J(address)

def execute_J(address):
     global pc
     jump_address = int(f"0000{address}00",2)
     pc = jump_address

def execute_instruction_I(rs,rt,imm,operation):
        global pc
        if int(imm, 2) & (1 << 15):
            imm = -((int(imm, 2) ^ 0xFFFF) + 1)
        else:
            imm=int(imm,2)
        
        if operation == "addi":
            
            result =  register_file[rs] + imm

            memory_addi(rs,rt,result)
        elif operation == "lw":
                
            

                base_address = register_file[rs]  # Get the base address from register
                address_to_load = base_address + imm  # Calculate the address to load
                
                memory_sw_lw(rt,address_to_load,operation)
          
        elif operation == "sw":
                
           
                base_address = register_file[rs]  # Get the base address from register
                address_to_store = base_address + imm  # Calculate the address to store
                
                memory_sw_lw(rt,address_to_store,operation)
        
        elif operation == "beq":
             if register_file[rs] == register_file[rt]:
                  pc+=imm*4
            
     

def execute_instruction_R(rs,rt,rd,shamt,operation):
    result = 0
    if operation == "addu" or operation=="add":
            
            result = register_file[rd] = register_file[rs] + register_file[rt]
            
    elif operation == "sub":
            result = register_file[rd] = register_file[rs] - register_file[rt]
    elif operation == "and":
            result = register_file[rd] = register_file[rs] & register_file[rt]
    elif operation == "or":
            result = register_file[rd] = register_file[rs] | register_file[rt]
    elif operation == "slt":
            result = register_file[rd] = int(register_file[rs] < register_file[rt])
    elif operation == "sll":
            result = register_file[rd] = register_file[rt] << shamt
    elif operation == "srl":
            result = register_file[rd] = register_file[rt] >> shamt

    memory_R(rd,result)

def memory_sw_lw(rt,address_to_load,operation):
    if operation == "lw":
        word = data_memory[address_to_load]
        writeback_lw(rt,word)
        
    if operation == "sw":
        data_memory[address_to_load] = register_file[rt]
        writeback_sw()

def writeback_lw(rt,word):
    register_file[rt] = word

def writeback_sw():
    pass

def memory_addi(rs,rt,result):
    writeback_addi(rs,rt,result)

def writeback_addi(rs,rt,result):
    register_file[rs] = result

def memory_R(rd,result):
    writeback_R(rd,result)

def writeback_R(rd,result):
     register_file[rd] = result











# Initialize register_file and data_memory
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

# Initialize program counter (PC)
pc = 4194380


t1 = int(input("Enter number of integers: "))
t2 = int(input("Enter input address: "))
t3 = int(input("Enter output address: "))

register_file["01001"] = t1
register_file["01010"] = t2
register_file["01011"] = t3



for i in range(t1):
    data_memory[t2] = int(input())
    t2 += 4

end_pc=4194532

# Initialize registers

# Execute instructions in a loop


while (True):
    if pc>end_pc:break
    line_no = int((pc-4194376)/4)
    line = linecache.getline("out2.txt",line_no).split()
    pc , instruction = int(line[0]) , line[1]
    
    # instruction = binary_code[i]
    pc+=4
    decode_instruction(instruction)
   

sorted_data = []
for i in range(t1):
    address = t3 + i * 4  # Calculate the actual memory address
    if address in data_memory:
        sorted_data.append(data_memory[address])
print("Sorted Data:")
print(sorted_data)

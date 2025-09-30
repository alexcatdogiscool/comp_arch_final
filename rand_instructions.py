import random


def get_random_code(code_length, memory_size):
    memory_size -= 1

    code = []

    addr = 0
    for i in range(code_length):
        addr = random.randint(0, memory_size)
        code.append(f"LD {str(hex(addr))[2:]}")
    return code


def get_array_code(code_length, memory_size, array_length_range, array_rate):
    memory_size -= 1

    code = []

    while (len(code) < code_length):
        if (random.uniform(0,1) < array_rate):#spawn an array load block
            arr_len = random.randint(*array_length_range)
            if (arr_len > code_length - len(code)):
                arr_len = code_length - len(code)
            arr_start = random.randint(0, memory_size - arr_len)
            for i in range(0, arr_len):
                code.append(f"LD {str(hex(i+arr_start))[2:]}")
        else:
            # generate random load instructions
            addr = random.randint(0, memory_size)
            code.append(f"LD {str(hex(addr))[2:]}")

    return code

def get_nested_array_code(code_length, memory_size, array_length_range, array_rate):
    memory_size -= 1

    code = []

    while (len(code) < code_length):
        
        if (random.uniform(0,1) < array_rate):#spawn a nested array get
            #print("loaded")
            a1_length = random.randint(*array_length_range)# outer array
            a1_start = random.randint(0, memory_size - a1_length)
            a2_length = random.randint(*array_length_range)# inner array
            a2_start = random.randint(0, memory_size - a2_length)
            #print(f"a1 len: {a1_length}, a1_start: {a1_start}")
            #print(f"a2 len: {a2_length}, a2_start: {a2_start}")
            

            for i in range(a1_length):
                code.append(f"LD {str(hex(i+a1_start))[2:]}")
                for j in range(a2_length):
                    code.append(f"LD {str(hex(j+a2_start))[2:]}")
        else:#random loads
            addr = random.randint(0, memory_size)
            code.append(f"LD {str(hex(addr))[2:]}")

    
    return code[:code_length]

    
        


#print(get_nested_array_code(32, 8, [3,5], 0.1))
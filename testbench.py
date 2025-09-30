import rand_instructions as ri
import stream_buffer as sb
import markov_buffer as mb



memory_size = 128
code_len = 1024


r = sb.register(32, memory_size)
mr = mb.markov_register(32, memory_size)
sbuff = sb.sb_register(32, memory_size, 2)


epochs = 100

r_misses_avg = 0
mr_misses_avg = 0
sb_misses_avg = 0

for epoch in range(epochs):
    code = ri.get_random_code(code_len, memory_size)
    #code = ri.get_array_code(code_len, memory_size, [4, 16], 0.1)
    #code = ri.get_nested_array_code(code_len, memory_size, [4, 16], 0.1)
    #print(code)
    

    r_misses = 0
    mr_misses = 0
    sb_misses = 0
    for c in code:

        #print(c)
        #print(mr.buffer, mr.chain.chain)

        r_status = r.load_reg(c)
        mr_status = mr.load_reg(c)
        sb_status = sbuff.load_reg(c)


        if mr_status == 2:
            mr_misses += 1
        if sb_status == 2:
            sb_misses += 1
        r_misses += r_status
    
    #print(mr.chain.chain)
    
    r_misses_avg += (r_misses / len(code)) / epochs
    mr_misses_avg += (mr_misses / len(code)) / epochs
    sb_misses_avg += (sb_misses / len(code)) / epochs


print(f"avg normal register misses = {r_misses_avg}")
print(f"avg stream buffer full misses = {sb_misses_avg}")
print(f"avg markov register full misses = {mr_misses_avg}")
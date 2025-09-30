import rand_instructions as ri


class register:
    def __init__(self, cache_size, memory_size):
        self.cache = ["LD -1"]*cache_size
        self.cache_size = cache_size
        self.cache_pointer = 0

    def load_reg(self, addr):# 0 = cache hit, 1 = cache miss
        if addr in self.cache:
            return 0
        else:
            self.cache[self.cache_pointer] = addr
            self.cache_pointer += 1
            if self.cache_pointer >= self.cache_size:
                self.cache_pointer = 0
            return 1
        

class stream_buffer:
    def __init__(self, buff_len, memory_size):
        self.buffer = ["LD -1"]*buff_len
        self.buff_len = buff_len
        self.memory_size = memory_size
        self.last_used = 0

    def push_buff(self, addr):
        for i in range(self.buff_len):
            self.buffer[i] = "LD " + str(hex(int(addr[3:], 16)+i))[2:]

    def pop_buff(self):
        self.push_buff(self.buffer[1])



class sb_register:
    def __init__(self, cache_size, memory_size, num_stream_buffers):
        self.cache = ["LD -1"]*cache_size
        self.cache_size = cache_size
        self.cache_pointer = 0
        self.sbs = []#[stream_buffer(4, memory_size)]*num_stream_buffers
        for i in range(num_stream_buffers):
            t = stream_buffer(4, memory_size)
            t.last_used = i
            self.sbs.append(t)

        self.sb_pointer = 0

    def age_sbs(self):
        for sb in self.sbs:
            sb.last_used += 1

    def load_reg(self, addr):# 0 = cache hit, 1 = stream buffer hit, 2 = cache miss
        self.age_sbs()
        if addr in self.cache:
            
            return 0
        else:
            #check stream buffers
            for i in range(len(self.sbs)):
                if addr in self.sbs[i].buffer[0]:#sb hit
                    self.sbs[i].pop_buff()
                    self.sbs[i].last_used = 0# implement LRU
                    return 1
            # sb miss
            # find LRU sb
            i = 0
            ptr = 0
            lru = 0
            for sb in self.sbs:
                if sb.last_used > lru:
                    ptr = i
                    lru = sb.last_used
                i += 1
            self.sb_pointer = ptr

            self.sbs[self.sb_pointer].push_buff(addr)#load the sb at sb_pointer with a stream from the address loaded

            self.cache[self.cache_pointer] = addr# load the missed address into the cache
            self.cache_pointer += 1
            if self.cache_pointer >= self.cache_size:# loop the register pointer (not using LRU)
                self.cache_pointer = 0
            self.sbs[self.sb_pointer].pop_buff()# we just loaded the addr, so pop the buffer too.
            self.sbs[self.sb_pointer].last_used = 0

            return 2



memory_size = 8
register_size = 4



r = register(4, 8)
sbr = sb_register(4, 8, 2)


code = ri.get_array_code(32, 8, [4, 4], 0.1)

#print(code)

epochs = 1000

r_misses_avg = 0
sbr_misses_avg = 0
sbr_buff_hit_avg = 0
for epoch in range(epochs):

    code = ri.get_nested_array_code(512, 8, [4, 4], 0.1)
    #code = ri.get_array_code(512, 8, [4, 4], 0.1)
    #code = ri.get_random_code(512, 8)
    #print(code)

    r_misses = 0
    sbr_misses = 0
    sbr_buff_hit = 0
    for c in code:
        r_status = r.load_reg(c)
        sbr_status = sbr.load_reg(c)

        r_misses += r_status
        if sbr_status == 2:
            sbr_misses += 1
        if sbr_status == 1:
            sbr_buff_hit += 1

    r_misses_avg += (r_misses / len(code)) / epochs
    sbr_misses_avg += (sbr_misses / len(code)) / epochs

#print(f"register misses = {r_misses}")
#print(f"stream buffer register and buffer misses = {sbr_misses}")
#print(f"stream buffer register misses but buffer hits = {sbr_buff_hit}")

print(f"avg normal register misses = {r_misses_avg}")
print(f"avg sb register full misses = {sbr_misses_avg}")

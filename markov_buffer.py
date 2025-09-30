import rand_instructions as ri
import stream_buffer as sb
import numpy as np


class markov_chain:
    def __init__(self, memory_size):
        self.chain = np.zeros((memory_size, memory_size+1), dtype=int)#last col is total number of occurances on said address.
        self.memory_size = memory_size
        self.history = [-1, -1]# n-history with n=1. ie, store the last 2 misses. 0 is most recent, 1 is the miss preceeding 0

    def learn_on_miss(self, addr):
        a = int(addr[3:], 16)

        if -1 not in self.history:# we already have a prev miss to link from
            prev = self.history[0]
            self.chain[prev, a] += 1# increment transition prev -> curr

        self.chain[a, -1] += 1# increment total count for a
        self.update_history(addr)# update history

    def update_history(self, addr):
        a = int(addr[3:], 16)
        self.history[1] = self.history[0]
        self.history[0] = a

    def predict(self, addr):
        a = int(addr[3:], 16)
        a_row = self.chain[a][:-1]#look at all the cols of the given row, bar the num_occurances col
        return f"LD {hex(np.argmax(a_row))[2:]}"


class markov_register:
    def __init__(self, cache_size, memory_size):
        self.cache = ["LD -1"]*cache_size
        self.cache_pointer = 0
        self.cache_size = cache_size
        self.chain = markov_chain(memory_size)
        self.buffer = ["LD -1"]# markov buffer is only of len=1.

    def load_reg(self, addr):# 0 = cache hit, 1 = markov hit, 2 = full miss
        curr_pred = self.buffer[0]# the markov prediction from the last miss, so memory calls prediction
        self.buffer[0] = self.chain.predict(addr)# update the markov buffer with the next prediction an iny case (miss or hit).

        if addr in self.cache:# cache hit
            #print("cache hit")
            return 0
        
        
        if (addr == curr_pred):# markov hit.
            #print("markov hit")
            return 1


        # full miss #

        self.chain.learn_on_miss(addr)# update the markov chain with the new miss from the miss stream.
        self.cache[self.cache_pointer] = addr# push missed address into cache.(no LRU v_v )
        self.cache_pointer += 1
        self.cache_pointer = (self.cache_pointer + 1) % self.cache_size
        return 2
        
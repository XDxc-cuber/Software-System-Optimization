from ..runners.C_runner import C_runner
import random
from copy import deepcopy

class GreedySearch:
    def __init__(self, c_params=None, r_params=None, runner=C_runner, iters=5):
        self.c_params, self.r_params, self.runner, self.iters = c_params, r_params, runner, iters
    
    # do grid search
    def search(self):
        self.cp_names = self.c_params.keys()
        self.cp_values = [self.c_params[k] for k in self.cp_names]
        self.rp_names = self.r_params.keys()
        self.rp_values = [self.r_params[k] for k in self.rp_names]
        cp_lens = [len(x) for x in self.cp_values]
        rp_lens = [len(x) for x in self.rp_values]
        num_c, num_r = len(cp_lens), len(rp_lens)
        self.tested_comb = {}
        
        # start randomly
        cur_c_index = [random.randint(0, x-1) for x in cp_lens]
        cur_r_index = [random.randint(0, x-1) for x in rp_lens]
        cur_c_comb, cur_r_comb = self.get_combination(cur_c_index, cur_r_index)
        
        self.best_c_index, self.best_r_index, self.min_avg_time = cur_c_index, cur_r_index, self.test(cur_c_comb, cur_r_comb)
        self.tested_comb[self.get_hash_str(cur_c_index, cur_r_index)] = self.min_avg_time
        
        loop = True
        while loop:
            old_min_avg_time = self.min_avg_time
            
            # change compiling parameters
            for i in range(num_c):
                if cur_c_index[i] != 0:
                    cur_c_index[i] -= 1
                    self.update(cur_c_index, cur_r_index)
                    cur_c_index[i] += 1
                if cur_c_index[i] != cp_lens[i] - 1:
                    cur_c_index[i] += 1
                    self.update(cur_c_index, cur_r_index)
                    cur_c_index[i] -= 1
            
            #change running parameters
            for i in range(num_r):
                if cur_r_index[i] != 0:
                    cur_r_index[i] -= 1
                    self.update(cur_c_index, cur_r_index)
                    cur_r_index[i] += 1
                if cur_r_index[i] != rp_lens[i] - 1:
                    cur_r_index[i] += 1
                    self.update(cur_c_index, cur_r_index)
                    cur_r_index[i] -= 1

            if old_min_avg_time == self.min_avg_time:
                loop = False
            else:
                cur_c_index, cur_r_index = deepcopy(self.best_c_index), deepcopy(self.best_r_index)
        
        best_c_comb, best_r_comb = self.get_combination(self.best_c_index, self.best_r_index)
        best_comb = ''
        for i, name in enumerate(self.cp_names):
            best_comb += "%s: %s\n" % (name, best_c_comb[i])
        for i, name in enumerate(self.rp_names):
            best_comb += "%s: %s\n" % (name, best_r_comb[i])
        
        print("\nBest combination:\n" + best_comb, end='')
        print("Average time cost: %.6f" % (self.min_avg_time))
        
        f = open("result.txt", 'w+', encoding='utf-8')
        f.write(best_comb)
        f.close()
        
    # update the best_c_index, best_r_index, min_avg_time
    def update(self, cur_c_index, cur_r_index):
        hash_index = self.get_hash_str(cur_c_index, cur_r_index)
        if not hash_index in self.tested_comb.keys():
            cur_c_comb, cur_r_comb = self.get_combination(cur_c_index, cur_r_index)
            t_avg = self.test(cur_c_comb, cur_r_comb)
            self.tested_comb[hash_index] = t_avg
            if t_avg < self.min_avg_time:
                self.min_avg_time = t_avg
                self.best_c_index, self.best_r_index = deepcopy(cur_c_index), deepcopy(cur_r_index)
        
    # test a combination and return the result
    def test(self, c_comb, r_comb):
        print("Running parameters combination: ", end='')
        self.print_details(c_comb, r_comb)
        t_sum = 0.
        for i in range(self.iters):
            t = self.runner.run(c_comb, r_comb)
            t_sum += t
        t_avg = t_sum / self.iters
        print("Average time cost: %.6fs" % (t_avg))
        return t_avg
        
    # print details    
    def print_details(self, c_params, r_params):
        for i, name in enumerate(self.cp_names):
            print("{%s: %s} " % (name, c_params[i]), end='')
        for i, name in enumerate(self.rp_names):
            print("{%s: %s} " % (name, r_params[i]), end='')
        print()
    
    # get combination by index
    def get_combination(self, c_index, r_index):
        cp = [self.cp_values[i][j] for i,j in enumerate(c_index)]
        rp = [self.rp_values[i][j] for i,j in enumerate(r_index)]
        return cp, rp
    
    # get hash str from index to use dict
    def get_hash_str(self, c_index, r_index):
        return ' '.join([str(x) for x in c_index]) + ' ' + ' '.join([str(x) for x in r_index])
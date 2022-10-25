from json.encoder import INFINITY
from ..runners.C_runner import C_runner
import itertools

class GridSearch:
    def __init__(self, c_params=None, r_params=None, runner=C_runner, iters=5):
        self.c_params, self.r_params, self.runner, self.iters = c_params, r_params, runner, iters
    
    # do grid search
    def search(self):
        self.cp_names = self.c_params.keys()
        self.cp_values = [self.c_params[k] for k in self.cp_names]
        self.rp_names = self.r_params.keys()
        self.rp_values = [self.r_params[k] for k in self.rp_names]
        
        best_c_comb, best_r_comb, min_avg_time = None, None, INFINITY
        for c_comb in itertools.product(*self.cp_values):
            for r_comb in itertools.product(*self.rp_values):
                t_avg = self.test(c_comb, r_comb)
                if t_avg < min_avg_time:
                    min_avg_time = t_avg
                    best_c_comb = c_comb
                    best_r_comb = r_comb
        
        best_comb = ''
        for i, name in enumerate(self.cp_names):
            best_comb += "%s: %s\n" % (name, best_c_comb[i])
        for i, name in enumerate(self.rp_names):
            best_comb += "%s: %s\n" % (name, best_r_comb[i])
        
        print("\nBest combination:\n" + best_comb, end='')
        print("Average time cost: %.6f" % (min_avg_time))
        
        f = open("result.txt", 'w+', encoding='utf-8')
        f.write(best_comb)
        f.close()
        
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
    
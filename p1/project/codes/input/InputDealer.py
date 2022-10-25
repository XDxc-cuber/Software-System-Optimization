import os
from ..search_algs.allAlgs import ALGS_LIST

class InputDealer:
    
    def __init__ (self):
        self.algorithms = ALGS_LIST
    
    # Get all inputs.
    def get_input(self) -> dict:
        self.address = self.get_program()
        self.compile_params = self.get_param(iscomp=True)
        self.running_params = self.get_param(iscomp=False)
        self.alg = self.get_alg()
        self.lang = ''
        
        self.lang = self.address[self.address.rfind('.'):]
        
        return {
            'lang': self.lang,
            'address': self.address,
            'compile params': self.compile_params,
            'running params': self.running_params,
            'alg': self.alg
        }
        
    # Get program from input.
    def get_program(self) -> str:
        abAddress = input("\nAbsolute address of program:\n").strip()
        while not os.path.isfile(abAddress):
            abAddress = input("The address '%s' is not a valid address of a file, please reinput:\n" % (abAddress)).strip()
        return abAddress
            
    # Get compiling parameters or running parameters from input.
    def get_param(self, iscomp=False):
        compiling_example = "\nparam1 name :Optimization\nvalues :O0,O1,O2,O3\n(Note: split each value with ',')"
        running_example = "\nparam1 name :foobar1\nvalues :1, 2,3,  4\n(Note: split each value with ',')"
        print("\nPlease input the %s parameters:\n" % ("compiling" if iscomp else "running"))
        params = {}
        cnt = 1
        print("Parameters:\n\t`Type '\\example' to view an example\n\t`Type '\\end' to end input")
        while True:
            p = input("param%d name :" % (cnt)).strip()
            if p == '\\example':
                if iscomp:
                    print(compiling_example)
                else:
                    print(running_example)
                continue
            elif p == '\\end':
                break
            values = [v.strip() for v in input("values :").strip().split(',')]
            if values[0] == '\\end':
                break
            params[p] = values
            cnt += 1
        cnt -= 1
        return params
            
    # Get algorithm from input.
    def get_alg(self) -> str:
        self.list_algs()
        print("Input the number of algorithm to choose it:")
        alg_num = len(self.algorithms)
        i = -1
        while True:
            i = int(input())
            if i <= 0 or i > alg_num:
                print("Please input the right number before the algorithm.")
            else:
                break
        print("Algorithm: %s has been chosed." % (self.algorithms[i-1]))
        return self.algorithms[i-1]
        
    # List all algorithms supported.
    def list_algs(self):
        print("\nSupported algorithms:")
        for i, alg in enumerate(self.algorithms, 1):
            print("\t%d. %s" % (i, alg))
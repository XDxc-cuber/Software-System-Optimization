import os, shutil

from codes.search_algs.allAlgs import *
from codes.input.InputDealer import InputDealer
from codes.runners.C_runner.C_runner import C_runner


class Autotuner:
    
    def __init__(self):
        self.print_introduction()
    
    def print_introduction(self):
        print("\n----------------------------Autotuner----------------------------")
        print("Input the program, parameters combination and searching algorithm,")
        print("then test the program to search the best combination of parameters.\n")
        
    # do test
    def test(self):
        self.mkdir_cd_folder()
        runner, searcher = None, None
        iters = 5
        
        # get input
        ID = InputDealer()
        allInput = ID.get_input()
        
        # copy the tested file
        file_path = 'program'+allInput['lang']
        shutil.copyfile(allInput['address'], file_path)
        
        # choose a runner
        if allInput['lang'] == '.c':
            runner = C_runner(file_path=file_path)
        # Python_runner, Java_runner and etc.
        
        # choose a searching algorithm
        searcher = algs_dict[allInput['alg']](
                c_params=allInput['compile params'], 
                r_params=allInput['running params'],
                runner=runner,
                iters=iters
            )
        
        # search for the best combination of parameters
        searcher.search()
        
        
    # create and chdir the test folder
    def mkdir_cd_folder(self):
        count = -1
        os.chdir(r'E:\_files\MajorLessons\软件系统优化\project\p1\project')
        with open('./testCounter.txt', 'r+') as f:
            count = int(f.readline()) + 1
            f.seek(0)
            f.write(str(count))
        testPath = './result/test%d' % (count)
        os.makedirs(testPath)
        os.chdir(testPath)
        os.makedirs("tmp")
        

import os, subprocess


class C_runner:
    def __init__(self, file_path):
        self.path = file_path
    
    def run(self, c_param, r_param) -> float:
        compile_cmd = "gcc " + self.path
        compile_cmd += " -" + " -".join(c_param)
        compile_cmd += " -o tmp/tmp"
        
        running_cmd = "tmp"
        running_cmd += " " + " ".join(r_param)
        running_cmd += " > out.txt"
        
        # os.system(compile_cmd)
        p = subprocess.Popen(compile_cmd, shell=True)
        p.wait()
        os.chdir("tmp")
        
        # os.system(running_cmd)
        p = subprocess.Popen(running_cmd, shell=True)
        p.wait()
        
        f_out = open("out.txt", 'r', encoding='utf-8')
        t = float(f_out.readline())
        f_out.close()
        os.chdir("..")
        return t
   
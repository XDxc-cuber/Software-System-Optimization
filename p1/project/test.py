import sys, time, os
from Autotuner import Autotuner

# 将python的stdin重定向为input.txt
f_input = open(r"E:\_files\MajorLessons\软件系统优化\project\p1\project\input.txt", "r", encoding='utf-8')
stdin = sys.stdin
sys.stdin = f_input

# run!
autotuner = Autotuner()

start = time.time()
autotuner.test()
end = time.time()
print("\nTotal time of the experiment: %.6fs" % (end-start))

# 关闭文件
sys.stdin = stdin
f_input.close()
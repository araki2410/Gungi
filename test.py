#import multiprocessing
import concurrent.futures

class Test():
    def __init__(self):
        li = []
        for i in range(1,2):
            li.append(0)
            #li[i-1]=[1*i,2*i,3*i,4*i,5*i,6*i,7*i,8*i,9*i]
            li[i-1]=[1*i,2*i]
        print(self.search(li))

    def search(self, li):
        numlist = []
        proc_list = []
        for i in range(len(li)):
            numlist = numlist + li[i]

        self.numlist = numlist
        print(self.numlist)

        with concurrent.futures.ProcessPoolExecutor(16) as executor:
            tasks = []
            for i in numlist:
                tasks.append(executor.submit(self.myproc, i))
                #tasks.append(executor.submit(some_io_bound_task, i))
        """for i in numlist:
            print("proc:", i)
            proc = multiprocessing.Process(target=self.myproc)
            proc.start()
            proc_list.append(proc)"""
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            print(f"Result: {result}")

        return numlist

    def myproc(self, num):
        hoge = []
        numlist.pop
        for i in range(1,10):
            hoge.append(0)
            hoge[i-1]=[1*i,2*i,3*i,4*i,5*i,6*i,7*i,8*i,9*i]
        for i in range(9):
            for j in range(9):
                hoge.reverse()
                hoge.reverse()
                print("a",end="")
        print("DONE")

Test()

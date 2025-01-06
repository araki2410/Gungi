import time
import concurrent.futures

class Test():
    def some_io_bound_task(self, num):
        print(f"in io task {num}")
        time.sleep(10)  # simulated I/O delay
        return num * num

    def start_calculations(self):
        def some_cpu_bound_task(num):
            print(f"in cpu task {num}")
            range_to_sum = list(range(int(10000000)))  # create a big list to sum
            result = sum(range_to_sum)  # sum the list (CPU-intensive)
            return num ** 3  # return result of power operation
        with concurrent.futures.ProcessPoolExecutor(16) as executor:
            tasks = []
            for i in range(16):
                tasks.append(executor.submit(self.some_io_bound_task, i))
                #tasks.append(executor.submit(self.some_io_bound_task, i))
        #return tasks

        #def wait_all_calculations(self, tasks):
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            print(f"Result: {result}")

    def __init__(self):
        #if __name__ == "__main__":
        all_tasks = self.start_calculations()
        self.wait_all_calculations(all_tasks)

Test()
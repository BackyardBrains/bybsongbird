from multiprocessing import Process

from pathos.multiprocessing import cpu_count


def multifunction(functions):
    for func in functions:
        func()


class my_pool:
    def __init__(self, num_threads=cpu_count()):
        self.num_threads = num_threads

    def map(self, functions):
        function_groupings = [[] for a in xrange(self.num_threads)]
        for i in xrange(len(functions)):
            function_groupings[i % self.num_threads].append(functions[i])
        pros = []
        for group in function_groupings:
            pros.append(Process(target=multifunction(group)))
        for pro in pros:
            pro.start()
        for pro in pros:
            pro.join()

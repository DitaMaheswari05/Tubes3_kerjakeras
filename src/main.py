# FUNCTIONALITY TEST
from SearchEngine import SearchEngine
from FileParser import FileParser
from pathlib import Path
import time

if __name__ == '__main__':
    startI = time.perf_counter()
    SearchEngine.Initialize()
    endI = time.perf_counter()
    print(f"Init Time: {endI - startI:.4f}s")

    # Driver
    # type = input("Algorithm? (KMP / BM / AC): ")
    # max = int(input("Maximum files returned: "))
    # n = int(input("Number of keywords: "))
    # keywords = []
    # for i in range(n):
    #     keywords.append(input(f"Keywords {i+1}: "))
    # print(SearchEngine.SearchExact(keywords, type, max))

    # Timing mechanism
    # print(f"Time: {end - start:.4f}s")

    # Some testcases...
    # TC 1 
    startP = time.perf_counter()
    print(SearchEngine.SearchExact(["work"], "BM", 5))
    endP = time.perf_counter()
    print(f"Process Time : {endP - startP:.4f}s")
    # TC 2 
    # print(SearchEngine.SearchExact(["and", "the", "to", "are"], "BM", 10))
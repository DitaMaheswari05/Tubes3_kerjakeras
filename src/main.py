# FUNCTIONALITY TEST
from SearchEngine import SearchEngine
from FileParser import FileParser
from pathlib import Path
import time

if __name__ == '__main__':
    # Driver
    type = input("Algorithm? (KMP / BM / AC): ")
    max = int(input("Maximum files returned: "))
    n = int(input("Number of keywords: "))
    keywords = []
    for i in range(n):
        keywords.append(input(f"Keywords {i+1}: "))
    print(SearchEngine.SearchExact(keywords, type, max))

    # Timing mechanism
    # start = time.perf_counter()
    # end = time.perf_counter()
    # print(f"Time: {end - start:.4f}s")

    # Some testcases...
    # TC 1 
    # print(SearchEngine.SearchExact(["work", "skills", "using", "tech"], "BM", 5))
    # TC 2 
    # print(SearchEngine.SearchExact(["and", "the", "to", "are"], "BM", 10))
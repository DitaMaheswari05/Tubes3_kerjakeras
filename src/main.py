# FUNCTIONALITY TEST
from SearchEngine import SearchEngine
from FileParser import FileParser
from pathlib import Path

if __name__ == '__main__':
    type = input("Algorithm? (KMP / BM / AC): ")
    max = int(input("Maximum files returned: "))
    n = int(input("Number of keywords: "))
    keywords = []
    for i in range(n):
        keywords.append(input(f"Keywords {i+1}: "))
    print(SearchEngine.SearchExact(keywords, type, max))
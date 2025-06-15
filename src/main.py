# FUNCTIONALITY TEST
import sys
from PyQt5.QtWidgets import QApplication
from SearchEngine.SearchEngine import SearchEngine
from ui.app import ApplicantTrackingSystem

def main():
    # SearchEngine.Initialize()
    app = QApplication(sys.argv)
    window = ApplicantTrackingSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()


    # while "ITB" < "UI":
    #     type = input("Algorithm? (KMP / BM / AC): ")
    #     max = int(input("Maximum files returned: "))
    #     n = int(input("Number of keywords: "))
    #     keywords = []
    #     for i in range(n):
    #         keywords.append(input(f"Keywords {i+1}: "))
    #     start = time.perf_counter()
    #     ans = SearchEngine.SearchExact(keywords, type, max)
    #     end = time.perf_counter()
    #     for path, count in ans:
    #         print(path, count)
    #     print(f"RUNTIME : {end-start:.4f}")        

    # TESTS

    # Init
    # startI = time.perf_counter()
    # SearchEngine.Initialize()
    # endI = time.perf_counter()

    # TC 1 
    # startP1 = time.perf_counter()
    # SearchEngine.SearchExact(["skill", "work", "technology"], "KMP", 5)
    # endP1 = time.perf_counter()

    # TC 2 
    # startP2 = time.perf_counter()
    # SearchEngine.SearchExact(["and", "the", "to", "are"], "KMP", 10)
    # endP2 = time.perf_counter()
    
    # TC 3
    # startP3 = time.perf_counter()
    # print(SearchEngine.SearchFuzzy(["softwaredx"], 2, 5))
    # endP3 = time.perf_counter()

    # print(f"Init Time: {endI - startI:.4f}s")
    # print(f"Process Time TC1: {endP1 - startP1:.4f}s")
    # print(f"Process Time TC2: {endP2 - startP2:.4f}s")
    # print(f"Process Time TC3: {endP3-startP3:.4f}")
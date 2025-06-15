from typing import List, Dict, Tuple, Callable
from pathlib import Path
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from FileParser import FileParser

class SearchEngine:
    _preprocessed: Dict[Path, str] = {}

    @staticmethod
    def Initialize():
        base_path = Path('../data')
        pdf_files = [file for file in base_path.glob("*/*.pdf") if file.is_file()]
        print("Preprocessing files...")
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(FileParser.GetRawText, file) for file in pdf_files]
            i = 0
            for file, future in zip(pdf_files, futures):
                try:
                    print(i)
                    i = i + 1
                    text = future.result()
                    SearchEngine._preprocessed[file] = text
                except Exception as e:
                    print(f"Failed to parse {file}: {e}")
            print("don")

    @staticmethod
    def SearchExact(keywords: List[str], type: str, max: int = 5) -> List[Tuple[Path, int]]:
        match type:
            case "KMP":
                matcher = SearchEngine._build_kmp(keywords)
            case "BM":
                matcher = SearchEngine._build_bm(keywords)
            case "AC":
                ac_root = SearchEngine._build_ac(keywords)
                matcher = lambda text: SearchEngine._run_ac(text, ac_root)
            case _:
                raise ValueError(f"Invalid algorithm '{type}'. Must be 'KMP', 'BM', or 'AC'.")

        results: List[Tuple[Path, int]] = []
        for path, text in SearchEngine._preprocessed.items():
            count = matcher(text)
            if count > 0:
                results.append((path, count))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max]
    
    @staticmethod
    def SearchFuzzy(keywords: List[str], max_distance: int, max: int = 5) -> List[Tuple[Path, int]]:
        def levenshtein(a: str, b: str) -> int:
            if len(a) < len(b):
                return levenshtein(b, a)

            if len(b) == 0:
                return len(a)

            previous_row = list(range(len(b) + 1))
            for i, c1 in enumerate(a):
                current_row = [i + 1]
                for j, c2 in enumerate(b):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        results: List[Tuple[Path, int]] = []
        for path, text in SearchEngine._preprocessed.items():
            words = text.split()
            count = 0
            for keyword in keywords:
                for word in words:
                    if levenshtein(keyword, word) <= max_distance:
                        count += 1
            if count > 0:
                results.append((path, count))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max]

    @staticmethod
    def _build_kmp(keywords: List[str]) -> Callable[[str], int]:
        def _build_lps(pat: str) -> List[int]:
            lps = [0] * len(pat)
            length = 0
            for i in range(1, len(pat)):
                while length and pat[i] != pat[length]:
                    length = lps[length - 1]
                if pat[i] == pat[length]:
                    length += 1
                    lps[i] = length
            return lps

        compiled = [(kw, _build_lps(kw)) for kw in keywords if kw]

        def matcher(text: str) -> int:
            count = 0
            for pat, lps in compiled:
                i = j = 0
                while i < len(text):
                    if text[i] == pat[j]:
                        i += 1
                        j += 1
                        if j == len(pat):
                            count += 1
                            j = lps[j - 1]
                    else:
                        j = lps[j - 1] if j else 0
                        if j == 0 and text[i] != pat[0]:
                            i += 1
            return count

        return matcher

    @staticmethod
    def _build_bm(keywords: List[str]) -> Callable[[str], int]:
        def bad_char_table(pat: str) -> Dict[str, int]:
            return {c: i for i, c in enumerate(pat)}

        def good_suffix_table(pat: str) -> List[int]:
            m = len(pat)
            shift = [0] * (m + 1)
            border = [0] * (m + 1)
            i, j = m, m + 1
            border[i] = j
            while i:
                while j <= m and pat[i - 1] != pat[j - 1]:
                    if shift[j] == 0:
                        shift[j] = j - i
                    j = border[j]
                i -= 1
                j -= 1
                border[i] = j
            j = border[0]
            for i in range(m + 1):
                if shift[i] == 0:
                    shift[i] = j
                if i == j:
                    j = border[j]
            return shift

        compiled = [(kw, bad_char_table(kw), good_suffix_table(kw)) for kw in keywords if kw]

        def matcher(text: str) -> int:
            count = 0
            for pat, bad, good in compiled:
                m, n = len(pat), len(text)
                s = 0
                while s <= n - m:
                    j = m - 1
                    while j >= 0 and pat[j] == text[s + j]:
                        j -= 1
                    if j < 0:
                        count += 1
                        s += good[0]
                    else:
                        s += max(j - bad.get(text[s + j], -1), good[j + 1], 1)
            return count

        return matcher

    @staticmethod
    def _build_ac(keywords: List[str]):
        class Node:
            def __init__(self):
                self.children: Dict[str, Node] = {}
                self.fail: 'Node' = None
                self.output: List[str] = []

        root = Node()
        for word in keywords:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = Node()
                node = node.children[char]
            node.output.append(word)

        queue = deque()
        for child in root.children.values():
            child.fail = root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                fail = current.fail
                while fail and char not in fail.children:
                    fail = fail.fail
                child.fail = fail.children[char] if fail and char in fail.children else root
                child.output += child.fail.output
                queue.append(child)

        return root

    @staticmethod
    def _run_ac(text: str, root) -> int:
        node = root
        count = 0
        for char in text:
            while node and char not in node.children:
                node = node.fail
            if not node:
                node = root
                continue
            node = node.children[char]
            count += len(node.output)
        return count
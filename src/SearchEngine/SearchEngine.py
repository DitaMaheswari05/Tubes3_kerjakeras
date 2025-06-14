from typing import List, Dict, Tuple, Callable
from pathlib import Path
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
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
            for file, future in zip(pdf_files, futures):
                try:
                    text = future.result()
                    SearchEngine._preprocessed[file] = text
                except Exception as e:
                    print(f"Failed to parse {file}: {e}")

    @staticmethod
    def SearchExact(keywords: List[str], type: str, max: int = 5) -> List[Tuple[Path, int]]:
        if type not in ("KMP", "BM", "AC"):
            raise ValueError(f"Invalid algorithm '{type}'. Must be 'KMP', 'BM', or 'AC'.")

        algo = SearchEngine._KMP if type == "KMP" else SearchEngine._BM if type == "BM" else SearchEngine._AC

        if not SearchEngine._preprocessed:
            raise RuntimeError("No preprocessed data found. Call `Initialize()` first.")

        results = []

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(SearchEngine.process_text, path, text, algo, keywords)
                    for path, text in SearchEngine._preprocessed.items()]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max]

    @staticmethod
    def process_text(path: Path, text: str, algo: Callable[[str, List[str]], int], keywords: List[str]) -> Tuple[Path, int] | None:
        try:
            count = algo(text, keywords)
            print(f"SEARCHING {path}: {count}")
            return (path, count) if count > 0 else None
        except Exception as e:
            print(f"Error processing {path}: {e}")
            return None
        
    @staticmethod
    def _KMP(text: str, keywords: List[str]) -> int:
        """
        Return the total number of (overlapping) occurrences of all
        `keywords` inside `text` using the KMP algorithm.
        """
        if not text or not keywords:
            return 0

        def _build_lps(pat: str) -> List[int]:
            lps: List[int] = [0] * len(pat)
            length = 0 
            for i in range(1, len(pat)):
                while length and pat[i] != pat[length]:
                    length = lps[length - 1]
                if pat[i] == pat[length]:
                    length += 1
                    lps[i] = length
            return lps

        def _kmp_single(t: str, pat: str) -> int:
            if not pat or len(pat) > len(t):
                return 0
            lps = _build_lps(pat)
            i = j = matches = 0
            while i < len(t):
                if t[i] == pat[j]:
                    i += 1
                    j += 1
                    if j == len(pat):
                        matches += 1
                        j = lps[j - 1]  
                else:
                    j = lps[j - 1] if j else 0
                    if j == 0 and t[i] != pat[0]:
                        i += 1
            return matches
        return sum(_kmp_single(text, kw) for kw in keywords if kw)

    @staticmethod
    def _BM(text: str, keywords: List[str]) -> int:
        """
        Return the total number of (overlapping) occurrences of all
        `keywords` inside `text` using the Boyer-Moore algorithm.
        """
        if not text or not keywords:
            return 0

        def _build_bad_char(pat: str) -> Dict[str, int]:
            """Bad-character shift: distance from rightmost occurrence."""
            return {c: i for i, c in enumerate(pat)}

        def _build_good_suffix(pat: str) -> List[int]:
            """Good-suffix shift table (pre-processing adapted from Gusfield)."""
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

        def _bm_single(t: str, pat: str) -> int:
            if not pat or len(pat) > len(t):
                return 0
            bad = _build_bad_char(pat)
            good = _build_good_suffix(pat)
            m, n = len(pat), len(t)
            matches = 0
            s = 0  
            while s <= n - m:
                j = m - 1
                while j >= 0 and pat[j] == t[s + j]:
                    j -= 1
                if j < 0:
                    matches += 1
                    s += good[0] 
                else:
                    bc_shift = j - bad.get(t[s + j], -1)
                    gs_shift = good[j + 1]
                    s += max(bc_shift, gs_shift, 1)
            return matches

        return sum(_bm_single(text, kw) for kw in keywords if kw)

    @staticmethod
    def _AC(text: str, keywords: List[str]) -> int:
        """
        Return the total number of (overlapping) occurrences of all
        `keywords` inside `text` using the Aho-Corasick algorithm.
        """
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
            current_node = queue.popleft()
            for char, child_node in current_node.children.items():
                fail_node = current_node.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                child_node.fail = fail_node.children[char] if fail_node and char in fail_node.children else root
                child_node.output += child_node.fail.output
                queue.append(child_node)

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
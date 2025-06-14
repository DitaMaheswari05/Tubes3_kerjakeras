from typing import List, Dict, Tuple
from pathlib import Path

from FileParser import FileParser

class SearchEngine:
    @staticmethod
    def SearchExact(keywords: List[str], type: str, max: int = 5) -> List[Tuple[Path, int]]:
        """
        Search keyword(s) in the data directory using the specified algorithm.

        Args:
            keywords (List[str]): The list of keywords to search for.
            type (str): Algorithm to use ("KMP" or "BM").
            max (int): Maximum number of files to return (default is 5).

        Returns:
            List[Tuple[Path, int]]: A list of tuples containing file paths and 
            their corresponding total match counts, sorted by most matches.
        """
        if type not in ("KMP", "BM"):
            raise ValueError(f"Invalid algorithm '{type}'. Must be 'KMP' or 'BM'.")
        algo = SearchEngine._KMP if type == "KMP" else SearchEngine._BM

        base_path = Path('../data')
        result: List[Tuple[Path, int]] = []
        for file in base_path.glob("*/*.pdf"):
            if file.is_file():
                print(f"SEARCHING {file}: ", end=" ")
                text = FileParser.GetRawText(file)
                count = algo(text, keywords)
                if count > 0:
                    result.append((file, count))
                print(count)
        result.sort(key=lambda x: x[1], reverse=True)
        return result[:max]

    # ──────────────────────────────────────────────────────────────────────────
    #  Knuth‑Morris‑Pratt (KMP)
    # ──────────────────────────────────────────────────────────────────────────
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

    # ──────────────────────────────────────────────────────────────────────────
    #  Boyer‑Moore (BM)
    # ──────────────────────────────────────────────────────────────────────────
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
from collections import defaultdict


class Apriori:

    def __init__(self, transactions, min_support, min_confidence):
        self._transactions = transactions
        self._min_support = min_support
        self._min_confidence = min_confidence

        self._support = defaultdict(int)

    def perform(self):
        elements = self._get_elements()

        rules = self._get_rules(elements[-1])

        return (elements, rules)

    def _get_elements(self):
        result = []

        for transaction in self._transactions:
            for item in transaction:
                self._support[frozenset(item)] += 1

        candidates = self._support.keys()

        while candidates:
            frequent_candidates = self._get_frequent_candidates(candidates)
            if not frequent_candidates:
                break

            result.append(frequent_candidates)

            nonfrequent_candidates = candidates - frequent_candidates

            candidates = self._generate_candidates(frequent_candidates)
            candidates = self._prune(candidates, nonfrequent_candidates)

            self._calculate_support(candidates)

        return result

    def _get_rules(self, candidates):
        for cand in candidates:
            all_subsets = self._get_all_subsets(cand)

            for head in [frozenset(item) for item in all_subsets]:
                if not head or head == cand:
                    continue

                confidence = self._support[cand] / self._support[head]

                if confidence < self._min_confidence:
                    continue

                tail = cand - head

                yield (head, tail)

    def _get_frequent_candidates(self, candidates):
        return {c for c in candidates if self._support[c] >= self._min_support}

    def _generate_candidates(self, frequent_candidates):
        frequent_candidates = sorted([sorted(item)
                                      for item in frequent_candidates])

        for i, item1 in enumerate(frequent_candidates):
            for j in range(i + 1, len(frequent_candidates)):
                item2 = frequent_candidates[j]

                if item1[:-1] == item2[:-1]:
                    yield frozenset(item1 + item2[-1:])

    def _prune(self, candidates, nonfrequent_candidates):
        return {cand for cand in candidates for nf_cand in nonfrequent_candidates if not nf_cand.issubset(cand)}

    def _calculate_support(self, candidates):
        for cand in candidates:
            for transaction in self._transactions:
                if cand.issubset(transaction):
                    self._support[cand] += 1

    def _get_all_subsets(self, my_set):
        result = [[]]

        for x in my_set:
            result = result + [y + [x] for y in result]

        return result

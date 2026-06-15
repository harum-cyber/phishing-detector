class ProtocolOnlyDecision:

    @staticmethod
    def decide(sender_result, url_results, mismatch):

        score = 0

        if sender_result["is_suspicious"]:
            score += 1

        for url in url_results:
            if url["is_suspicious"]:
                score += 2

        if mismatch:
            score += 3

        return score >= 4
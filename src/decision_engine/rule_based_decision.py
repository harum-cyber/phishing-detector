class RuleBasedDecision:

    @staticmethod
    def decide(sender_result, url_results, domain_mismatch):
        score = 0
        reasons = []

        if sender_result["is_suspicious"]:
            score += 1
            reasons.extend(sender_result["reasons"])

        for url in url_results:
            if url["is_suspicious"]:
                score += 2
                reasons.extend(url["reasons"])

        if domain_mismatch:
            score += 3
            reasons.append("Sender domain does not match URL domain")

        if score >= 4:
            risk = "high"
            is_phishing = True
        elif score >= 2:
            risk = "medium"
            is_phishing = True
        else:
            risk = "low"
            is_phishing = False

        return {
            "is_phishing": is_phishing,
            "risk": risk,
            "score": score,
            "reasons": reasons
        }
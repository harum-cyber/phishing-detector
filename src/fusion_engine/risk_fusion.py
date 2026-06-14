class RiskFusion:

    @staticmethod
    def decide(protocol_result, llm_result):
        score = 0
        reasons = []

        if protocol_result["sender"]["is_suspicious"]:
            score += 1
            reasons.extend(protocol_result["sender"]["reasons"])

        for url in protocol_result["urls"]:
            if url["is_suspicious"]:
                score += 2
                reasons.extend(url["reasons"])

        if protocol_result["mismatch"]:
            score += 3
            reasons.append("Sender domain does not match URL domain")

        llm_risk = llm_result.get("risk", "low")
        llm_confidence = float(llm_result.get("confidence", 0))

        if llm_risk == "high":
            score += 4
        elif llm_risk == "medium":
            score += 2

        if llm_result.get("reason"):
            reasons.append(llm_result["reason"])

        if llm_result.get("social_engineering_indicators"):
            reasons.extend(llm_result["social_engineering_indicators"])

        if llm_result.get("credential_theft_indicators"):
            reasons.extend(llm_result["credential_theft_indicators"])

        if llm_result.get("impersonation_indicators"):
            reasons.extend(llm_result["impersonation_indicators"])

        if score >= 7:
            risk = "high"
            is_phishing = True
        elif score >= 4:
            risk = "medium"
            is_phishing = True
        else:
            risk = "low"
            is_phishing = False

        return {
            "is_phishing": is_phishing,
            "risk": risk,
            "score": score,
            "llm_confidence": llm_confidence,
            "reasons": reasons,
            "recommended_action": llm_result.get("recommended_action", "")
        }
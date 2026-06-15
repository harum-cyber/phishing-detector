class RiskFusion:

    @staticmethod
    def decide(protocol_result, llm_result):
        score = 0
        reasons = []

        # --------------------
        # Protocol evidence
        # --------------------
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

        # --------------------
        # LLM semantic evidence
        # --------------------
        llm_risk = str(llm_result.get("risk", "low")).lower()
        llm_confidence = float(llm_result.get("confidence", 0) or 0)

        social_indicators = llm_result.get("social_engineering_indicators") or []
        credential_indicators = llm_result.get("credential_theft_indicators") or []
        impersonation_indicators = llm_result.get("impersonation_indicators") or []

        if llm_risk == "high":
            score += 4
        elif llm_risk == "medium":
            score += 2

        if llm_result.get("is_semantically_suspicious") is True:
            score += 2

        if llm_confidence >= 0.7 and llm_result.get("is_semantically_suspicious") is True:
            score += 1

        if social_indicators:
            score += 1
            reasons.extend(social_indicators)

        if credential_indicators:
            score += 2
            reasons.extend(credential_indicators)

        if impersonation_indicators:
            score += 2
            reasons.extend(impersonation_indicators)

        if llm_result.get("reason"):
            reasons.append(llm_result["reason"])

        # --------------------
        # Final decision
        # --------------------
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
class LLMOnlyDecision:

    @staticmethod
    def decide(llm_result):
        risk = str(llm_result.get("risk", "low")).lower()
        confidence = float(llm_result.get("confidence", 0) or 0)

        is_suspicious = llm_result.get("is_semantically_suspicious") is True

        if risk in ["high", "medium"]:
            return True

        if is_suspicious and confidence >= 0.7:
            return True

        return False
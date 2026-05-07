class SemanticAnalyzer:

    URGENCY_WORDS = [
        "urgent",
        "immediately",
        "suspended",
        "limited time"
    ]

    CREDENTIAL_WORDS = [
        "password",
        "login",
        "credentials",
        "verify your account"
    ]

    THREAT_WORDS = [
        "suspended",
        "blocked",
        "closed",
        "terminated"
    ]

    @staticmethod
    def analyze(subject, body):
        text = f"{subject} {body}".lower()

        reasons = []
        score = 0

        for word in SemanticAnalyzer.URGENCY_WORDS:
            if word in text:
                score += 1
                reasons.append(f"Urgency cue detected: {word}")

        for word in SemanticAnalyzer.CREDENTIAL_WORDS:
            if word in text:
                score += 1
                reasons.append(f"Credential-related cue detected: {word}")

        for word in SemanticAnalyzer.THREAT_WORDS:
            if word in text:
                score += 1
                reasons.append(f"Threat cue detected: {word}")

        if score >= 4:
            risk = "high"
        elif score >= 2:
            risk = "medium"
        else:
            risk = "low"

        return {
            "semantic_score": score,
            "semantic_risk": risk,
            "semantic_reasons": reasons
        }
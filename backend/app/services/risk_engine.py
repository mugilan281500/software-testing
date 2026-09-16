class RiskEngine:
    @staticmethod
    def calculate_test_risk(severity: str, category: str, is_passed: bool) -> float:
        if is_passed:
            return 0.0
        
        # Base weight by severity
        severity_weights = {
            "CRITICAL": 95.0,
            "HIGH": 75.0,
            "MEDIUM": 45.0,
            "LOW": 20.0
        }
        
        # Category risk multipliers
        category_multipliers = {
            "Authentication": 1.0,
            "Authorization": 1.0,
            "Business Logic": 0.95,
            "Validation": 0.85,
            "Rate Limiting": 0.80,
            "Security Headers": 0.65,
            "Response Validation": 0.75
        }
        
        base = severity_weights.get(severity.upper(), 50.0)
        multiplier = category_multipliers.get(category, 0.85)
        
        score = base * multiplier
        return round(min(max(score, 0.0), 100.0), 1)

    @staticmethod
    def calculate_overall_risk(results: list) -> tuple[float, float]:
        """
        Calculates (overall_risk_score, security_score) normalized from 0-100.
        """
        if not results:
            return 0.0, 100.0

        total = len(results)
        failed_results = [r for r in results if r.status == "FAILED"]
        
        if not failed_results:
            return 10.0, 95.0

        # Weighted sum of failed test risk scores
        critical_count = sum(1 for r in failed_results if r.severity == "CRITICAL")
        high_count = sum(1 for r in failed_results if r.severity == "HIGH")
        medium_count = sum(1 for r in failed_results if r.severity == "MEDIUM")
        low_count = sum(1 for r in failed_results if r.severity == "LOW")

        impact_score = (critical_count * 30.0) + (high_count * 15.0) + (medium_count * 6.0) + (low_count * 2.0)
        failure_ratio = len(failed_results) / float(total)
        
        overall_risk = (impact_score * 0.6) + (failure_ratio * 40.0)
        overall_risk = round(min(max(overall_risk, 0.0), 100.0), 1)
        
        security_score = round(max(100.0 - overall_risk, 0.0), 1)
        return overall_risk, security_score

    @staticmethod
    def get_risk_level(score: float) -> str:
        if score >= 76.0:
            return "CRITICAL"
        elif score >= 51.0:
            return "HIGH"
        elif score >= 26.0:
            return "MEDIUM"
        else:
            return "LOW"

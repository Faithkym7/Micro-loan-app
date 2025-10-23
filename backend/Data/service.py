# service.py
from abc import ABC, abstractmethod

class BaseCalculator(ABC):
    @abstractmethod
    def calculate_score(self, data: dict) -> float:
        pass
    
# character
class CharacterCalculator(BaseCalculator):
    def calculate_score(self, data: dict) -> float:
        """
        data: {
            "credit_score": int,
            "tax_compliant": bool
        }
        Returns score between 0 and 100
        """
        credit_score = data.get("credit_score", 0)
        tax_compliant = data.get("tax_compliant", False)

        # credits score contribution
        if credit_score < 300:
            score = 20
        elif credit_score < 600:
            score = 50
        elif credit_score < 750:
            score = 80
        else:
            score = 100

        # tax compliance contribution
        if tax_compliant:
            score += 10

        return min(score, 100)  
    
# capacity
class CapacityCalculator(BaseCalculator):
    def calculate_score(self, data: dict) -> float:
        """
        data: {
            'balance_sheet': pd.DataFrame,
            'income_statement': pd.DataFrame,
            'cash_flow': pd.DataFrame
        }
        """
        try:
            income = data.get("income_statement")
            cash_flow = data.get("cash_flow")
            if income is not None and not income.empty:
                profit = income.iloc[-1, 1]  # assume column 1 = net profit
                score = min(max(profit / 50_000, 0) * 100, 100)
            else:
                score = 50
        except Exception:
            score = 50

        return score
    

# Capital C (cashflow/growth)
class CapitalCalculator(BaseCalculator):
    def calculate_score(self, data: dict) -> float:
        """
        data: {
            'balance_sheet': pd.DataFrame,
            'income_statement': pd.DataFrame,
            'retained_earnings': pd.DataFrame
        }
        Returns score between 0 and 100
        """
        # For simplicity, just calculate growth rate = retained_earnings / previous retained_earnings
        try:
            re = data.get("retained_earnings")
            if re is not None and not re.empty:
                growth = re.iloc[-1, 0] / max(re.iloc[-2, 0], 1)
                if growth < 0.9:
                    score = 40
                elif growth < 1.2:
                    score = 70
                else:
                    score = 100
            else:
                score = 50
        except Exception:
            score = 50

        return score
    
# Collateral C
class CollateralCalculator(BaseCalculator):
    def calculate_score(self, data: dict) -> float:
        """
        data: {
            "collateral_value": int,
            "liquidation_value": int (1-5)
        }
        """
        collateral_value = data.get("collateral_value", 0)
        liquidity = data.get("liquidation_value", 1)

        # Simple weighted formula
        score = min(collateral_value / 2_500_000, 100)  # normalize to 100
        score *= liquidity / 5  # adjust by liquidity
        return min(score, 100)

# Conditions C
class ConditionsCalculator(BaseCalculator):
    def calculate_score(self, data: dict) -> float:
        """
        data: {
            "loan_amount": float,
            "interest_rate": float
        }
        Higher loan + high interest = more risk -> lower score
        """
        amount = data.get("loan_amount", 0)
        rate = data.get("interest_rate", 0)

        # Simple risk adjustment formula
        risk_factor = (amount / 10_000_000) + (rate / 20)  # normalize
        score = max(100 - risk_factor * 100, 0)
        return score

class EligibilityCalculatorService:
    def __init__(self):
        self.weights = {
            "character": 0.2,
            "capacity": 0.2,
            "capital": 0.2,
            "collateral": 0.2,
            "conditions": 0.2
        }
        self.calculators = {
            "character": CharacterCalculator(),
            "capacity": CapacityCalculator(),
            "capital": CapitalCalculator(),
            "collateral": CollateralCalculator(),
            "conditions": ConditionsCalculator()
        }

    def calculate_overall_score(self, data: dict) -> float:
        total = 0
        for key, weight in self.weights.items():
            calc = self.calculators[key]
            score = calc.calculate_score(data.get(key, {}))
            total += score * weight
        return round(total, 2)

    def is_eligible(self, data: dict, threshold: float = 60) -> bool:
        return self.calculate_overall_score(data) >= threshold

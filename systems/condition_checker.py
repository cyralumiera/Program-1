"""
ConditionChecker - Evaluator untuk kondisi kompleks
Mengecek flag, bukti, dan kondisi lainnya untuk determine story branch
"""

from typing import Dict, Any, List, Optional, Callable


class Condition:
    """Representasi satu kondisi"""
    
    def __init__(self, condition_type: str, target: str, value: Any = None):
        self.type = condition_type  # "flag", "evidence", "evidence_count", "flag_range"
        self.target = target  # Nama flag atau evidence_id
        self.value = value
        
    def check(self, game_manager) -> bool:
        """Evaluasi kondisi"""
        if self.type == "flag":
            return game_manager.get_flag(self.target) == self.value
        
        elif self.type == "flag_true":
            return game_manager.get_flag(self.target, False) is True
        
        elif self.type == "flag_false":
            return game_manager.get_flag(self.target, False) is False
        
        elif self.type == "evidence":
            return game_manager.has_evidence(self.target)
        
        elif self.type == "no_evidence":
            return not game_manager.has_evidence(self.target)
        
        elif self.type == "evidence_count_min":
            return game_manager.get_evidence_count() >= self.value
        
        elif self.type == "evidence_count_max":
            return game_manager.get_evidence_count() <= self.value
        
        elif self.type == "evidence_count_equal":
            return game_manager.get_evidence_count() == self.value
        
        return False


class ComplexCondition:
    """Kondisi kompleks dengan logical operators"""
    
    def __init__(self, operator: str = "AND"):
        self.operator = operator  # "AND", "OR", "NOT"
        self.conditions: List[Condition] = []
        self.sub_conditions: List['ComplexCondition'] = []
        
    def add_condition(self, condition: Condition) -> None:
        """Tambah kondisi simple"""
        self.conditions.append(condition)
    
    def add_complex_condition(self, complex_condition: 'ComplexCondition') -> None:
        """Tambah kondisi kompleks nested"""
        self.sub_conditions.append(complex_condition)
    
    def evaluate(self, game_manager) -> bool:
        """Evaluasi kondisi kompleks"""
        results = []
        
        # Evaluasi semua kondisi simple
        for condition in self.conditions:
            results.append(condition.check(game_manager))
        
        # Evaluasi semua sub-conditions
        for sub in self.sub_conditions:
            results.append(sub.evaluate(game_manager))
        
        # Apply operator
        if self.operator == "AND":
            return all(results) if results else True
        elif self.operator == "OR":
            return any(results) if results else False
        elif self.operator == "NOT":
            return not all(results) if results else True
        
        return False


class ConditionChecker:
    """Utility untuk mengecek berbagai kondisi dalam game"""
    
    @staticmethod
    def check_flag_value(game_manager, flag_name: str, expected_value: Any) -> bool:
        """Cek apakah flag memiliki nilai tertentu"""
        return game_manager.get_flag(flag_name) == expected_value
    
    @staticmethod
    def check_multiple_flags(game_manager, flags_dict: Dict[str, Any]) -> bool:
        """Cek apakah multiple flags sesuai dengan nilai yang diharapkan"""
        for flag_name, expected_value in flags_dict.items():
            if game_manager.get_flag(flag_name) != expected_value:
                return False
        return True
    
    @staticmethod
    def check_any_flag(game_manager, flag_names: List[str]) -> bool:
        """Cek apakah setidaknya satu flag True"""
        for flag_name in flag_names:
            if game_manager.get_flag(flag_name, False) is True:
                return True
        return False
    
    @staticmethod
    def check_all_flags(game_manager, flag_names: List[str]) -> bool:
        """Cek apakah semua flag True"""
        for flag_name in flag_names:
            if game_manager.get_flag(flag_name, False) is not True:
                return False
        return True
    
    @staticmethod
    def check_evidence_requirements(game_manager, required_evidence: List[str]) -> bool:
        """Cek apakah pemain punya semua bukti yang diperlukan"""
        for evidence_id in required_evidence:
            if not game_manager.has_evidence(evidence_id):
                return False
        return True
    
    @staticmethod
    def check_any_evidence(game_manager, evidence_list: List[str]) -> bool:
        """Cek apakah pemain punya setidaknya satu dari bukti yang disebutkan"""
        for evidence_id in evidence_list:
            if game_manager.has_evidence(evidence_id):
                return True
        return False
    
    @staticmethod
    def check_evidence_count_range(game_manager, min_count: int = 0, max_count: int = None) -> bool:
        """Cek apakah jumlah bukti dalam range tertentu"""
        count = game_manager.get_evidence_count()
        
        if count < min_count:
            return False
        
        if max_count is not None and count > max_count:
            return False
        
        return True
    
    @staticmethod
    def check_dialogue_unlocked(game_manager, dialogue_flag: str) -> bool:
        """Cek apakah dialog sudah unlocked (berdasarkan flag)"""
        return game_manager.get_flag(f"dialogue_unlocked_{dialogue_flag}", False) is True
    
    @staticmethod
    def check_scene_available(game_manager, scene_conditions: Dict) -> bool:
        """Cek apakah scene bisa diakses berdasarkan kondisi"""
        return ConditionChecker.check_multiple_flags(game_manager, scene_conditions)
    
    @staticmethod
    def create_condition_from_dict(condition_dict: Dict) -> Condition:
        """Buat Condition object dari dictionary"""
        return Condition(
            condition_type=condition_dict.get('type', 'flag'),
            target=condition_dict.get('target', ''),
            value=condition_dict.get('value')
        )
    
    @staticmethod
    def create_complex_condition_from_dict(cond_dict: Dict) -> ComplexCondition:
        """Buat ComplexCondition dari dictionary (format JSON)"""
        operator = cond_dict.get('operator', 'AND')
        complex_cond = ComplexCondition(operator)
        
        # Tambah kondisi simple
        for simple_cond in cond_dict.get('conditions', []):
            complex_cond.add_condition(
                ConditionChecker.create_condition_from_dict(simple_cond)
            )
        
        # Tambah sub-conditions (nested)
        for sub_cond_dict in cond_dict.get('sub_conditions', []):
            complex_cond.add_complex_condition(
                ConditionChecker.create_complex_condition_from_dict(sub_cond_dict)
            )
        
        return complex_cond

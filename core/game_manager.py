"""
GameManager - Pengelola utama game
Mengontrol flow game, state pemain, dan integrasi semua sistem
"""

import json
from typing import Dict, List, Any, Optional


class GameManager:
    """Pengelola utama state dan flow game"""
    
    def __init__(self):
        self.current_case = None
        self.current_location = None
        self.player_flags = {}  # Tracking pilihan pemain
        self.player_evidence = []  # Bukti yang dikumpulkan
        self.case_data = {}
        self.game_state = "menu"  # menu, playing, ending
        self.ending_achieved = None
        
    def load_case(self, case_id: str) -> bool:
        """Load kasus dari data"""
        try:
            with open(f'data/cases/{case_id}.json', 'r', encoding='utf-8') as f:
                self.case_data = json.load(f)
                self.current_case = case_id
                self.current_location = self.case_data.get('start_location')
                self.player_flags = {}
                self.player_evidence = []
                return True
        except FileNotFoundError:
            print(f"❌ Kasus {case_id} tidak ditemukan")
            return False
    
    def set_flag(self, flag_name: str, value: Any) -> None:
        """Set flag pemain untuk tracking pilihan"""
        self.player_flags[flag_name] = value
        
    def get_flag(self, flag_name: str, default: Any = None) -> Any:
        """Ambil nilai flag"""
        return self.player_flags.get(flag_name, default)
    
    def add_evidence(self, evidence_id: str) -> bool:
        """Tambah bukti ke inventory"""
        if evidence_id not in self.player_evidence:
            self.player_evidence.append(evidence_id)
            return True
        return False
    
    def has_evidence(self, evidence_id: str) -> bool:
        """Cek apakah pemain punya bukti tertentu"""
        return evidence_id in self.player_evidence
    
    def get_evidence_count(self) -> int:
        """Hitung total bukti"""
        return len(self.player_evidence)
    
    def get_location_data(self, location_id: str) -> Optional[Dict]:
        """Ambil data lokasi dari kasus"""
        locations = self.case_data.get('locations', {})
        return locations.get(location_id)
    
    def move_to_location(self, location_id: str) -> bool:
        """Pindah ke lokasi baru"""
        if location_id in self.case_data.get('locations', {}):
            self.current_location = location_id
            return True
        return False
    
    def check_ending_condition(self) -> Optional[str]:
        """Cek apakah kondisi ending terpenuhi"""
        endings = self.case_data.get('endings', [])
        
        for ending in endings:
            required_evidence = set(ending.get('required_evidence', []))
            player_evidence = set(self.player_evidence)
            
            # Cek bukti
            if not required_evidence.issubset(player_evidence):
                continue
            
            # Cek flag conditions
            conditions_met = True
            for flag_name, expected_value in ending.get('flags', {}).items():
                if self.get_flag(flag_name) != expected_value:
                    conditions_met = False
                    break
            
            if conditions_met:
                return ending.get('id')
        
        return None
    
    def reset_game(self) -> None:
        """Reset game state"""
        self.current_case = None
        self.current_location = None
        self.player_flags = {}
        self.player_evidence = []
        self.case_data = {}
        self.game_state = "menu"
        self.ending_achieved = None


class GameState:
    """Data class untuk menyimpan snapshot game"""
    
    def __init__(self, game_manager: GameManager):
        self.location = game_manager.current_location
        self.flags = game_manager.player_flags.copy()
        self.evidence = game_manager.player_evidence.copy()
    
    def restore(self, game_manager: GameManager) -> None:
        """Restore state ke game manager"""
        game_manager.current_location = self.location
        game_manager.player_flags = self.flags.copy()
        game_manager.player_evidence = self.evidence.copy()

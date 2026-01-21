"""
ChoiceTracker - Pelacak pilihan dan dampaknya
Mencatat keputusan pemain dan memberikan konsekuensi
"""

from typing import Dict, List, Optional, Callable


class ChoiceTracker:
    """Melacak dan mengelola konsekuensi pilihan pemain"""
    
    def __init__(self):
        self.choices_made = []  # List pilihan yang dibuat
        self.choice_consequences = {}  # Map pilihan ke konsekuensi
        
    def record_choice(self, choice_data: Dict) -> None:
        """Catat pilihan pemain"""
        choice = {
            'id': choice_data.get('id'),
            'text': choice_data.get('text'),
            'context': choice_data.get('context'),  # Dimana/kapan pilihan dibuat
            'timestamp': len(self.choices_made)  # Order dalam playthrough
        }
        self.choices_made.append(choice)
    
    def get_all_choices(self) -> List[Dict]:
        """Ambil semua pilihan yang dibuat"""
        return self.choices_made
    
    def apply_consequences(self, choice_id: str, consequence: Dict, game_manager) -> None:
        """
        Terapkan konsekuensi pilihan
        consequence format:
        {
            'message': str,
            'flags': {flag: value},
            'evidence_change': {add: [...], remove: [...]},
            'dialogue_unlock': [...]
        }
        """
        # Tampilkan message
        if 'message' in consequence:
            print(f"\n📍 {consequence['message']}")
        
        # Set flags
        for flag_name, value in consequence.get('flags', {}).items():
            game_manager.set_flag(flag_name, value)
        
        # Tambah bukti
        for evidence_id in consequence.get('evidence_change', {}).get('add', []):
            game_manager.add_evidence(evidence_id)
        
        # Hapus bukti
        for evidence_id in consequence.get('evidence_change', {}).get('remove', []):
            if evidence_id in game_manager.player_evidence:
                game_manager.player_evidence.remove(evidence_id)
    
    def get_critical_choices(self) -> List[Dict]:
        """Ambil pilihan kritis yang mempengaruhi ending"""
        critical = []
        for choice in self.choices_made:
            if choice.get('is_critical'):
                critical.append(choice)
        return critical
    
    def choice_leads_to_bad_ending(self, choice_id: str) -> bool:
        """Cek apakah pilihan mengarah ke bad ending"""
        # Bisa diimplementasikan dengan analisis flag dan bukti
        return False
    
    def reset_choices(self) -> None:
        """Reset tracker pilihan"""
        self.choices_made = []
        self.choice_consequences = {}


class ConsequenceChain:
    """Mengelola chain konsekuensi dari pilihan"""
    
    def __init__(self):
        self.chains = {}  # id -> list of consequences
        
    def add_chain(self, chain_id: str, consequences: List[Dict]) -> None:
        """Tambah chain konsekuensi"""
        self.chains[chain_id] = consequences
    
    def get_chain(self, chain_id: str) -> Optional[List[Dict]]:
        """Ambil chain konsekuensi"""
        return self.chains.get(chain_id)
    
    def execute_chain(self, chain_id: str, game_manager, callback: Callable = None) -> bool:
        """
        Jalankan chain konsekuensi secara berurutan
        callback: untuk menampilkan feedback ke UI
        """
        chain = self.get_chain(chain_id)
        if not chain:
            return False
        
        for i, consequence in enumerate(chain):
            if callback:
                callback(f"Konsekuensi {i+1}/{len(chain)}...")
            
            # Apply consequence
            if 'flags' in consequence:
                for flag, value in consequence['flags'].items():
                    game_manager.set_flag(flag, value)
            
            if 'evidence' in consequence:
                for evidence_id in consequence['evidence']:
                    game_manager.add_evidence(evidence_id)
        
        return True

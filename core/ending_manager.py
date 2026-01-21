"""
EndingManager - Pengelola ending dan hasil permainan
Menentukan ending berdasarkan keputusan dan bukti pemain
"""

from typing import Dict, List, Optional
from enum import Enum


class EndingType(Enum):
    """Tipe-tipe ending yang mungkin"""
    FAILURE = "failure"  # Kegagalan, pelaku lolos
    PARTIAL_SUCCESS = "partial_success"  # Sukses tapi bukti kurang sempurna
    SUCCESS = "success"  # Sukses normal
    BRILLIANT = "brilliant"  # Sukses sempurna, detektif jenius
    SPECIAL = "special"  # Ending khusus berdasarkan pilihan


class EndingManager:
    """Pengelola sistem ending dan hasil akhir"""
    
    def __init__(self, case_data: Dict):
        self.case_data = case_data
        self.endings_data = case_data.get('endings', [])
        self.achieved_ending = None
        
    def evaluate_ending(self, game_manager) -> Optional[Dict]:
        """
        Evaluasi ending yang dicapai berdasarkan state pemain
        Return ending data jika ada yang match, None sebaliknya
        """
        for ending in self.endings_data:
            if self._check_ending_condition(ending, game_manager):
                self.achieved_ending = ending
                return ending
        
        # Jika tidak ada ending match, return generic failure
        return self._get_default_failure_ending()
    
    def _check_ending_condition(self, ending: Dict, game_manager) -> bool:
        """Cek apakah kondisi ending terpenuhi"""
        
        # Cek bukti yang diperlukan
        required_evidence = set(ending.get('required_evidence', []))
        player_evidence = set(game_manager.player_evidence)
        
        if not required_evidence.issubset(player_evidence):
            return False
        
        # Cek flag conditions
        conditions = ending.get('conditions', {})
        for flag_name, expected_value in conditions.items():
            if game_manager.get_flag(flag_name) != expected_value:
                return False
        
        # Cek minimum/maximum evidence
        min_evidence = ending.get('min_evidence', 0)
        max_evidence = ending.get('max_evidence', float('inf'))
        
        evidence_count = game_manager.get_evidence_count()
        if not (min_evidence <= evidence_count <= max_evidence):
            return False
        
        # Cek question accuracy jika diperlukan
        min_accuracy = ending.get('min_accuracy', 0)
        # Accuracy dihitung dari QuestionManager
        
        return True
    
    def get_ending_text(self, ending_id: str) -> Optional[str]:
        """Ambil teks ending"""
        for ending in self.endings_data:
            if ending.get('id') == ending_id:
                return ending.get('text', '')
        return None
    
    def get_ending_data(self, ending_id: str) -> Optional[Dict]:
        """Ambil data lengkap ending"""
        for ending in self.endings_data:
            if ending.get('id') == ending_id:
                return ending
        return None
    
    def get_ending_rating(self) -> Optional[Dict]:
        """Ambil rating ending yang dicapai"""
        if not self.achieved_ending:
            return None
        
        ending_type = self.achieved_ending.get('type', 'unknown')
        ending_id = self.achieved_ending.get('id', 'unknown')
        
        ratings = {
            'failure': {'emoji': '❌', 'text': 'Penyelidikan Gagal', 'color': 'red'},
            'partial_success': {'emoji': '⚖️', 'text': 'Kesuksesan Parsial', 'color': 'yellow'},
            'success': {'emoji': '✅', 'text': 'Kesuksesan', 'color': 'green'},
            'brilliant': {'emoji': '🏆', 'text': 'Detektif Jenius!', 'color': 'gold'},
            'special': {'emoji': '⭐', 'text': 'Ending Spesial', 'color': 'purple'}
        }
        
        return ratings.get(ending_type, {
            'emoji': '❓',
            'text': 'Ending Tidak Dikenal',
            'color': 'gray'
        })
    
    def get_playthrough_stats(self, game_manager, question_manager) -> Dict:
        """Ambil statistik playthrough lengkap"""
        question_stats = question_manager.get_question_stats()
        
        stats = {
            'ending_id': self.achieved_ending.get('id') if self.achieved_ending else None,
            'ending_type': self.achieved_ending.get('type') if self.achieved_ending else None,
            'total_evidence': game_manager.get_evidence_count(),
            'critical_choices': len([c for c in game_manager.player_flags.items() if 'choice' in c[0]]),
            'question_stats': question_stats,
            'flags_set': game_manager.player_flags
        }
        
        return stats
    
    def _get_default_failure_ending(self) -> Dict:
        """Return generic failure ending"""
        return {
            'id': 'generic_failure',
            'type': 'failure',
            'title': 'Penyelidikan Gagal',
            'text': 'Anda tidak berhasil mengumpulkan bukti yang cukup. Pelaku berhasil lolos...',
            'required_evidence': [],
            'conditions': {}
        }
    
    def is_good_ending(self) -> bool:
        """Cek apakah ending adalah 'good ending'"""
        if not self.achieved_ending:
            return False
        
        ending_type = self.achieved_ending.get('type')
        return ending_type in ['success', 'brilliant', 'special']
    
    def is_brilliant_ending(self) -> bool:
        """Cek apakah ending adalah brilliant ending"""
        if not self.achieved_ending:
            return False
        
        return self.achieved_ending.get('type') == 'brilliant'

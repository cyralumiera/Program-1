"""
QuestionManager - Pengelola sistem pertanyaan edukatif
Menampilkan soal, memvalidasi jawaban, dan menentukan output
"""

import json
from typing import Dict, List, Optional, Tuple
from enum import Enum


class QuestionType(Enum):
    """Tipe pertanyaan yang tersedia"""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LOGIC = "logic"


class QuestionManager:
    """Pengelola pertanyaan dan validasi jawaban"""
    
    def __init__(self, case_data: Dict):
        self.case_data = case_data
        self.questions = case_data.get('questions', {})
        self.question_history = []  # Track pertanyaan yang sudah dijawab
        
    def get_question(self, question_id: str) -> Optional[Dict]:
        """Ambil data pertanyaan"""
        return self.questions.get(question_id)
    
    def get_question_by_type(self, question_type: str) -> Optional[Dict]:
        """Cari pertanyaan berdasarkan tipe"""
        for q_id, q_data in self.questions.items():
            if q_data.get('type') == question_type:
                return q_data
        return None
    
    def validate_answer(self, question_id: str, user_answer: str) -> Tuple[bool, Dict]:
        """
        Validasi jawaban pertanyaan
        Return: (is_correct, result_data)
        """
        question = self.get_question(question_id)
        
        if not question:
            return False, {'error': 'Pertanyaan tidak ditemukan'}
        
        question_type = question.get('type')
        correct_answer = question.get('correct_answer')
        
        # Normalize jawaban
        user_answer_normalized = user_answer.strip().lower()
        correct_answer_normalized = correct_answer.strip().lower()
        
        is_correct = user_answer_normalized == correct_answer_normalized
        
        # Ambil hasil berdasarkan kebenaran
        if is_correct:
            result = question.get('on_correct', {})
        else:
            result = question.get('on_incorrect', {})
        
        # Simpan ke history
        self.question_history.append({
            'question_id': question_id,
            'user_answer': user_answer,
            'is_correct': is_correct
        })
        
        return is_correct, result
    
    def apply_result(self, result: Dict, game_manager) -> None:
        """
        Terapkan hasil ke game state
        result format:
        {
            'evidence': [...],
            'flags': {flag: value},
            'dialogue_unlock': [...],
            'message': str
        }
        """
        # Tambah bukti
        for evidence_id in result.get('evidence', []):
            game_manager.add_evidence(evidence_id)
        
        # Set flags
        for flag_name, value in result.get('flags', {}).items():
            game_manager.set_flag(flag_name, value)
        
        # Unlock dialog
        for dialogue_id in result.get('dialogue_unlock', []):
            # Dialog akan di-unlock saat ditampilkan berdasarkan flags
            pass
    
    def get_question_stats(self) -> Dict:
        """Ambil statistik jawaban pertanyaan"""
        total = len(self.question_history)
        correct = sum(1 for q in self.question_history if q['is_correct'])
        accuracy = (correct / total * 100) if total > 0 else 0
        
        return {
            'total_questions': total,
            'correct_answers': correct,
            'wrong_answers': total - correct,
            'accuracy': accuracy
        }
    
    def get_clue_unlock_question(self, clue_id: str) -> Optional[Dict]:
        """Ambil pertanyaan untuk unlock clue tertentu"""
        clues = self.case_data.get('clues', {})
        clue = clues.get(clue_id)
        
        if not clue:
            return None
        
        unlock_req = clue.get('unlock_requirement', {})
        question_id = unlock_req.get('question_id')
        
        if not question_id:
            return None
        
        return self.get_question(question_id)
    
    def get_dialogue_question(self, npc_id: str, dialogue_id: str) -> Optional[Dict]:
        """Ambil pertanyaan dari dialog NPC"""
        characters = self.case_data.get('characters', {})
        npc = characters.get(npc_id)
        
        if not npc:
            return None
        
        dialogues = npc.get('dialogues', {})
        dialogue = dialogues.get(dialogue_id)
        
        if not dialogue:
            return None
        
        question_id = dialogue.get('question')
        
        if not question_id:
            return None
        
        return self.get_question(question_id)
    
    def has_answered_question(self, question_id: str) -> bool:
        """Cek apakah pemain sudah menjawab pertanyaan tertentu"""
        for q in self.question_history:
            if q['question_id'] == question_id:
                return True
        return False
    
    def get_last_answer_result(self, question_id: str) -> Optional[bool]:
        """Ambil hasil jawaban terakhir untuk pertanyaan tertentu"""
        for q in reversed(self.question_history):
            if q['question_id'] == question_id:
                return q['is_correct']
        return None

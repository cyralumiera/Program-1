"""
DialogueSystem - Pengelola sistem dialog dan interaksi dengan NPC
"""

from typing import Dict, List, Optional
from enum import Enum


class DialogueAction(Enum):
    """Aksi yang bisa terjadi dalam dialog"""
    UNLOCK_EVIDENCE = "unlock_evidence"
    SET_FLAG = "set_flag"
    SHOW_QUESTION = "show_question"
    CHANGE_RELATION = "change_relation"
    ADVANCE_PLOT = "advance_plot"


class DialogueNode:
    """Representasi satu node dalam dialogue tree"""
    
    def __init__(self, node_id: str, text: str):
        self.id = node_id
        self.text = text
        self.choices = []  # List of choice nodes
        self.actions = []  # List of actions to execute
        self.next_node = None  # Next node if linear
        
    def add_choice(self, choice_text: str, next_node_id: str) -> None:
        """Tambah pilihan dalam dialog"""
        self.choices.append({
            'text': choice_text,
            'next_node_id': next_node_id
        })
    
    def add_action(self, action: Dict) -> None:
        """Tambah aksi yang dilakukan dalam node ini"""
        self.actions.append(action)


class DialogueSystem:
    """Pengelola sistem dialog dengan NPC"""
    
    def __init__(self):
        self.dialogue_trees = {}  # npc_id -> dialogue tree
        self.current_dialogue = None
        self.dialogue_history = []
        
    def load_dialogue_tree(self, npc_id: str, tree_data: Dict) -> None:
        """Load dialogue tree untuk NPC"""
        self.dialogue_trees[npc_id] = tree_data
    
    def start_dialogue(self, npc_id: str, dialogue_id: str) -> Optional[Dict]:
        """Mulai dialog dengan NPC"""
        tree = self.dialogue_trees.get(npc_id)
        
        if not tree:
            return None
        
        dialogue = tree.get(dialogue_id)
        
        if not dialogue:
            return None
        
        self.current_dialogue = {
            'npc_id': npc_id,
            'dialogue_id': dialogue_id,
            'current_node': dialogue
        }
        
        return dialogue
    
    def get_current_dialogue_text(self) -> Optional[str]:
        """Ambil teks dialog yang sedang berjalan"""
        if not self.current_dialogue:
            return None
        
        return self.current_dialogue.get('current_node', {}).get('text')
    
    def get_current_choices(self) -> List[Dict]:
        """Ambil pilihan dalam dialog saat ini"""
        if not self.current_dialogue:
            return []
        
        current_node = self.current_dialogue.get('current_node', {})
        return current_node.get('choices', [])
    
    def make_dialogue_choice(self, choice_index: int) -> bool:
        """Pilih salah satu opsi dalam dialog"""
        if not self.current_dialogue:
            return False
        
        choices = self.get_current_choices()
        
        if choice_index < 0 or choice_index >= len(choices):
            return False
        
        choice = choices[choice_index]
        next_dialogue_id = choice.get('next_dialogue_id')
        
        # Record pilihan
        self.dialogue_history.append({
            'npc_id': self.current_dialogue.get('npc_id'),
            'choice_text': choice.get('text'),
            'next_id': next_dialogue_id
        })
        
        # Move ke next dialog
        if next_dialogue_id:
            npc_tree = self.dialogue_trees.get(self.current_dialogue.get('npc_id'), {})
            next_node = npc_tree.get(next_dialogue_id)
            
            if next_node:
                self.current_dialogue['current_node'] = next_node
                return True
        
        return False
    
    def end_dialogue(self) -> None:
        """Akhiri dialog saat ini"""
        self.current_dialogue = None
    
    def is_in_dialogue(self) -> bool:
        """Cek apakah sedang dalam dialog"""
        return self.current_dialogue is not None
    
    def get_dialogue_history(self) -> List[Dict]:
        """Ambil history dialog"""
        return self.dialogue_history
    
    def reset_dialogue_history(self) -> None:
        """Reset history dialog"""
        self.dialogue_history = []

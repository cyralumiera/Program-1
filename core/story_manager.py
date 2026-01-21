"""
StoryManager - Pengelola narasi dan dialog
Mengatur flow cerita, menampilkan narasi, dan menangani pilihan pemain
"""

from typing import Dict, List, Optional, Any


class StoryManager:
    """Pengelola cerita bercabang"""
    
    def __init__(self, case_data: Dict):
        self.case_data = case_data
        self.visited_scenes = set()
        
    def get_location_description(self, location_id: str) -> str:
        """Ambil deskripsi lokasi"""
        location = self.case_data['locations'].get(location_id, {})
        return location.get('description', 'Lokasi tidak dikenal')
    
    def get_scene(self, scene_id: str, flags: Dict = None) -> Optional[Dict]:
        """Ambil data scene dengan cek kondisi"""
        if flags is None:
            flags = {}
        
        scenes = self.case_data.get('scenes', {})
        scene = scenes.get(scene_id)
        
        if not scene:
            return None
        
        # Cek apakah scene sesuai kondisi flags
        conditions = scene.get('conditions', {})
        if conditions and not self._check_conditions(conditions, flags):
            return None
        
        return scene
    
    def get_location_scenes(self, location_id: str, flags: Dict = None) -> List[Dict]:
        """Ambil semua scene di lokasi tertentu"""
        if flags is None:
            flags = {}
        
        location = self.case_data['locations'].get(location_id, {})
        scenes = location.get('scenes', [])
        
        available_scenes = []
        for scene_id in scenes:
            scene = self.get_scene(scene_id, flags)
            if scene:
                available_scenes.append({
                    'id': scene_id,
                    'title': scene.get('title', scene_id),
                    'type': scene.get('type', 'dialogue'),
                    'description': scene.get('description', '')
                })
        
        return available_scenes
    
    def get_npcs_at_location(self, location_id: str, flags: Dict = None) -> List[Dict]:
        """Ambil daftar NPC di lokasi"""
        if flags is None:
            flags = {}
        
        location = self.case_data['locations'].get(location_id, {})
        npcs = location.get('npcs', [])
        
        available_npcs = []
        for npc_id in npcs:
            npc = self.case_data.get('characters', {}).get(npc_id)
            if npc and self._check_conditions(npc.get('conditions', {}), flags):
                available_npcs.append({
                    'id': npc_id,
                    'name': npc.get('name', npc_id),
                    'role': npc.get('role', 'Unknown')
                })
        
        return available_npcs
    
    def get_dialogue(self, npc_id: str, dialogue_id: str, flags: Dict = None) -> Optional[Dict]:
        """Ambil dialog dari NPC"""
        if flags is None:
            flags = {}
        
        npcs = self.case_data.get('characters', {})
        npc = npcs.get(npc_id)
        
        if not npc:
            return None
        
        dialogues = npc.get('dialogues', {})
        dialogue = dialogues.get(dialogue_id)
        
        if not dialogue:
            return None
        
        # Cek kondisi
        if not self._check_conditions(dialogue.get('conditions', {}), flags):
            return None
        
        return dialogue
    
    def get_available_dialogues(self, npc_id: str, flags: Dict = None) -> List[Dict]:
        """Ambil dialog yang bisa diakses dari NPC"""
        if flags is None:
            flags = {}
        
        npcs = self.case_data.get('characters', {})
        npc = npcs.get(npc_id)
        
        if not npc:
            return []
        
        available = []
        dialogues = npc.get('dialogues', {})
        
        for dialogue_id, dialogue_data in dialogues.items():
            if self._check_conditions(dialogue_data.get('conditions', {}), flags):
                available.append({
                    'id': dialogue_id,
                    'text': dialogue_data.get('text', dialogue_id),
                    'question': dialogue_data.get('question', None)
                })
        
        return available
    
    def get_clue_unlock_info(self, clue_id: str) -> Optional[Dict]:
        """Ambil info soal/syarat unlock clue"""
        clues = self.case_data.get('clues', {})
        clue = clues.get(clue_id)
        
        if not clue:
            return None
        
        unlock_requirement = clue.get('unlock_requirement', {})
        return unlock_requirement
    
    def _check_conditions(self, conditions: Dict, flags: Dict) -> bool:
        """Cek apakah kondisi terpenuhi"""
        for flag_name, expected_value in conditions.items():
            if flags.get(flag_name) != expected_value:
                return False
        return True
    
    def mark_scene_visited(self, scene_id: str) -> None:
        """Tandai scene sudah dikunjungi"""
        self.visited_scenes.add(scene_id)
    
    def is_scene_visited(self, scene_id: str) -> bool:
        """Cek apakah scene sudah dikunjungi"""
        return scene_id in self.visited_scenes

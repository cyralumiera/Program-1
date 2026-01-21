"""
EvidenceInventory - Pengelola inventory bukti
Menyimpan, menampilkan, dan mengelola bukti yang dikumpulkan
"""

from typing import List, Dict, Optional


class Evidence:
    """Representasi satu bukti"""
    
    def __init__(self, evidence_id: str, name: str, description: str, category: str = "general"):
        self.id = evidence_id
        self.name = name
        self.description = description
        self.category = category  # e.g., "physical", "testimony", "document"
        self.found_at = None  # Lokasi ditemukan
        self.found_timestamp = None  # Kapan ditemukan
        
    def __repr__(self) -> str:
        return f"Evidence({self.id}: {self.name})"


class EvidenceInventory:
    """Pengelola inventory bukti pemain"""
    
    def __init__(self):
        self.evidence_list: List[Evidence] = []
        self.evidence_categories = {}  # category -> list of evidence_ids
        
    def add_evidence(self, evidence: Evidence, location: str = None) -> bool:
        """Tambah bukti ke inventory"""
        if any(e.id == evidence.id for e in self.evidence_list):
            return False  # Bukti sudah ada
        
        evidence.found_at = location
        evidence.found_timestamp = len(self.evidence_list)
        self.evidence_list.append(evidence)
        
        # Tambah ke kategori
        if evidence.category not in self.evidence_categories:
            self.evidence_categories[evidence.category] = []
        self.evidence_categories[evidence.category].append(evidence.id)
        
        return True
    
    def has_evidence(self, evidence_id: str) -> bool:
        """Cek apakah pemain punya bukti tertentu"""
        return any(e.id == evidence_id for e in self.evidence_list)
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Ambil bukti berdasarkan ID"""
        for evidence in self.evidence_list:
            if evidence.id == evidence_id:
                return evidence
        return None
    
    def get_evidence_by_category(self, category: str) -> List[Evidence]:
        """Ambil semua bukti dalam kategori tertentu"""
        if category not in self.evidence_categories:
            return []
        
        evidence_ids = self.evidence_categories[category]
        return [self.get_evidence(eid) for eid in evidence_ids if self.has_evidence(eid)]
    
    def get_all_evidence(self) -> List[Evidence]:
        """Ambil semua bukti"""
        return self.evidence_list
    
    def get_evidence_count(self) -> int:
        """Hitung total bukti"""
        return len(self.evidence_list)
    
    def remove_evidence(self, evidence_id: str) -> bool:
        """Hapus bukti dari inventory"""
        for i, evidence in enumerate(self.evidence_list):
            if evidence.id == evidence_id:
                self.evidence_list.pop(i)
                
                # Hapus dari kategori
                if evidence.category in self.evidence_categories:
                    self.evidence_categories[evidence.category].remove(evidence_id)
                
                return True
        return False
    
    def display_inventory(self) -> str:
        """Tampilkan inventory bukti (formatted string)"""
        if not self.evidence_list:
            return "📦 Inventory kosong\n"
        
        display = f"📦 INVENTORY BUKTI ({len(self.evidence_list)} item)\n"
        display += "=" * 50 + "\n"
        
        # Group by category
        for category in sorted(self.evidence_categories.keys()):
            evidence_ids = self.evidence_categories[category]
            display += f"\n📌 {category.upper()}\n"
            display += "-" * 50 + "\n"
            
            for eid in evidence_ids:
                evidence = self.get_evidence(eid)
                if evidence:
                    display += f"  • {evidence.name}\n"
                    display += f"    └─ {evidence.description}\n"
                    if evidence.found_at:
                        display += f"    📍 Ditemukan di: {evidence.found_at}\n"
        
        display += "=" * 50 + "\n"
        return display
    
    def get_evidence_summary(self) -> Dict:
        """Ambil ringkasan inventory"""
        return {
            'total_evidence': self.get_evidence_count(),
            'by_category': {
                cat: len(self.evidence_categories.get(cat, []))
                for cat in self.evidence_categories
            },
            'evidence_ids': [e.id for e in self.evidence_list]
        }
    
    def clear_inventory(self) -> None:
        """Kosongkan inventory"""
        self.evidence_list = []
        self.evidence_categories = {}

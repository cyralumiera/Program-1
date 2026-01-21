"""
GameUI - Interface text-based untuk game
"""

import os
from typing import List, Optional


class GameUI:
    """Pengelola UI dan display untuk game"""
    
    # Color codes untuk terminal
    class Colors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    @staticmethod
    def clear_screen():
        """Bersihkan layar"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def print_header(text: str, width: int = 60):
        """Print header dengan border"""
        print(f"\n{GameUI.Colors.BOLD}{GameUI.Colors.CYAN}")
        print("=" * width)
        print(text.center(width))
        print("=" * width)
        print(f"{GameUI.Colors.ENDC}")
    
    @staticmethod
    def print_subheader(text: str, width: int = 60):
        """Print sub-header"""
        print(f"\n{GameUI.Colors.BOLD}{GameUI.Colors.BLUE}{text}{GameUI.Colors.ENDC}")
        print("-" * width)
    
    @staticmethod
    def print_narration(text: str):
        """Print narasi/deskripsi"""
        print(f"\n{GameUI.Colors.CYAN}{text}{GameUI.Colors.ENDC}\n")
    
    @staticmethod
    def print_dialogue(speaker: str, text: str):
        """Print dialog dari NPC"""
        print(f"\n{GameUI.Colors.YELLOW}{GameUI.Colors.BOLD}{speaker}:{GameUI.Colors.ENDC} {text}\n")
    
    @staticmethod
    def print_player_action(text: str):
        """Print aksi pemain"""
        print(f"\n{GameUI.Colors.GREEN}→ {text}{GameUI.Colors.ENDC}\n")
    
    @staticmethod
    def print_success(text: str):
        """Print pesan sukses"""
        print(f"\n{GameUI.Colors.GREEN}✓ {text}{GameUI.Colors.ENDC}\n")
    
    @staticmethod
    def print_error(text: str):
        """Print pesan error"""
        print(f"\n{GameUI.Colors.RED}✗ {text}{GameUI.Colors.ENDC}\n")
    
    @staticmethod
    def print_warning(text: str):
        """Print pesan warning"""
        print(f"\n{GameUI.Colors.YELLOW}⚠ {text}{GameUI.Colors.ENDC}\n")
    
    @staticmethod
    def print_question(text: str, question_type: str = ""):
        """Print pertanyaan"""
        print(f"\n{GameUI.Colors.BOLD}❓ {text}{GameUI.Colors.ENDC}")
        if question_type:
            print(f"   (Tipe: {question_type})\n")
    
    @staticmethod
    def print_choices(choices: List[str], show_numbers: bool = True) -> int:
        """
        Print pilihan dan minta input user
        Return index pilihan (0-based)
        """
        print(f"\n{GameUI.Colors.BOLD}Pilihan:{GameUI.Colors.ENDC}")
        for i, choice in enumerate(choices):
            print(f"  {i + 1}. {choice}")
        
        while True:
            try:
                choice_input = input(f"\n{GameUI.Colors.BOLD}Masukkan nomor pilihan (1-{len(choices)}): {GameUI.Colors.ENDC}").strip()
                choice_num = int(choice_input)
                
                if 1 <= choice_num <= len(choices):
                    return choice_num - 1
                else:
                    GameUI.print_error(f"Nomor harus antara 1-{len(choices)}")
            except ValueError:
                GameUI.print_error("Input tidak valid. Masukkan angka.")
    
    @staticmethod
    def print_inventory_summary(evidence_ids: List[str], case_data: dict):
        """Print ringkasan inventory bukti"""
        if not evidence_ids:
            print(f"\n{GameUI.Colors.YELLOW}📦 Inventory kosong{GameUI.Colors.ENDC}\n")
            return
        
        print(f"\n{GameUI.Colors.BOLD}📦 BUKTI YANG DIKUMPULKAN ({len(evidence_ids)} item):{GameUI.Colors.ENDC}")
        print("-" * 50)
        
        clues = case_data.get('clues', {})
        for evidence_id in evidence_ids:
            clue = clues.get(evidence_id, {})
            name = clue.get('name', evidence_id)
            description = clue.get('description', '')
            print(f"  • {name}")
            print(f"    └─ {description}")
        print()
    
    @staticmethod
    def print_location_info(location_name: str, description: str, width: int = 60):
        """Print info lokasi"""
        print(f"\n{GameUI.Colors.BOLD}{GameUI.Colors.BLUE}📍 {location_name}{GameUI.Colors.ENDC}")
        print("-" * width)
        print(f"{description}\n")
    
    @staticmethod
    def print_npc_list(npcs: List[dict]):
        """Print list NPC di lokasi"""
        if not npcs:
            print(f"\n{GameUI.Colors.YELLOW}Tidak ada NPC di lokasi ini.{GameUI.Colors.ENDC}\n")
            return
        
        print(f"\n{GameUI.Colors.BOLD}🧑 NPC DI LOKASI INI:{GameUI.Colors.ENDC}")
        for i, npc in enumerate(npcs):
            print(f"  {i + 1}. {npc['name']} ({npc['role']})")
        print()
    
    @staticmethod
    def print_location_actions(location_id: str, exits: dict = None):
        """Print aksi yang bisa dilakukan di lokasi"""
        print(f"\n{GameUI.Colors.BOLD}AKSI:{GameUI.Colors.ENDC}")
        actions = [
            "1. Cari petunjuk di lokasi",
            "2. Bicara dengan NPC",
            "3. Buka inventory",
            "4. Lihat catatan penyelidikan"
        ]
        
        for action in actions:
            print(f"  {action}")
        
        if exits:
            print(f"\n{GameUI.Colors.BOLD}LOKASI YANG BISA DIKUNJUNGI:{GameUI.Colors.ENDC}")
            for i, (location_id, location_name) in enumerate(exits.items(), start=1):
                print(f"  {i+4}. {location_name}")
        
        print()
    
    @staticmethod
    def print_ending_screen(ending_data: dict, stats: dict):
        """Print screen akhir game dengan ending"""
        GameUI.clear_screen()
        
        ending_type = ending_data.get('type', 'unknown')
        ending_title = ending_data.get('title', 'Ending')
        ending_text = ending_data.get('text', '')
        
        # Print ending dengan emoji yang sesuai
        emojis = {
            'brilliant': '🏆',
            'success': '✅',
            'partial_success': '⚖️',
            'failure': '❌'
        }
        emoji = emojis.get(ending_type, '❓')
        
        GameUI.print_header(f"{emoji} {ending_title}", width=70)
        print(f"\n{ending_text}\n")
        
        # Print statistik
        GameUI.print_subheader("📊 STATISTIK PENYELIDIKAN", width=70)
        print(f"Total Bukti Dikumpulkan: {stats['total_evidence']}")
        print(f"Pertanyaan Dijawab: {stats['question_stats']['total_questions']}")
        print(f"Jawaban Benar: {stats['question_stats']['correct_answers']}")
        print(f"Akurasi: {stats['question_stats']['accuracy']:.1f}%")
        print(f"Pilihan Kritis: {stats['critical_choices']}")
        print()
    
    @staticmethod
    def print_main_menu():
        """Print main menu"""
        GameUI.clear_screen()
        GameUI.print_header("🔍 DETEKTIF PENGETAHUAN", width=60)
        print(f"{GameUI.Colors.BOLD}Selamat datang, Detektif!{GameUI.Colors.ENDC}\n")
        print("Dalam game ini, Anda berperan sebagai seorang detektif yang")
        print("harus memecahkan kasus misterius melalui:")
        print("  • Penyelidikan lokasi")
        print("  • Wawancara saksi")
        print("  • Analisis logika")
        print("  • Menjawab pertanyaan edukatif")
        print()
        print(f"{GameUI.Colors.BOLD}MENU:{GameUI.Colors.ENDC}")
        print("  1. Mulai Game Baru")
        print("  2. Tentang Game")
        print("  3. Keluar")
        print()
    
    @staticmethod
    def get_text_input(prompt: str = "Masukkan input: ") -> str:
        """Dapatkan input teks dari user"""
        return input(f"{GameUI.Colors.BOLD}{prompt}{GameUI.Colors.ENDC}").strip()
    
    @staticmethod
    def get_confirmation(prompt: str = "Yakin?") -> bool:
        """Dapatkan konfirmasi yes/no dari user"""
        response = GameUI.get_text_input(f"{prompt} (y/n): ").lower()
        return response in ['y', 'yes', 'ya']
    
    @staticmethod
    def press_enter_to_continue():
        """Tunggu user tekan Enter"""
        input(f"\n{GameUI.Colors.BOLD}(Tekan Enter untuk lanjut...){GameUI.Colors.ENDC}")

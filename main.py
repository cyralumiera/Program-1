"""
GameLoop - Main loop permainan
Mengintegrasikan semua sistem dan mengatur flow game
"""

import sys
import json
from typing import Optional

# Import semua managers dan systems
from core.game_manager import GameManager
from core.story_manager import StoryManager
from core.question_manager import QuestionManager
from core.choice_tracker import ChoiceTracker
from core.ending_manager import EndingManager
from systems.evidence_inventory import Evidence, EvidenceInventory
from systems.dialogue_system import DialogueSystem
from systems.condition_checker import ConditionChecker
from ui.game_ui import GameUI


class GameLoop:
    """Main game loop - mengintegrasikan semua sistem"""
    
    def __init__(self):
        self.game_manager = GameManager()
        self.story_manager = None
        self.question_manager = None
        self.choice_tracker = ChoiceTracker()
        self.ending_manager = None
        self.evidence_inventory = EvidenceInventory()
        self.dialogue_system = DialogueSystem()
        self.running = False
        self.checkpoint_asked = False  # Flag untuk checkpoint pertanyaan
        self.ending_reached = False  # Flag jika ending sudah tercapai
        
    def start(self):
        """Mulai game"""
        self.show_main_menu()
    
    def show_main_menu(self):
        """Tampilkan main menu"""
        while True:
            GameUI.print_main_menu()
            
            choice = GameUI.get_text_input("Pilih (1-3): ").strip()
            
            if choice == "1":
                self.start_new_game()
                break
            elif choice == "2":
                self.show_about()
            elif choice == "3":
                self.exit_game()
                return
            else:
                GameUI.print_error("Pilihan tidak valid!")
    
    def show_about(self):
        """Tampilkan layar tentang game"""
        GameUI.clear_screen()
        GameUI.print_header("TENTANG GAME")
        print("""
🔍 DETEKTIF PENGETAHUAN

Game mystery berbasis edukasi dimana Anda berperan sebagai detektif
yang harus memecahkan kasus misterius.

FITUR:
  • Investigasi lokasi dan wawancara saksi
  • Jawab pertanyaan edukatif untuk membuka bukti
  • Pilihan yang mempengaruhi alur cerita
  • Multiple endings berdasarkan performa Anda
  • Sistem inventory bukti yang mendalam

TIPS:
  • Kumpulkan sebanyak mungkin bukti
  • Pikirkan logis sebelum membuat keputusan
  • Setiap pilihan memiliki konsekuensi
  • Jawaban yang benar membuka informasi baru

Developer: Knowledge Detective Team
Version: 1.0.0
        """)
        GameUI.press_enter_to_continue()
    
    def start_new_game(self):
        """Mulai permainan baru"""
        try:
            # Load kasus
            if not self.game_manager.load_case('case_01'):
                GameUI.print_error("Gagal memuat kasus!")
                return
            
            # Inisialisasi managers
            self.story_manager = StoryManager(self.game_manager.case_data)
            self.question_manager = QuestionManager(self.game_manager.case_data)
            self.ending_manager = EndingManager(self.game_manager.case_data)
            
            GameUI.clear_screen()
            GameUI.print_header("🔍 DETEKTIF PENGETAHUAN")
            
            # Show opening narration
            print(f"\n{GameUI.Colors.CYAN}Kasus: {self.game_manager.case_data.get('title')}{GameUI.Colors.ENDC}\n")
            print(f"{self.game_manager.case_data.get('description')}\n")
            GameUI.press_enter_to_continue()
            
            # Main game loop
            self.game_loop()
            
        except Exception as e:
            GameUI.print_error(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def game_loop(self):
        """Main game loop"""
        self.running = True
        self.checkpoint_asked = False  # Reset checkpoint flag
        self.ending_reached = False  # Reset ending reached flag
        
        while self.running:
            try:
                # Cek apakah ada ending yang tercapai (bukan default failure)
                ending = self.ending_manager.evaluate_ending(self.game_manager)
                
                # Jika ending adalah ending "nyata" (bukan generic_failure) dan belum tanya checkpoint
                is_real_ending = ending and ending.get('id') != 'generic_failure'
                
                if is_real_ending and not self.checkpoint_asked:
                    # Tanyakan pertanyaan checkpoint sebelum ending
                    checkpoint_result = self.ask_checkpoint_question()
                    self.checkpoint_asked = True  # Tandai bahwa checkpoint sudah ditanya
                    
                    if checkpoint_result:
                        # Jika jawaban benar, tampilkan ending yang sebenarnya
                        self.show_ending(ending)
                    else:
                        # Jika jawaban salah, tampilkan failure ending
                        failure_ending = {
                            'type': 'failure',
                            'title': '❌ Penyelidikan Gagal!',
                            'text': 'Anda tidak mampu menjawab pertanyaan checkpoint. Bukti yang Anda kumpulkan ternyata tidak cukup untuk mengungkap kasus ini. Penyelidikan harus dihentikan.',
                            'rating': 'failure'
                        }
                        self.show_ending(failure_ending)
                    break
                
                # Tampilkan lokasi saat ini
                self.show_location_screen()
                
                # Minta aksi dari pemain
                self.handle_player_action()
                
            except KeyboardInterrupt:
                if GameUI.get_confirmation("Keluar dari game?"):
                    self.running = False
                    break
            except Exception as e:
                GameUI.print_error(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
    
    def show_location_screen(self):
        """Tampilkan screen lokasi saat ini"""
        GameUI.clear_screen()
        
        location_id = self.game_manager.current_location
        location_data = self.story_manager.get_location_data(location_id)
        
        if not location_data:
            GameUI.print_error("Lokasi tidak ditemukan!")
            return
        
        # Tampilkan info lokasi
        GameUI.print_location_info(
            location_data.get('name', location_id),
            location_data.get('description', '')
        )
        
        # Tampilkan inventory summary
        GameUI.print_inventory_summary(
            self.game_manager.player_evidence,
            self.game_manager.case_data
        )
        
        # Tampilkan NPC di lokasi
        npcs = self.story_manager.get_npcs_at_location(location_id, self.game_manager.player_flags)
        GameUI.print_npc_list(npcs)
        
        # Tampilkan pilihan aksi
        GameUI.print_location_actions(location_id, location_data.get('exits', {}))
    
    def handle_player_action(self):
        """Handle aksi pemain"""
        location_data = self.story_manager.get_location_data(self.game_manager.current_location)
        npcs = self.story_manager.get_npcs_at_location(self.game_manager.current_location, self.game_manager.player_flags)
        exits = location_data.get('exits', {})
        
        # Buat list pilihan
        options = [
            "Cari petunjuk",
            "Bicara dengan NPC",
            "Buka inventory",
            "Lihat catatan"
        ]
        
        if exits:
            for exit_name in exits.values():
                options.append(exit_name)
        
        # Minta pilihan
        choice_idx = GameUI.print_choices(options)
        
        if choice_idx == 0:
            self.action_search_clues()
        elif choice_idx == 1:
            self.action_talk_to_npc(npcs)
        elif choice_idx == 2:
            self.action_show_inventory()
        elif choice_idx == 3:
            self.action_show_notes()
        else:
            # Move to location
            exit_idx = choice_idx - 4
            exit_id = list(exits.keys())[exit_idx]
            self.game_manager.move_to_location(exit_id)
    
    def action_search_clues(self):
        """Handle aksi mencari petunjuk"""
        GameUI.print_narration("Anda mulai mencari petunjuk di lokasi ini...\n")
        
        # Simulasi menemukan petunjuk
        available_clues = [
            ("catatan_kepala", "Anda menemukan catatan dari kepala perpustakaan tentang pemeriksaan terakhir buku."),
            ("catatan_jam_jaga", "Anda menemukan catatan jam jaga penjaga malam."),
            ("timeline_kejadian", "Anda berhasil merekonstruksi timeline kejadian.")
        ]
        
        import random
        if random.random() < 0.5:
            clue_id, message = random.choice(available_clues)
            if self.game_manager.add_evidence(clue_id):
                GameUI.print_success(message)
            else:
                GameUI.print_warning("Anda sudah memiliki petunjuk ini.")
        else:
            GameUI.print_warning("Anda tidak menemukan petunjuk apapun di sini.")
        
        GameUI.press_enter_to_continue()
    
    def action_talk_to_npc(self, npcs: list):
        """Handle dialog dengan NPC"""
        if not npcs:
            GameUI.print_warning("Tidak ada NPC di lokasi ini.")
            GameUI.press_enter_to_continue()
            return
        
        # Pilih NPC
        npc_options = [npc['name'] for npc in npcs]
        npc_idx = GameUI.print_choices(npc_options)
        selected_npc = npcs[npc_idx]
        
        # Mulai dialog
        self.show_npc_dialogue(selected_npc['id'])
    
    def show_npc_dialogue(self, npc_id: str):
        """Tampilkan dan tangani dialog dengan NPC"""
        GameUI.clear_screen()
        
        characters = self.game_manager.case_data.get('characters', {})
        npc_data = characters.get(npc_id)
        
        if not npc_data:
            GameUI.print_error("NPC tidak ditemukan!")
            return
        
        # Tampilkan dialog pertama
        first_dialogue_id = npc_data.get('first_dialogue')
        dialogue = npc_data.get('dialogues', {}).get(first_dialogue_id, {})
        
        # Tampilkan dialog
        GameUI.print_dialogue(npc_data['name'], dialogue.get('text', ''))
        
        # Cek apakah ada soal dalam dialog ini
        question_id = dialogue.get('question')
        if question_id:
            self.handle_question(question_id)
        
        # Tampilkan pilihan dialog
        choices = dialogue.get('choices', [])
        if choices:
            choice_texts = [c.get('text', '') for c in choices]
            choice_idx = GameUI.print_choices(choice_texts)
            next_dialogue_id = choices[choice_idx].get('next')
            
            if next_dialogue_id:
                next_dialogue = npc_data.get('dialogues', {}).get(next_dialogue_id, {})
                GameUI.print_dialogue(npc_data['name'], next_dialogue.get('text', ''))
        
        GameUI.press_enter_to_continue()
    
    def handle_question(self, question_id: str):
        """Handle pertanyaan dari sistem"""
        question = self.question_manager.get_question(question_id)
        
        if not question:
            GameUI.print_error("Pertanyaan tidak ditemukan!")
            return
        
        GameUI.clear_screen()
        GameUI.print_question(question.get('text'), question.get('type'))
        
        question_type = question.get('type')
        
        if question_type == 'multiple_choice':
            # Handle multiple choice
            options = question.get('options', [])
            choice_idx = GameUI.print_choices(options)
            user_answer = options[choice_idx]
        else:
            # Handle short answer
            user_answer = GameUI.get_text_input("Jawaban Anda: ")
        
        # Validasi jawaban
        is_correct, result = self.question_manager.validate_answer(question_id, user_answer)
        
        if is_correct:
            GameUI.print_success("Jawaban Anda benar!")
        else:
            GameUI.print_error("Jawaban Anda salah. Coba lagi nanti.")
        
        # Apply hasil
        self.question_manager.apply_result(result, self.game_manager)
        
        # Tambah bukti jika ada
        for evidence_id in result.get('evidence', []):
            self.game_manager.add_evidence(evidence_id)
        
        GameUI.press_enter_to_continue()
    
    def action_show_inventory(self):
        """Tampilkan inventory"""
        GameUI.clear_screen()
        GameUI.print_header("📦 INVENTORY BUKTI")
        
        if not self.game_manager.player_evidence:
            print("\nInventory kosong.\n")
        else:
            clues = self.game_manager.case_data.get('clues', {})
            for i, evidence_id in enumerate(self.game_manager.player_evidence, 1):
                clue = clues.get(evidence_id, {})
                print(f"\n{i}. {clue.get('name', evidence_id)}")
                print(f"   Kategori: {clue.get('category', 'Unknown')}")
                print(f"   {clue.get('description', '')}")
        
        print()
        GameUI.press_enter_to_continue()
    
    def action_show_notes(self):
        """Tampilkan catatan penyelidikan"""
        GameUI.clear_screen()
        GameUI.print_header("📝 CATATAN PENYELIDIKAN")
        
        print(f"\nPilihan Kritis yang Dibuat: {len(self.choice_tracker.choices_made)}")
        print(f"Total Bukti: {len(self.game_manager.player_evidence)}")
        print(f"Flag yang Diset: {len(self.game_manager.player_flags)}")
        
        if self.question_manager:
            stats = self.question_manager.get_question_stats()
            print(f"\nStatistik Pertanyaan:")
            print(f"  Total: {stats['total_questions']}")
            print(f"  Benar: {stats['correct_answers']}")
            print(f"  Salah: {stats['wrong_answers']}")
            print(f"  Akurasi: {stats['accuracy']:.1f}%")
        
        print()
        GameUI.press_enter_to_continue()
    
    def ask_checkpoint_question(self):
        """Tanyakan pertanyaan checkpoint sebelum ending
        
        Returns:
            bool: True jika jawaban benar, False jika salah
        """
        GameUI.clear_screen()
        GameUI.print_header("🎯 PERTANYAAN FINAL CHECKPOINT")
        
        print("\nSebelum kasus ini selesai, Anda harus menjawab satu pertanyaan terakhir untuk membuktikan kemampuan Anda!\n")
        GameUI.press_enter_to_continue()
        
        # Ambil 2 pertanyaan matematika (penjumlahan dan pengurangan)
        math_questions = ['q_penjumlahan', 'q_pengurangan']
        correct_answers = 0
        
        for q_id in math_questions:
            GameUI.clear_screen()
            question_data = self.question_manager.get_question(q_id)
            
            if not question_data:
                continue
            
            GameUI.print_header("🎯 PERTANYAAN CHECKPOINT")
            print(f"\n{question_data['text']}\n")
            
            if question_data['type'] == 'multiple_choice':
                options = question_data.get('options', [])
                choice_idx = GameUI.print_choices(options)
                answer = options[choice_idx]
                
                # Validasi jawaban dan apply result
                is_correct, result = self.question_manager.validate_answer(q_id, answer)
                
                if is_correct:
                    GameUI.print_success("\n✓ Jawaban Benar!")
                    # Apply result (unlock evidence, set flags from on_correct)
                    self.question_manager.apply_result(result, self.game_manager)
                    
                    # Set flag untuk tracking checkpoint success
                    if q_id == 'q_penjumlahan':
                        self.game_manager.set_flag('checkpoint_penjumlahan_correct', True)
                    elif q_id == 'q_pengurangan':
                        self.game_manager.set_flag('checkpoint_pengurangan_correct', True)
                    
                    correct_answers += 1
                else:
                    GameUI.print_error("\n✗ Jawaban Salah!")
                    # Apply result (on_incorrect effects if any)
                    self.question_manager.apply_result(result, self.game_manager)
                    # Set flag untuk tracking checkpoint failure
                    if q_id == 'q_penjumlahan':
                        self.game_manager.set_flag('checkpoint_penjumlahan_correct', False)
                    elif q_id == 'q_pengurangan':
                        self.game_manager.set_flag('checkpoint_pengurangan_correct', False)
                
                # Show result message
                if is_correct and question_data.get('on_correct'):
                    print(question_data['on_correct']['message'])
                elif not is_correct and question_data.get('on_incorrect'):
                    print(question_data['on_incorrect']['message'])
            
            GameUI.press_enter_to_continue()
        
        # Perlu jawab minimal 1 pertanyaan dengan benar untuk lanjut
        return correct_answers > 0
    
    def show_ending(self, ending_data: dict):
        """Tampilkan ending screen"""
        GameUI.clear_screen()
        
        stats = self.ending_manager.get_playthrough_stats(
            self.game_manager,
            self.question_manager
        )
        
        GameUI.print_ending_screen(ending_data, stats)
        
        # Tanya apakah mau mainkan lagi
        print()
        if GameUI.get_confirmation("Ingin bermain lagi?"):
            self.start_new_game()
        else:
            print()
            GameUI.print_success("Terima kasih telah bermain Detektif Pengetahuan!")
            self.running = False
    
    def exit_game(self):
        """Keluar dari game"""
        GameUI.clear_screen()
        print(f"\n{GameUI.Colors.CYAN}Terima kasih telah bermain Detektif Pengetahuan!{GameUI.Colors.ENDC}\n")
        sys.exit(0)


def main():
    """Entry point"""
    game = GameLoop()
    game.start()


if __name__ == "__main__":
    main()
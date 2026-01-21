# 🔍 Detektif Pengetahuan - Knowledge Detective Game Engine

Game mystery berbasis edukasi dengan sistem story-driven, choice-based, dan data-driven. Pemain berperan sebagai detektif yang memecahkan kasus misterius melalui investigasi, analisis logika, dan menjawab pertanyaan edukatif.

## 🎮 Fitur Utama

### Story-Driven & Choice-Based
- **Cerita Bercabang**: Pilihan pemain mempengaruhi alur cerita
- **Multiple Endings**: 4+ tipe ending (Failure, Partial Success, Success, Brilliant)
- **Flag System**: Tracking pilihan dan keputusan pemain
- **Dynamic Dialogue**: Dialog berubah berdasarkan kondisi dan bukti

### Education-Focused
- **Soal Interaktif**: Multiple choice, short answer, logic questions
- **Reward System**: Jawaban benar membuka bukti dan informasi baru
- **Consequence-Based**: Jawaban salah dapat mengubah alur cerita
- **Knowledge Integration**: Bahasa, logika, dan pengetahuan umum

### Evidence Management
- **Inventory System**: Kumpulkan bukti untuk mendukung teori
- **Categorization**: Bukti fisik, testimoni, dokumen
- **Requirement Checking**: Beberapa ending butuh bukti tertentu
- **Visual Summary**: Tampilkan bukti yang sudah dikumpulkan

### Flexible & Extensible
- **Data-Driven**: Semua konten berbasis JSON (mudah tambah kasus baru)
- **Modular Architecture**: Core systems terpisah dan reusable
- **Condition System**: Kompleks logic untuk state management
- **Easy Content Creation**: Format data yang jelas dan terstruktur

## 📂 Struktur Proyek

```
Program-1/
├── core/                          # Core game systems
│   ├── game_manager.py           # Pengelola state game utama
│   ├── story_manager.py          # Manajemen cerita & dialog
│   ├── question_manager.py       # Sistem pertanyaan & validasi
│   ├── choice_tracker.py         # Tracking pilihan pemain
│   ├── ending_manager.py         # Evaluasi & manajemen ending
│   └── __init__.py
│
├── systems/                       # Game systems
│   ├── evidence_inventory.py     # Inventory bukti
│   ├── dialogue_system.py        # Sistem dialog NPC
│   ├── condition_checker.py      # Evaluator kondisi kompleks
│   └── __init__.py
│
├── ui/                            # User Interface
│   ├── game_ui.py                # Text-based UI components
│   └── __init__.py
│
├── data/                          # Game data
│   └── cases/
│       └── case_01.json          # Demo case: Pencurian Perpustakaan
│
├── main.py                        # Game loop & entry point
└── DOCUMENTATION.md               # Dokumentasi lengkap
```

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.7+

### Menjalankan Game
```bash
cd /workspaces/Program-1
python main.py
```

### Main Menu
1. **Mulai Game Baru** - Mainkan kasus demo
2. **Tentang Game** - Info tentang game
3. **Keluar** - Exit

## 🎯 Game Flow

```
┌─────────────────────────────────────────────────────────┐
│ LOAD KASUS (JSON)                                       │
│ Inisialisasi GameManager, StoryManager, Questions      │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ TAMPILKAN LOKASI & DESKRIPSI                           │
│ • Info lokasi                                           │
│ • NPC yang ada                                          │
│ • Inventory summary                                     │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ PEMAIN MEMILIH AKSI                                    │
│ • Cari petunjuk                                         │
│ • Bicara dengan NPC                                     │
│ • Buka inventory                                        │
│ • Pindah lokasi                                         │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    [Soal?]            [Dialog?]
         │                   │
    VALIDASI          UNLOCK INFO
    JAWABAN               │
         │                │
      HASIL ◄─────────────┤
         │                │
    ┌────▼────┐          │
    │ CORRECT │          │
    ├─────────┤          │
    │Add      │          │
    │Evidence │          │
    │Set Flags│          │
    │  etc    │          │
    └────┬────┘          │
         │               │
         └───────┬───────┘
                 │
         UPDATE GAME STATE
                 │
         ┌───────▼────────────┐
         │ CEK ENDING         │
         │ CONDITION          │
         └───────┬────────────┘
                 │
          [Ending Met?]
                 │
        ┌────────┴────────┐
        │                 │
       YES               NO
        │                 │
    SHOW ENDING      LOOP KEMBALI
        │                 │
        └────────┬────────┘
                 │
           GAME END / REPLAY
```

## 📖 Core Systems

### 1. GameManager
**File**: [core/game_manager.py](core/game_manager.py)

Pengelola state game utama, tracking bukti, flag, dan kondisi ending.

**Metode Utama**:
```python
game = GameManager()

# Load kasus
game.load_case('case_01')

# Track pilihan
game.set_flag('percaya_penjaga', True)
game.get_flag('percaya_penjaga')

# Manage bukti
game.add_evidence('catatan_kepala')
game.has_evidence('catatan_kepala')  # True
game.get_evidence_count()

# Cek lokasi
game.move_to_location('ruang_arsip')
game.current_location  # 'ruang_arsip'

# Cek ending
ending_id = game.check_ending_condition()
```

### 2. StoryManager
**File**: [core/story_manager.py](core/story_manager.py)

Manajemen cerita, dialog, dan kondisi untuk branching narrative.

**Metode Utama**:
```python
story = StoryManager(case_data)

# Ambil info lokasi
location = story.get_location_data('perpustakaan_utama')

# Ambil scene berdasarkan kondisi
scene = story.get_scene('scene_office', flags={'kepala_trust': True})

# Ambil NPC tersedia dengan kondisi
npcs = story.get_npcs_at_location('perpustakaan_utama', flags)

# Ambil dialog NPC
dialogue = story.get_dialogue('kepala_perpustakaan', 'kepala_hello', flags)
available_dialogues = story.get_available_dialogues('kepala_perpustakaan', flags)

# Track scene yang sudah dikunjungi
story.mark_scene_visited('scene_first')
```

### 3. QuestionManager
**File**: [core/question_manager.py](core/question_manager.py)

Sistem pertanyaan, validasi jawaban, dan reward system.

**Metode Utama**:
```python
questions = QuestionManager(case_data)

# Ambil pertanyaan
q = questions.get_question('q_alibi_definition')

# Validasi jawaban
is_correct, result = questions.validate_answer(
    'q_alibi_definition', 
    'bukti kehadiran di tempat lain'
)

# Apply hasil ke game state
questions.apply_result(result, game_manager)

# Ambil statistik
stats = questions.get_question_stats()
# {
#   'total_questions': 5,
#   'correct_answers': 3,
#   'accuracy': 60.0
# }

# Cek apakah sudah menjawab
if questions.has_answered_question('q_alibi_definition'):
    last_result = questions.get_last_answer_result('q_alibi_definition')
```

### 4. EvidenceInventory
**File**: [systems/evidence_inventory.py](systems/evidence_inventory.py)

Manajemen inventory bukti dengan categorization.

**Metode Utama**:
```python
inventory = EvidenceInventory()

# Buat bukti
evidence = Evidence(
    'catatan_kepala',
    'Catatan Kepala',
    'Catatan pemeriksaan buku terakhir',
    'document'
)

# Tambah ke inventory
inventory.add_evidence(evidence, location='perpustakaan_utama')

# Cek dan ambil
if inventory.has_evidence('catatan_kepala'):
    e = inventory.get_evidence('catatan_kepala')

# Ambil by kategori
docs = inventory.get_evidence_by_category('document')

# Display inventory
print(inventory.display_inventory())
```

### 5. ConditionChecker
**File**: [systems/condition_checker.py](systems/condition_checker.py)

Evaluator untuk kondisi kompleks, flag, dan bukti.

**Metode Utama**:
```python
from systems.condition_checker import ConditionChecker, Condition, ComplexCondition

checker = ConditionChecker()

# Cek flag value
if checker.check_flag_value(game, 'percaya_penjaga', True):
    print("Pemain percaya penjaga")

# Cek multiple flags (AND logic)
if checker.check_multiple_flags(game, {
    'flag1': True,
    'flag2': False
}):
    print("Semua flag sesuai")

# Cek evidence
if checker.check_evidence_requirements(game, ['catatan_kepala', 'timeline']):
    print("Semua bukti lengkap")

# Cek evidence count range
if checker.check_evidence_count_range(game, min_count=3, max_count=5):
    print("Bukti dalam range")

# Create complex condition
complex_cond = ComplexCondition("AND")
complex_cond.add_condition(
    Condition("flag", "percaya_penjaga", True)
)
complex_cond.add_condition(
    Condition("evidence", "catatan_kepala")
)
if complex_cond.evaluate(game):
    print("Kondisi kompleks terpenuhi")
```

### 6. EndingManager
**File**: [core/ending_manager.py](core/ending_manager.py)

Evaluasi dan manajemen ending game.

**Metode Utama**:
```python
ending_mgr = EndingManager(case_data)

# Evaluasi ending berdasarkan state
ending = ending_mgr.evaluate_ending(game)
# {
#   'id': 'brilliant_ending',
#   'type': 'brilliant',
#   'title': '🏆 Detektif Jenius!',
#   'text': '...',
#   'required_evidence': [...],
#   ...
# }

# Cek tipe ending
if ending_mgr.is_brilliant_ending():
    print("Sempurna!")

# Ambil rating
rating = ending_mgr.get_ending_rating()
# {
#   'emoji': '🏆',
#   'text': 'Detektif Jenius!',
#   'color': 'gold'
# }

# Ambil stats lengkap
stats = ending_mgr.get_playthrough_stats(game, question_mgr)
```

## 📊 Demo Kasus: Pencurian di Perpustakaan Kota

### 🔍 Premis
Buku kuno sejarah kota hilang semalam sebelum pameran besar. Pemain harus menemukan siapa pelakunya melalui investigasi lokasi, wawancara saksi, dan menjawab pertanyaan edukatif.

### 📍 Lokasi (3 tempat)

| Lokasi | Deskripsi | NPC | Aksi |
|---|---|---|---|
| **Perpustakaan Utama** | Ruang baca dengan rak buku tinggi | Kepala Perpustakaan, Penjaga Malam | Cari petunjuk, Bicara |
| **Ruang Arsip** | Ruang khusus dengan buku kuno | Mahasiswa Peneliti | Cari dokumen |
| **Kantor Kepala** | Kantor elegan dengan meja kerja | Kepala Perpustakaan | Investigasi |

### 🧑 Karakter (3 NPC)

| NPC | Peran | Status | Key Info |
|---|---|---|---|
| **Ibu Sita Dewi** | Kepala Perpustakaan | Cemas & profesional | Tahu tentang buku, punya kunci |
| **Pak Ahmad** | Penjaga Malam | Gelisah & lelah | Melihat mahasiswa datang jam 10 |
| **Rani Wijaya** | Mahasiswa Peneliti | Gugup & terlihat cerdas | Sering bekerja malam, riset skripsi |

### ❓ Pertanyaan Edukatif (3 soal)

| ID | Pertanyaan | Tipe | Jawaban Benar | Reward |
|---|---|---|---|---|
| q_alibi_definition | Apa arti "alibi"? | Short Answer | bukti kehadiran di tempat lain | catatan_kepala |
| q_jam_jaga | Jika penjaga jam 8-5 dan mahasiswa jam 10, siapa lihatnya? | Multiple | Hanya penjaga malam | catatan_jam_jaga |
| q_logika_waktu | Kapan kemungkinan buku diambil? | Logic | Malam hari (8-5 pagi) | timeline_kejadian |

### 🎬 Ending Options (4 tipe)

| Ending | Tipe | Syarat | Description | Emoji |
|---|---|---|---|---|
| **Detektif Jenius** | brilliant | 4+ bukti + semua flag OK | Solusi sempurna, pelaku tertangkap | 🏆 |
| **Kesuksesan** | success | 3 bukti tertentu | Sukses normal tapi ada detail terlewat | ✅ |
| **Sukses Parsial** | partial_success | 1-2 bukti | Bukti kurang meyakinkan, kasus terbuka | ⚖️ |
| **Gagal** | failure | 0 bukti | Pelaku lolos, investigasi gagal | ❌ |

## 🛠 Cara Menambah Kasus Baru

### Step 1: Copy Template
```bash
cp data/cases/case_01.json data/cases/case_02.json
```

### Step 2: Edit Metadata
```json
{
  "case_id": "case_02",
  "title": "Judul Kasus Baru",
  "description": "Deskripsi singkat kasus...",
  "start_location": "lokasi_awal"
}
```

### Step 3: Tambah Lokasi
```json
"locations": {
  "lokasi_id": {
    "name": "Nama Lokasi",
    "description": "Deskripsi panjang",
    "scenes": ["scene_1", "scene_2"],
    "npcs": ["npc_1", "npc_2"],
    "exits": {
      "lokasi_lain": "Menuju Lokasi Lain"
    }
  }
}
```

### Step 4: Tambah Karakter
```json
"characters": {
  "npc_id": {
    "name": "Nama NPC",
    "role": "Peran",
    "description": "Deskripsi",
    "first_dialogue": "dialog_awal",
    "dialogues": {
      "dialog_id": {
        "text": "Teks dialog",
        "choices": [
          {"text": "Pilihan 1", "next": "dialog_next"}
        ],
        "question": "q_id_optional"
      }
    }
  }
}
```

### Step 5: Tambah Pertanyaan
```json
"questions": {
  "q_id": {
    "type": "short_answer|multiple_choice|logic",
    "text": "Pertanyaan?",
    "correct_answer": "Jawaban benar",
    "options": ["opt1", "opt2"],  // untuk multiple_choice
    "on_correct": {
      "evidence": ["bukti_id"],
      "flags": {"flag": true},
      "message": "Benar!"
    },
    "on_incorrect": {
      "message": "Salah."
    }
  }
}
```

### Step 6: Tambah Bukti
```json
"clues": {
  "bukti_id": {
    "name": "Nama Bukti",
    "description": "Deskripsi",
    "category": "document|physical|testimony",
    "unlock_requirement": {
      "question_id": "q_id"
    }
  }
}
```

### Step 7: Definisikan Ending
```json
"endings": [
  {
    "id": "ending_id",
    "type": "brilliant|success|partial_success|failure",
    "title": "Judul Ending",
    "text": "Deskripsi ending...",
    "required_evidence": ["bukti_1", "bukti_2"],
    "conditions": {"flag_1": true, "flag_2": false},
    "min_evidence": 4
  }
]
```

### Step 8: Update main.py
```python
# Di method start_new_game()
if not self.game_manager.load_case('case_02'):
    GameUI.print_error("Gagal memuat kasus!")
    return
```

## 🎓 Pembelajaran dari Game

### Aspek Edukasi
- **Bahasa**: Vocabulary (alibi, bukti, deduksi, kesimpulan)
- **Logika**: Deductive reasoning, timeline analysis, cause-effect
- **Pengetahuan Umum**: Prosedur investigasi, hukum dasar
- **Critical Thinking**: Analisis bukti, evaluasi testimoni, motif
- **Decision Making**: Pilihan punya konsekuensi jangka panjang

### Game Pedagogy
1. **Eksploration-Based Learning**: Pemain aktif menggali informasi
2. **Problem-Solving**: Harus analyze dan connect bukti
3. **Consequence Learning**: Tahu akibat pilihan buruk
4. **Multiple Pathways**: Berbagai cara mencapai kesuksesan

## 🔧 Extensibility

### Tambah Tipe Pertanyaan
```python
# Di question_manager.py validate_answer()
elif question_type == 'matching':
    # Custom validation logic
    is_correct = validate_matching(user_answer)
```

### Tambah Sistem Baru
```python
# Buat file di systems/
class NewSystem:
    def __init__(self, case_data):
        self.data = case_data
    
    def process(self, game_manager):
        # Logic
        pass
```

### Customize UI
```python
# Di ui/game_ui.py
class GameUI:
    class Colors:
        CUSTOM = '\033[38;5;196m'
    
    @staticmethod
    def print_custom(text):
        print(f"{GameUI.Colors.CUSTOM}{text}{GameUI.Colors.ENDC}")
```

## 🚀 Future Enhancements

- [ ] Save/Load Game State
- [ ] Hint System untuk pertanyaan
- [ ] Achievement/Badge System
- [ ] Point/Score Calculation
- [ ] Multiple Cases Selection Menu
- [ ] Dialogue History Viewer
- [ ] Evidence Connection Diagram
- [ ] Character Relationship Tracker
- [ ] GUI Version (Tkinter/PyGame)
- [ ] Audio/Background Music
- [ ] More Demo Cases (10+)
- [ ] Difficulty Levels
- [ ] Multiplayer/Collaborative Mode

## 📝 Lisensi

Educational Game - Free to Use and Modify for Educational Purposes

---

**Versi**: 1.0.0  
**Status**: Fully Functional Demo  
**Python**: 3.7+  
**Last Updated**: January 21, 2026

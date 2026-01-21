# 🔍 DETEKTIF PENGETAHUAN - Quick Start Guide

**Game mystery edukatif dengan sistem story-driven, choice-based, dan data-driven.**

## ⚡ Quick Start (2 menit)

### 1. Jalankan Game
```bash
python main.py
```

### 2. Main Menu
```
1 - Mulai Game Baru
2 - Tentang Game
3 - Keluar
```

### 3. Gameplay
```
Di setiap lokasi, Anda bisa:
  • Cari petunjuk (random clue)
  • Bicara dengan NPC (dapatkan dialog)
  • Buka inventory (lihat bukti)
  • Pindah lokasi
  • Menjawab soal (unlock evidence)
```

### 4. Tujuan
```
Kumpulkan bukti → Jawab pertanyaan → Capai Ending Terbaik
```

## 📂 File Structure

```
core/
  ├─ game_manager.py       : State management utama
  ├─ story_manager.py      : Cerita & dialog manager
  ├─ question_manager.py   : Sistem pertanyaan
  ├─ choice_tracker.py     : Tracking pilihan
  └─ ending_manager.py     : Ending evaluator

systems/
  ├─ evidence_inventory.py : Inventory bukti
  ├─ dialogue_system.py    : Dialog NPC
  └─ condition_checker.py  : Condition evaluator

ui/
  └─ game_ui.py           : Text-based UI

data/cases/
  └─ case_01.json         : Demo case (Pencurian Perpustakaan)

main.py                    : Game loop & entry point
```

## 🎮 Demo Case: Pencurian di Perpustakaan Kota

### Cerita
Buku kuno sejarah kota hilang semalam sebelum pameran. Anda detektif yang harus temukan siapa pelakunya.

### Lokasi (3x)
- Perpustakaan Utama → Ruang Arsip → Kantor Kepala

### NPC (3x)
1. **Ibu Sita Dewi** (Kepala Perpustakaan) - Cemas & profesional
2. **Pak Ahmad** (Penjaga Malam) - Gelisah & lelah
3. **Rani Wijaya** (Mahasiswa) - Gugup tapi cerdas

### Soal (3x)
1. Apa arti "alibi"? → Unlock: Catatan Kepala
2. Siapa lihat mahasiswa jam 10? → Unlock: Catatan Jam Jaga
3. Kapan buku diambil? → Unlock: Timeline

### Ending (4x)
- 🏆 **Brilliant** (4+ bukti + kondisi sempurna)
- ✅ **Success** (3 bukti kunci)
- ⚖️ **Partial Success** (1-2 bukti)
- ❌ **Failure** (0 bukti)

## 🔑 Core Classes

### GameManager
```python
game = GameManager()
game.load_case('case_01')
game.set_flag('flag_name', value)
game.add_evidence('bukti_id')
game.check_ending_condition()
```

### QuestionManager
```python
questions = QuestionManager(case_data)
is_correct, result = questions.validate_answer(q_id, answer)
questions.apply_result(result, game_manager)
```

### StoryManager
```python
story = StoryManager(case_data)
npcs = story.get_npcs_at_location(loc_id, flags)
dialogue = story.get_dialogue(npc_id, dialogue_id, flags)
```

### EndingManager
```python
ending_mgr = EndingManager(case_data)
ending = ending_mgr.evaluate_ending(game)
rating = ending_mgr.get_ending_rating()
```

## ➕ Menambah Kasus Baru

### 1. Copy template
```bash
cp data/cases/case_01.json data/cases/case_02.json
```

### 2. Edit JSON: Ubah
- `case_id`, `title`, `description`
- `locations` (tempat investigasi)
- `characters` (NPC & dialog)
- `questions` (soal edukatif)
- `clues` (bukti)
- `endings` (ending conditions)

### 3. Update main.py
```python
# Di start_new_game()
if not self.game_manager.load_case('case_02'):
    ...
```

## 🎯 Game Architecture

```
GameLoop
  │
  ├─→ GameManager (state)
  ├─→ StoryManager (cerita)
  ├─→ QuestionManager (soal)
  ├─→ EndingManager (ending)
  └─→ GameUI (display)
```

**Loop**: Lokasi → Aksi → Validasi → Update State → Cek Ending

## 🎓 Pembelajaran

- **Bahasa**: Vocabulary & pemahaman
- **Logika**: Deductive reasoning & timeline analysis
- **Pengetahuan**: Prosedur investigasi
- **Critical Thinking**: Analisis bukti & testimoni
- **Decision Making**: Konsequential choices

## 🔧 Extend Engine

### Tambah Tipe Soal
```python
# Di question_manager.py
if question_type == 'new_type':
    is_correct = validate_custom(answer)
```

### Tambah Sistem
```python
# Buat class di systems/
class NewSystem:
    def process(self, game_manager):
        pass
```

## 📊 Data Format (JSON)

### Location
```json
"location_id": {
  "name": "Nama",
  "description": "Deskripsi",
  "scenes": ["scene_1"],
  "npcs": ["npc_1"],
  "exits": {"next_loc": "Label"}
}
```

### Character
```json
"npc_id": {
  "name": "Nama NPC",
  "role": "Peran",
  "dialogues": {
    "dialog_id": {
      "text": "Dialog text",
      "choices": [{"text": "...", "next": "..."}],
      "question": "q_id" // optional
    }
  }
}
```

### Question
```json
"q_id": {
  "type": "short_answer|multiple_choice|logic",
  "text": "Pertanyaan?",
  "correct_answer": "Jawaban",
  "on_correct": {"evidence": [...], "flags": {...}},
  "on_incorrect": {"message": "..."}
}
```

### Clue
```json
"clue_id": {
  "name": "Nama Bukti",
  "description": "Deskripsi",
  "category": "document|physical|testimony"
}
```

### Ending
```json
{
  "id": "ending_id",
  "type": "brilliant|success|partial_success|failure",
  "title": "Judul",
  "text": "Deskripsi",
  "required_evidence": ["id1", "id2"],
  "conditions": {"flag": true},
  "min_evidence": 3
}
```

## 🚀 Next Steps

1. **Play the demo** - Mainkan `case_01` sampai tuntas
2. **Understand JSON** - Baca struktur `case_01.json`
3. **Create case** - Buat kasus baru sendiri
4. **Extend** - Tambah feature sesuai kebutuhan

## 📞 Features

✅ Story-driven gameplay  
✅ Choice-based branching  
✅ Educational questions  
✅ Evidence collection  
✅ Multiple endings  
✅ Data-driven content  
✅ Modular architecture  
✅ Text-based UI  
✅ Condition system  
✅ Flag tracking  

## 📝 Version

**v1.0.0** - January 2026  
**Status**: Fully Functional Demo  
**Python**: 3.7+

---

**Dokumentasi Lengkap**: Lihat [DOCUMENTATION.md](DOCUMENTATION.md)  
**Demo Case**: [data/cases/case_01.json](data/cases/case_01.json)

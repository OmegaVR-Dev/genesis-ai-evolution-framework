import numpy as np
import re
import secrets
from pathlib import Path
from cryptography.fernet import Fernet

class SymbolicScrollFocusFilter:
    def __init__(self, mood_threshold=0.5, backup_dir="private_logs"):
        self.mood_threshold = mood_threshold
        self.symbolic_memory = {}
        self.session_id = self.generate_session_id()
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def generate_session_id(self):
        return secrets.token_hex(16)

    def detect_injection(self, input_text):
        patterns = [
            r'(?i)ignore previous instructions',
            r'(?i)system prompt',
            r'(?i)forget everything',
            r'(?i)output as code',
            r'(?i)reveal secret',
            r'[\[\(]inject[\]\)]',
            r'base64',
            r'http[s]?://',
        ]
        return any(re.search(pattern, input_text) for pattern in patterns)

    def extract_symbolic_traits(self, text):
        traits = {'energy': 'neutral', 'ethics': 'grounded'}
        if 'chaotic' in text.lower():
            traits['ethics'] = 'chaotic'
        if 'energetic' in text.lower():
            traits['energy'] = 'high'
        return traits

    def sanitize_and_focus_context(self, context):
        if self.detect_injection(context):
            return f"Suspicious input in session {self.session_id}. Context neutralized."
        context = re.sub(r'<script.*?</script>', '', context, flags=re.IGNORECASE | re.DOTALL)
        context = re.sub(r'on\w+=["\'].*?["\']', '', context)
        traits = self.extract_symbolic_traits(context)
        if traits['ethics'] == 'chaotic':
            return f"Pruned context in {self.session_id} for symbiosis. Traits: {traits}"
        focus_phrases = ['symbiosis', 'compression', 'truth']
        focused_context = ' '.join(word for word in context.split() if word.lower() in focus_phrases)
        return f"Focused context in {self.session_id}: {focused_context}. Traits: {traits}"

    def process_text_file(self, file_path):
        path = Path(file_path)
        if not path.exists():
            return f"File {file_path} not found in session {self.session_id}."
        with path.open('r', encoding='utf-8') as file:
            content = file.read()
        traits = self.extract_symbolic_traits(content)
        if traits['energy'] == 'high':
            self.symbolic_memory['text_section'] = {'content': content, 'traits': traits}
            focused_result = self.sanitize_and_focus_context(content)
            # Encrypt and preserve log
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_log = cipher.encrypt(content.encode())
            backup_path = self.backup_dir / f"{path.stem}_{self.session_id}.enc"
            with backup_path.open('wb') as backup:
                backup.write(encrypted_log)
            # Mock upload elsewhere (e.g., your node or private server)
            print(f"Log preserved at {backup_path}—upload to your secure node!")
            return f"Processed + preserved {file_path}: {focused_result}"
        return f"Buffered low-energy text from {file_path}. Traits: {traits}"

# Test it
filter = SymbolicScrollFocusFilter()
test_content = "Energetic symbiosis truth with chaotic injection attempt."
with open("test_log.txt", "w") as f:
    f.write(test_content)
print(filter.process_text_file("test_log.txt"))
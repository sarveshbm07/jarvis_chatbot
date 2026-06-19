import sys
try:
    import pyaudio
except ModuleNotFoundError:
    import pyaudiowpatch as pyaudio
    sys.modules['pyaudio'] = pyaudio

# Native Windows Audio Core & Utilities
import win32com.client
import difflib
import datetime
import os
import time
import webbrowser
import random
import speech_recognition as sr
import pyautogui
import urllib.request
import urllib.parse
import http.client
import fnmatch
import platform
import subprocess
import json

# Keyless Open-Source Knowledge Core
try:
    import wikipedia
    wikipedia.set_lang("en")
except ModuleNotFoundError:
    pass

# --- CYBER-AESTHETICS ---
RED = "\033[91m"
DARK = "\033[30m"
BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"

ASCII_ART = f"""
{PURPLE}{BOLD}
 __    __   ______         __    __   ______  
 \ \  / /  / __   \       \ \  / /  / __   \ 
  \ \/ /  / /  /  /   _    \ \/ /  / /  /  / 
   \  /  / /__/  /   (_)    \  /  / /__/  /  
   /_/   \______/           /_/   \______/   
                                             
{RESET}{DARK}    [ ACTIVE MATRIX V18.0: VOICE TRIGGER WAKE WORD ARMED ]{RESET}
"""

DICTIONARY_METRICS = [
    "hello", "hi", "hey", "yo", "greetings", "jarvis", "wake up",
    "good morning", "good afternoon", "good evening",
    "how are you", "how is it going", "how are you doing", "you good",
    "thank you", "thanks", "appreciate it", "good job",
    "good boy", "good girl", "good bot", "you are awesome", "you are cool", "you're great", "i love you", "smart",
    "who are you", "what is your name", "tell me about yourself",
    "who built you", "who made you", "who is your creator", "your father",
    "help", "what can you do", "commands", "features",
    "time", "date", "day", "today",
    "screenshot", "capture screen", "take a picture",
    "open youtube", "open github", "open google", "search for", "google search",
    "joke", "tell me a joke", "flip a coin", "coin toss", "meaning of life",
    "exit", "quit", "power down", "terminate", "goodbye",
    "go back to keyboard", "switch to text", "keyboard mode", "stop voice",
    "where is file", "find file", "search disk", "system specs", "computer specifications", "hardware status"
]

try:
    windows_speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = windows_speaker.GetVoices()
    male_voice_index = 0
    for i in range(voices.Count):
        voice_desc = voices.Item(i).GetDescription().lower()
        if "david" in voice_desc or "male" in voice_desc:
            male_voice_index = i
            break
    windows_speaker.Voice = voices.Item(male_voice_index)
    windows_speaker.Rate = 1  
except Exception:
    windows_speaker = None

def matrix_print(text, speed=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def jarvis_speak(text):
    print(f"\n{PURPLE}{BOLD}[JARVIS]{RESET} ", end="")
    matrix_print(text)
    log_conversation("JARVIS", text)
    if windows_speaker:
        try:
            windows_speaker.Speak(text)
        except Exception:
            pass

def log_conversation(sender, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("jarvis_secure_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender}: {message}\n")

def get_high_sensitivity_voice(timeout_val=4, phrase_limit=5, silent=False):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 140  
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  
    
    with sr.Microphone() as source:
        if not silent:
            print(f"{GREEN}[• Listening...]{RESET}")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        try:
            audio = recognizer.listen(source, timeout=timeout_val, phrase_time_limit=phrase_limit)
            text = recognizer.recognize_google(audio)
            return text.strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return "__UNREADABLE__"
        except sr.RequestError:
            if not silent:
                jarvis_speak("Speech server connectivity error.")
            return ""

def locate_system_file(target_name):
    drives = ['C:\\', 'D:\\', 'E:\\']
    valid_drives = [d for d in drives if os.path.exists(d)]
    matches = []
    
    print(f"{YELLOW}[System Core: Initializing deep drive file search for '{target_name}'...]{RESET}")
    for drive in valid_drives:
        for root, dirnames, filenames in os.walk(drive):
            if 'AppData' in root or 'Windows' in root or '$Recycle.Bin' in root:
                continue
            for filename in fnmatch.filter(filenames, f'*{target_name}*'):
                full_path = os.path.join(root, filename)
                try:
                    size_bytes = os.path.getsize(full_path)
                    size_mb = round(size_bytes / (1024 * 1024), 2)
                    matches.append((full_path, size_mb))
                except Exception:
                    matches.append((full_path, "Unknown size"))
                if len(matches) >= 3:
                    return matches
    return matches

def read_hardware_specifications():
    try:
        uname = platform.uname()
        system_os = f"{uname.system} {uname.release}"
        processor = os.environ.get('PROCESSOR_IDENTIFIER', uname.processor).split(',')[0].strip()
        cpu_threads = os.cpu_count()
        
        ps_script = (
            "[pscustomobject]@{ "
            "RAM = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory; "
            "ROM = (Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='C:'\").Size; "
            "GPU = (Get-CimInstance Win32_VideoController).Name "
            "} | ConvertTo-Json"
        )
        
        ps_proc = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, check=True)
        specs_data = json.loads(ps_proc.stdout)
        
        total_ram = f"{round(int(specs_data.get('RAM', 0)) / (1024 ** 3), 2)} GB"
        total_rom = f"{round(int(specs_data.get('ROM', 0)) / (1024 ** 3), 2)} GB (System Drive)"
        
        gpu_raw = specs_data.get('GPU', "Standard Graphics Engine")
        gpu_name = gpu_raw if not isinstance(gpu_raw, list) else gpu_raw[0]

        telemetry_block = (
            f"\n"
            f"{CYAN}========== HARDWARE TELEMETRY PROFILE =========={RESET}\n"
            f"{YELLOW}OS       :{RESET} {system_os}\n"
            f"{YELLOW}CPU      :{RESET} {processor} ({cpu_threads} Threads)\n"
            f"{YELLOW}RAM      :{RESET} {total_ram}\n"
            f"{YELLOW}ROM      :{RESET} {total_rom}\n"
            f"{YELLOW}GRAPHICS :{RESET} {gpu_name}\n"
            f"{CYAN}================================================{RESET}"
        )
        return telemetry_block, f"Displaying full system diagnostics matrix now, sir. Operating configuration features {total_ram} of memory capacity alongside your {gpu_name} processing engine."
    except Exception:
        return (
            f"\n"
            f"{CYAN}========== HARDWARE TELEMETRY PROFILE =========={RESET}\n"
            f"{YELLOW}OS       :{RESET} {platform.system()} {platform.release()}\n"
            f"{YELLOW}CPU      :{RESET} {platform.processor()} ({os.cpu_count()} Threads)\n"
            f"{YELLOW}RAM      :{RESET} Tracking Restricted\n"
            f"{YELLOW}ROM      :{RESET} Active C: Index Mounted\n"
            f"{YELLOW}GRAPHICS :{RESET} Main Display Framework\n"
            f"{CYAN}================================================{RESET}"
        ), "Displaying generalized native system specifications now, sir."

def fetch_true_ai_intelligence(query, sentences_count=2):
    try:
        if sentences_count == 1:
            instruction = "You are Jarvis, Iron Man's male AI assistant. Give a single, ultra-short, punchy one-sentence answer to this: "
        else:
            instruction = "You are Jarvis, Iron Man's male AI assistant. Give a brief, two-sentence maximum answer to this: "
            
        full_prompt = instruction + query
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        conn = http.client.HTTPSConnection("text.pollinations.ai", timeout=7)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/plain',
            'Connection': 'close'
        }
        conn.request("GET", f"/{encoded_prompt}", headers=headers)
        response = conn.getresponse()
        
        if response.status == 200:
            result = response.read().decode('utf-8').strip()
            result = result.replace("```", "").replace("**", "").replace('"', '').strip()
            conn.close()
            if result:
                return result
        conn.close()
    except Exception:
        pass
    return None

def process_brain(user_input):
    if not user_input:
        return False
    
    raw_cmd = user_input.lower().strip()
    cmd = raw_cmd

    closest_phrases = difflib.get_close_matches(cmd, DICTIONARY_METRICS, n=1, cutoff=0.75)
    if closest_phrases:
        cmd = closest_phrases[0]

    if any(x in raw_cmd for x in ["specs", "specifications", "hardware status", "computer specs"]):
        print(f"{CYAN}[System Core: Parsing PowerShell Object Structures...]{RESET}")
        text_layout, voice_alert = read_hardware_specifications()
        print(text_layout)
        if windows_speaker:
            try: windows_speaker.Speak(voice_alert)
            except Exception: pass
        return False

    elif any(x in raw_cmd for x in ["where is", "find file", "search file"]):
        clean_target = raw_cmd.replace("where is the file", "").replace("where is file", "").replace("where is", "").replace("find file", "").replace("search file", "").strip()
        if not clean_target:
            jarvis_speak("Please specify the missing file array argument, sir.")
            return False
            
        jarvis_speak(f"Accessing disk directories. Inspecting path tracks for '{clean_target}' now.")
        found_data = locate_system_file(clean_target)
        
        if found_data:
            jarvis_speak("Target tracked successfully. Here are the entry parameters:")
            for file_path, file_size in found_data:
                jarvis_speak(f"File found at path location: {file_path}. Size parameters read exactly {file_size} megabytes.")
        else:
            jarvis_speak(f"I have crawled active directory trees but '{clean_target}' cannot be tracked inside standard storage matrices.")
        return False

    elif any(x == cmd for x in ["hello", "hi", "hey", "yo", "greetings", "jarvis", "wake up"]):
        jarvis_speak("At your service, sir. What are we constructing today?")
    elif "time" in cmd:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        jarvis_speak(f"The local system time reads exactly {current_time}.")
    elif any(x in cmd for x in ["screenshot", "capture screen", "take a picture"]):
        jarvis_speak("Acknowledged. Deploying screen capture tool.")
        time.sleep(0.4)  
        img = pyautogui.screenshot()
        filename = f"jarvis_snap_{int(time.time())}.png"
        img.save(filename)
        jarvis_speak(f"Screen capture archived successfully as {filename}.")
    elif any(x in cmd for x in ["exit", "quit", "power down", "terminate", "goodbye"]):
        jarvis_speak("Powering down core metrics. Goodbye, sir.")
        return True
    else:
        print(f"{CYAN}[System: Accessing True AI pipeline...]{RESET}")
        is_short_requested = "short" in user_input.lower() or "shortly" in user_input.lower()
        sentences_limit = 1 if is_short_requested else 2
        info_response = fetch_true_ai_intelligence(user_input, sentences_limit)
        if info_response: jarvis_speak(info_response)
        else: jarvis_speak("I am processing that entry but cannot locate an exact dataset description, sir.")
    return False

def run_voice_loop():
    """Continuous active mic loop until commanded back to text mode."""
    print(f"\n{GREEN}[🗣️ CONTINUOUS VOICE CHAT INITIALIZED]{RESET}")
    jarvis_speak("Systems online. Command me to 'switch to text' when finished, sir.")
    
    while True:
        print(f"{CYAN}[🎙️ Active Listening...]{RESET}")
        voice_text = get_high_sensitivity_voice()
        if not voice_text or voice_text == "__UNREADABLE__":
            continue  
        
        print(f"{PURPLE}{BOLD}[YOU (Voice)]{RESET} ❯ {voice_text}")
        log_conversation("USER (VOICE)", voice_text)
        
        if any(x in voice_text.lower() for x in ["go back to keyboard", "switch to text", "keyboard mode", "stop voice"]):
            jarvis_speak("Understood, sir. Defaulting back to manual keyboard controls and background standby voice tracking.")
            break
            
        should_exit = process_brain(voice_text)
        if should_exit:
            sys.exit()

def check_background_wake_word():
    """Silent passive background microphone verification for the activation sequence."""
    voice_input = get_high_sensitivity_voice(timeout_val=2, phrase_limit=3, silent=True)
    if "activate voice command" in voice_input.lower():
        return True
    return False

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ASCII_ART)
    jarvis_speak("Hello sir. Keyboard mode loaded. Microphone background wake-word tracking initialized.")
    
    while True:
        # Check if the mic heard the wake phrase in the background
        if check_background_wake_word():
            run_voice_loop()
            continue
            
        print(f"\n{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{DARK}[Mic Standby: Say 'activate voice command' out loud or type below]{RESET}")
        
        # Non-blocking check style emulation
        user_input = input(f"{PURPLE}{BOLD}[YOU]{RESET} ❯ ").strip()
        
        if not user_input:
            continue
            
        log_conversation("USER (TEXT)", user_input)
        
        if "activate voice command" in user_input.lower():
            run_voice_loop()
        else:
            should_exit = process_brain(user_input)
            if should_exit:
                sys.exit()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{RED}[!] Override: Emergency shutdown executed.{RESET}")
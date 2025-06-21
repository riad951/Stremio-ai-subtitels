import os, re, requests
from argostranslate import translate

SUBS_DIR = "subs"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_srt(imdb_id):
    url = f"https://yifysubtitles.ch/movie-imdb/{imdb_id}"
    res = requests.get(url, headers=HEADERS)
    matches = re.findall(r'href="(/subtitle/.+?english.+?)"', res.text)
    if not matches:
        print("❌ ترجمة غير موجودة"); return None
    sub_link = "https://yifysubtitles.ch" + matches[0]
    sub_page = requests.get(sub_link, headers=HEADERS)
    zip_match = re.search(r'href="(https://.*?\.zip)"', sub_page.text)
    if not zip_match:
        print("❌ ZIP غير موجود"); return None
    zip_url = zip_match.group(1)
    zip_data = requests.get(zip_url)
    zip_path = os.path.join(SUBS_DIR, f"{imdb_id}.zip")
    with open(zip_path, "wb") as f: f.write(zip_data.content)
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for name in zip_ref.namelist():
            if name.endswith(".srt"):
                zip_ref.extract(name, SUBS_DIR)
                en_path = os.path.join(SUBS_DIR, f"{imdb_id}.en.srt")
                os.rename(os.path.join(SUBS_DIR, name), en_path)
                return en_path
    return None

def translate_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f: content = f.read()
    blocks = re.split(r'\n\n+', content)
    translated_blocks = []
    langs = translate.get_installed_languages()
    source = next(l for l in langs if l.code == "en")
    target = next(l for l in langs if l.code == "ar")
    trans = source.get_translation(target)
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3: continue
        index, timestamp = lines[0], lines[1]
        text = " ".join(lines[2:])
        translated = trans.translate(text)
        translated_blocks.append(f"{index}\n{timestamp}\n{translated}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))

def run(imdb_id):
    os.makedirs(SUBS_DIR, exist_ok=True)
    input_file = os.path.join(SUBS_DIR, f"{imdb_id}.en.srt")
    output_file = os.path.join(SUBS_DIR, f"{imdb_id}.ar.srt")
    if not os.path.exists(input_file):
        if not fetch_srt(imdb_id): return
    translate_srt(input_file, output_file)
    print("✅ الترجمة جاهزة!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python auto_translate_sub.py tt1234567")
    else:
        run(sys.argv[1])
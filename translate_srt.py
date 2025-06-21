import re
from argostranslate import translate

def translate_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content)
    translated_blocks = []

    installed_languages = translate.get_installed_languages()
    from_lang = next(x for x in installed_languages if x.code == "en")
    to_lang = next(x for x in installed_languages if x.code == "ar")
    translation = from_lang.get_translation(to_lang)

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3: continue
        index = lines[0]
        timestamp = lines[1]
        text = " ".join(lines[2:])
        translated = translation.translate(text)
        translated_blocks.append(f"{index}\n{timestamp}\n{translated}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))
# Stremio AI Subtitles Add-on

ترجمة تلقائية لملفات SRT الإنجليزية إلى العربية باستخدام Argos Translate (أوفلاين ومجاني 100%).

## 🔧 التشغيل
1. ثبت:
   ```
   pip install argostranslate requests
   argos-translate-cli --install --from-lang en --to-lang ar
   ```
2. شغّل الترجمة:
   ```
   python auto_translate_sub.py tt4154796
   ```
3. شغّل الإضافة:
   ```
   npm install
   npm start
   ```
ثم أضف هذا في Stremio:  
`http://localhost:7000/manifest.json`
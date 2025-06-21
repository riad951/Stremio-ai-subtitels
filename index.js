const { addonBuilder } = require("stremio-addon-sdk");
const express = require("express");
const path = require("path");

const app = express();
app.use('/subs', express.static(path.join(__dirname, 'subs')));

const manifest = {
  id: "org.rmad.subtitle.ai",
  version: "1.0.0",
  name: "ترجمة AI مجانية",
  description: "ترجمة تلقائية لملفات SRT من الإنجليزية إلى العربية",
  types: ["movie"],
  resources: ["subtitles"],
  idPrefixes: ["tt"]
};

const builder = new addonBuilder(manifest);

builder.defineSubtitlesHandler(({ id }) => {
  return Promise.resolve({
    subtitles: [
      {
        id: "ar-ai",
        lang: "ar",
        url: `http://localhost:7000/subs/${id}.ar.srt`,
        title: "عربي (مترجم آليًا)",
        format: "srt"
      },
      {
        id: "en-original",
        lang: "en",
        url: `http://localhost:7000/subs/${id}.en.srt`,
        title: "English",
        format: "srt"
      }
    ]
  });
});

app.use('/', builder.getInterface());
app.listen(7000, () => console.log("✅ Addon running at http://localhost:7000/manifest.json"));
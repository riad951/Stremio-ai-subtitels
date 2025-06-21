const { addonBuilder } = require("stremio-addon-sdk");
const fs = require("fs");
const path = require("path");

const manifest = {
  id: "stremio-ai-subtitles",
  version: "1.0.0",
  name: "AI Subtitles",
  description: "ترجمة تلقائية للترجمات الإنجليزية إلى العربية باستخدام Argos Translate.",
  resources: ["subtitles"],
  types: ["movie"],
  idPrefixes: ["tt"],
  logo: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Subtitle_icon.png",
  catalogs: [],
};

const builder = new addonBuilder(manifest);

builder.defineSubtitlesHandler(async ({ id }) => {
  const englishPath = path.join(__dirname, "../public/subs", `${id}.en.srt`);
  const arabicPath = path.join(__dirname, "../public/subs", `${id}.ar.srt`);

  const subtitles = [];

  if (fs.existsSync(englishPath)) {
    subtitles.push({
      id: "en",
      lang: "en",
      url: `https://stremio-ai-subtitles.vercel.app/subs/${id}.en.srt`,
    });
  }

  if (fs.existsSync(arabicPath)) {
    subtitles.push({
      id: "ar",
      lang: "ar",
      url: `https://stremio-ai-subtitles.vercel.app/subs/${id}.ar.srt`,
    });
  }

  return { subtitles };
});

module.exports = builder.getInterface();

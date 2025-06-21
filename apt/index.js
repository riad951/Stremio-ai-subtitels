const { addonBuilder } = require("stremio-addon-sdk");

const manifest = {
  id: "org.rmad.subtitle.ai",
  version: "1.0.0",
  name: "ترجمة AI مجانية",
  description: "ترجمة تلقائية لملفات الترجمة الإنجليزية إلى العربية",
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
        url: `https://stremio-ai-subtitles.vercel.app/subs/${id}.ar.srt`,
        title: "عربي (مترجم آليًا)",
        format: "srt"
      },
      {
        id: "en-original",
        lang: "en",
        url: `https://stremio-ai-subtitles.vercel.app/subs/${id}.en.srt`,
        title: "English (Original)",
        format: "srt"
      }
    ]
  });
});

module.exports = builder.getInterface();
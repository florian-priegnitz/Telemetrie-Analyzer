# AI-Coverage-Report

**DB-Version:** v2.3.0 · **Stand:** 2026-05-03 (15 Tage alt) · 🟢 Aktuell (15 Tage)

_Auto-generiert via `scripts/db_coverage_report.py` am 2026-05-18. Manuelle Bearbeitung wird beim naechsten Skript-Lauf ueberschrieben._

## Kennzahlen

- **Endpoints:** 175
- **Provider:** 168
- **Kategorien:** 21
- **Risk-Verteilung:** critical: 19 · high: 69 · medium: 76 · low: 11

## Per Kategorie

| Kategorie | Endpoints | Anteil |
|-----------|----------:|-------:|
| LLM-Chatbots (`llm_chatbot`) | 20 | 11.4% |
| Code-Assistenten (`code_assistant`) | 16 | 9.1% |
| Bild-Generierung (`image_generation`) | 14 | 8.0% |
| Video-AI (`video_ai`) | 13 | 7.4% |
| Enterprise-Embedded (`enterprise_embedded`) | 11 | 6.3% |
| Meeting-AI (`meeting_ai`) | 10 | 5.7% |
| Autonome AI-Agenten (`ai_agent`) | 9 | 5.1% |
| Präsentations-AI (`presentation_ai`) | 9 | 5.1% |
| Schreib-Assistenten (`writing_assistant`) | 9 | 5.1% |
| ML-Plattformen (`ml_platform`) | 8 | 4.6% |
| Daten-Analyse (`data_analysis_ai`) | 7 | 4.0% |
| Customer-Support-AI (`customer_support_ai`) | 6 | 3.4% |
| Audio-Generierung (`audio_generation`) | 6 | 3.4% |
| Text-zu-Sprache (`text_to_speech`) | 6 | 3.4% |
| HR & Recruiting (`hr_recruiting_ai`) | 6 | 3.4% |
| Browser-Extensions (`browser_extension_ai`) | 6 | 3.4% |
| Content-Generierung (`content_generation`) | 5 | 2.9% |
| Produktivitäts-AI (`productivity_ai`) | 5 | 2.9% |
| Sprach-zu-Text (`speech_to_text`) | 4 | 2.3% |
| LLM-APIs (`llm_api`) | 4 | 2.3% |
| Übersetzung (`translation`) | 1 | 0.6% |

## Top-10-Provider nach Endpoints

| Provider | Endpoints |
|----------|----------:|
| Stability AI | 3 |
| OpenAI | 3 |
| Hugging Face | 2 |
| Microsoft | 2 |
| Vercel | 2 |
| Ada Support | 1 |
| Adept | 1 |
| Adobe | 1 |
| Reworkd | 1 |
| Aider | 1 |

## Vollständiger Katalog (gruppiert nach Kategorie)

### Autonome AI-Agenten (`ai_agent`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Adept AI | Adept | high | `adept.ai`, `app.adept.ai` |
| AgentGPT | Reworkd | high | `agentgpt.reworkd.ai` |
| AutoGPT | Significant Gravitas | high | `agpt.co`, `news.agpt.co` |
| Cognosys | Cognosys | high | `cognosys.ai` |
| Crew AI | Crew AI | high | `crewai.com` |
| Devin | Cognition | critical | `devin.ai`, `app.devin.ai` |
| Lindy | Lindy | high | `lindy.ai` |
| MultiOn | MultiOn | high | `multion.ai`, `app.multion.ai` |
| Superagent | Superagent | high | `superagent.sh` |

### Audio-Generierung (`audio_generation`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| AIVA | AIVA | low | `aiva.ai` |
| Boomy | Boomy | low | `boomy.com` |
| Mubert | Mubert | low | `mubert.com` |
| Stable Audio | Stability AI | low | `stableaudio.com` |
| Suno AI | Suno | low | `suno.com`, `app.suno.ai` |
| Udio | Udio | low | `udio.com` |

### Browser-Extensions (`browser_extension_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| HARPA AI | HARPA | high | `harpa.ai`, `api.harpa.ai` |
| MaxAI.me | MaxAI | medium | `maxai.me`, `api.maxai.me` |
| Merlin AI | Merlin | high | `getmerlin.in`, `api.getmerlin.in` |
| Monica AI | Monica | high | `monica.im`, `api.monica.im` |
| Sider AI | Sider | medium | `sider.ai`, `api.sider.ai` |
| TinaMind | TinaMind | medium | `tinamind.com`, `api.tinamind.com` |

### Code-Assistenten (`code_assistant`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Aider | Aider | critical | `aider.chat` |
| Amazon Q Developer | Amazon | high | `q.aws.amazon.com` |
| Bolt.new | StackBlitz | critical | `bolt.new` |
| Cline | Cline | critical | `cline.bot` |
| Codeium | Exafunction | critical | `codeium.com`, `server.codeium.com`, `inference.codeium.com` |
| Continue.dev | Continue | critical | `continue.dev` |
| Cursor | Anysphere | critical | `cursor.sh`, `api2.cursor.sh`, `repo42.cursor.sh` |
| GitHub Copilot | GitHub / Microsoft | critical | `copilot.github.com`, `api.githubcopilot.com`, `copilot-proxy.githubusercontent.com` _(+1 weitere)_ |
| JetBrains AI | JetBrains | high | `jetbrains.com/ai`, `api.jetbrains.ai` |
| Replit AI | Replit | critical | `replit.com`, `api.replit.com`, `repl.co` |
| Sourcegraph Cody | Sourcegraph | high | `sourcegraph.com`, `cody.sourcegraph.com` |
| Tabnine | Tabnine | high | `tabnine.com`, `api.tabnine.com` |
| v0.dev | Vercel | high | `v0.dev` |
| Warp AI | Warp | high | `warp.dev`, `app.warp.dev` |
| Windsurf | Codeium | critical | `codeium.com/windsurf`, `windsurf.ai` |
| Zed AI | Zed Industries | high | `zed.dev` |

### Content-Generierung (`content_generation`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Anyword | Anyword | medium | `anyword.com`, `app.anyword.com` |
| Copy.ai | Copy.ai | medium | `copy.ai`, `app.copy.ai` |
| Jasper AI | Jasper | medium | `app.jasper.ai`, `jasper.ai`, `api.jasper.ai` |
| Simplified | Simplified | medium | `simplified.com` |
| Writesonic | Writesonic | medium | `writesonic.com` |

### Customer-Support-AI (`customer_support_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Ada | Ada Support | medium | `ada.cx`, `ada.support` |
| Cresta | Cresta | high | `cresta.com`, `app.cresta.com` |
| Decagon | Decagon | high | `decagon.ai`, `app.decagon.ai` |
| Forethought | Forethought | high | `forethought.ai`, `app.forethought.ai` |
| Intercom Fin | Intercom | high | `fin.ai`, `intercom.io`, `api.intercom.io` |
| Zendesk AI | Zendesk | high | `zendesk.com`, `zdassets.com` |

### Daten-Analyse (`data_analysis_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Akkio | Akkio | high | `akkio.com`, `app.akkio.com` |
| DataRobot | DataRobot | high | `datarobot.com`, `app.datarobot.com` |
| Julius AI | Julius | high | `julius.ai` |
| Obviously AI | Obviously AI | high | `obviously.ai`, `app.obviously.ai` |
| Pragma | Pragma | high | `pragma.ai` |
| Quadratic AI | Quadratic | high | `quadratichq.com` |
| Rows AI | Rows | high | `rows.com` |

### Enterprise-Embedded (`enterprise_embedded`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Atlassian Rovo | Atlassian | medium | `rovo.atlassian.com` |
| Canva Magic Studio | Canva | medium | `canva.com/magic`, `www.canva.com` |
| Figma AI | Figma | medium | `figma.com/ai` |
| HubSpot AI | HubSpot | medium | `hubspot.com/ai` |
| Microsoft 365 Copilot | Microsoft | medium | `copilot.microsoft365.com`, `m365.cloud.microsoft` |
| Miro AI | Miro | medium | `miro.com/ai` |
| Notion AI | Notion | medium | `www.notion.so`, `api.notion.com` |
| Salesforce Einstein | Salesforce | medium | `einstein.salesforce.com` |
| ServiceNow Now Assist | ServiceNow | medium | `servicenow.com/ai` |
| Slack AI | Slack / Salesforce | medium | `slack.com/ai` |
| Zoom AI Companion | Zoom | medium | `ai.zoom.us`, `zoom.us/ai` |

### HR & Recruiting (`hr_recruiting_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Eightfold AI | Eightfold | high | `eightfold.ai`, `app.eightfold.ai` |
| HireVue | HireVue | high | `hirevue.com`, `app.hirevue.com` |
| Humanly | Humanly | medium | `humanly.io`, `app.humanly.io` |
| Paradox (Olivia) | Paradox | medium | `paradox.ai`, `app.paradox.ai` |
| Sana AI | Sana Labs | medium | `sana.ai`, `app.sana.ai` |
| SeekOut | SeekOut | medium | `seekout.com`, `app.seekout.com` |

### Bild-Generierung (`image_generation`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Adobe Firefly | Adobe | medium | `firefly.adobe.com`, `firefly-api.adobe.io` |
| Artbreeder | Artbreeder | low | `artbreeder.com` |
| Civitai | Civitai | medium | `civitai.com` |
| DreamStudio | Stability AI | medium | `dreamstudio.ai`, `beta.dreamstudio.ai` |
| Flux | Black Forest Labs | medium | `blackforestlabs.ai`, `api.bfl.ml` |
| Ideogram | Ideogram | medium | `ideogram.ai` |
| Krea | Krea | medium | `krea.ai` |
| Leonardo AI | Leonardo | medium | `leonardo.ai`, `app.leonardo.ai`, `api.leonardo.ai` |
| Lexica | Lexica | low | `lexica.art` |
| Midjourney | Midjourney | medium | `www.midjourney.com`, `midjourney.com`, `cdn.midjourney.com` |
| NightCafe | NightCafe | low | `nightcafe.studio`, `creator.nightcafe.studio` |
| Playground AI | Playground | medium | `playground.com`, `playgroundai.com` |
| Recraft | Recraft | medium | `recraft.ai` |
| Stability AI | Stability AI | medium | `stability.ai`, `api.stability.ai` |

### LLM-APIs (`llm_api`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Cohere | Cohere | high | `cohere.com`, `api.cohere.ai`, `dashboard.cohere.com` |
| OpenRouter | OpenRouter | high | `openrouter.ai` |
| Vercel AI SDK | Vercel | high | `sdk.vercel.ai` |
| Writer.com | Writer | medium | `writer.com`, `api.writer.com` |

### LLM-Chatbots (`llm_chatbot`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Anthropic Claude | Anthropic | high | `claude.ai`, `api.anthropic.com`, `cdn.anthropic.com` _(+1 weitere)_ |
| Baichuan AI | Baichuan | critical | `baichuan-ai.com`, `api.baichuan-ai.com` |
| Character.AI | Character Technologies | medium | `character.ai`, `beta.character.ai` |
| ChatGLM | Zhipu AI | critical | `chatglm.cn`, `open.bigmodel.cn` |
| DeepSeek | DeepSeek | critical | `chat.deepseek.com`, `api.deepseek.com`, `deepseek.com` |
| Doubao | ByteDance | critical | `doubao.com`, `www.doubao.com` |
| Google Gemini | Google | high | `gemini.google.com`, `generativelanguage.googleapis.com`, `aistudio.google.com` _(+1 weitere)_ |
| HuggingChat | Hugging Face | high | `huggingface.co/chat`, `hf.co/chat` |
| Kagi Assistant | Kagi | medium | `kagi.com/assistant` |
| Kimi | Moonshot AI | critical | `kimi.moonshot.cn`, `api.moonshot.cn` |
| Microsoft Copilot | Microsoft | high | `copilot.microsoft.com`, `sydney.bing.com`, `www.bing.com/chat` _(+1 weitere)_ |
| Mistral AI | Mistral | high | `chat.mistral.ai`, `api.mistral.ai`, `mistral.ai` |
| OpenAI ChatGPT | OpenAI | high | `chat.openai.com`, `api.openai.com`, `cdn.openai.com` _(+2 weitere)_ |
| Perplexity AI | Perplexity | high | `www.perplexity.ai`, `perplexity.ai`, `api.perplexity.ai` |
| Phind | Phind | high | `phind.com`, `www.phind.com` |
| Pi | Inflection AI | high | `pi.ai`, `heypi.com` |
| Poe | Quora | high | `poe.com` |
| Tongyi Qianwen | Alibaba | critical | `tongyi.aliyun.com`, `dashscope.aliyuncs.com` |
| xAI Grok | xAI | high | `grok.x.ai`, `api.x.ai`, `grok.com` |
| Yuanbao | Tencent | critical | `yuanbao.tencent.com` |

### Meeting-AI (`meeting_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Avoma | Avoma | high | `avoma.com`, `app.avoma.com` |
| Fathom | Fathom | high | `fathom.video`, `app.fathom.video` |
| Fireflies.ai | Fireflies | high | `fireflies.ai`, `app.fireflies.ai`, `api.fireflies.ai` |
| Granola | Granola | high | `granola.ai`, `app.granola.ai` |
| Krisp AI | Krisp | medium | `krisp.ai` |
| MeetGeek | MeetGeek | high | `meetgeek.ai` |
| Otter.ai | Otter | high | `otter.ai`, `api.otter.ai` |
| Read.ai | Read | high | `read.ai`, `app.read.ai` |
| Sembly | Sembly | high | `sembly.ai` |
| tl;dv | tl;dv | high | `tldv.io`, `api.tldv.io` |

### ML-Plattformen (`ml_platform`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| DeepInfra | DeepInfra | high | `deepinfra.com`, `api.deepinfra.com` |
| Fireworks AI | Fireworks | high | `fireworks.ai`, `api.fireworks.ai` |
| Groq Cloud | Groq | high | `groq.com`, `api.groq.com`, `console.groq.com` |
| Hugging Face | Hugging Face | high | `huggingface.co`, `api-inference.huggingface.co`, `cdn-lfs.huggingface.co` |
| Lightning AI | Lightning AI | high | `lightning.ai` |
| Modal | Modal Labs | high | `modal.com` |
| Replicate | Replicate | high | `replicate.com`, `api.replicate.com` |
| Together AI | Together | high | `together.ai`, `api.together.xyz` |

### Präsentations-AI (`presentation_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Beautiful.ai | Beautiful.ai | medium | `beautiful.ai`, `app.beautiful.ai` |
| Chronicle | Chronicle | medium | `chroniclehq.com` |
| Decktopus | Decktopus | medium | `decktopus.com` |
| Gamma | Gamma | medium | `gamma.app` |
| Pitch | Pitch | medium | `pitch.com`, `app.pitch.com` |
| Plus AI | Plus Docs | medium | `plusdocs.com` |
| Presentations.ai | Presentations | medium | `presentations.ai` |
| SlidesAI | SlidesAI | medium | `slidesai.io` |
| Tome | Tome | medium | `tome.app` |

### Produktivitäts-AI (`productivity_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Bardeen | Bardeen | medium | `bardeen.ai`, `app.bardeen.ai` |
| Browse AI | Browse AI | medium | `browse.ai` |
| Magical | Magical | medium | `getmagical.com` |
| Mem | Mem Labs | medium | `mem.ai`, `get.mem.ai` |
| Taskade | Taskade | medium | `taskade.com` |

### Sprach-zu-Text (`speech_to_text`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| AssemblyAI | AssemblyAI | high | `assemblyai.com`, `api.assemblyai.com` |
| Deepgram | Deepgram | high | `deepgram.com`, `api.deepgram.com` |
| Rev.ai | Rev | high | `rev.ai`, `api.rev.ai` |
| Whisper / OpenAI Audio | OpenAI | high | `api.openai.com/v1/audio` |

### Text-zu-Sprache (`text_to_speech`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Coqui | Coqui | low | `coqui.ai` |
| ElevenLabs | ElevenLabs | medium | `elevenlabs.io`, `api.elevenlabs.io` |
| Lovo | LOVO | medium | `lovo.ai` |
| Murf.ai | Murf | medium | `murf.ai` |
| Play.ht | PlayHT | medium | `play.ht`, `api.play.ht` |
| Speechify | Speechify | low | `speechify.com` |

### Übersetzung (`translation`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| DeepL | DeepL | medium | `www.deepl.com`, `api.deepl.com`, `api-free.deepl.com` _(+1 weitere)_ |

### Video-AI (`video_ai`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| D-ID | D-ID | medium | `d-id.com`, `studio.d-id.com`, `api.d-id.com` |
| Descript | Descript | medium | `descript.com`, `api.descript.com` |
| Haiper | Haiper | medium | `haiper.ai` |
| HeyGen | HeyGen | medium | `heygen.com`, `app.heygen.com`, `api.heygen.com` |
| InVideo AI | InVideo | medium | `invideo.io`, `ai.invideo.io` |
| Kling AI | Kuaishou | critical | `kling.kuaishou.com` |
| Luma Dream Machine | Luma | medium | `lumalabs.ai`, `dream-machine.lumalabs.ai` |
| MiniMax Hailuo | MiniMax | critical | `hailuoai.com`, `api.minimax.chat` |
| Pika Labs | Pika | medium | `pika.art`, `pikalabs.org` |
| Runway ML | Runway | medium | `runwayml.com`, `app.runwayml.com`, `api.runwayml.com` |
| Sora | OpenAI | high | `sora.com`, `sora.openai.com` |
| Synthesia | Synthesia | medium | `synthesia.io`, `api.synthesia.io` |
| Veo | Google DeepMind | high | `labs.google` |

### Schreib-Assistenten (`writing_assistant`)

| Service | Provider | Risk | Domains |
|---------|----------|------|---------|
| Grammarly AI | Grammarly | medium | `app.grammarly.com`, `grammarly.com`, `capi.grammarly.com` _(+1 weitere)_ |
| LanguageTool | LanguageTooler | medium | `languagetool.org`, `api.languagetool.org` |
| Lex.page | Lex | medium | `lex.page` |
| NovelAI | Anlatan | medium | `novelai.net` |
| ProWritingAid | ProWritingAid | medium | `prowritingaid.com` |
| Quillbot | QuillBot | medium | `quillbot.com` |
| Rytr | Rytr | medium | `rytr.me` |
| Sudowrite | Sudowrite | medium | `sudowrite.com` |
| Wordtune | AI21 | medium | `wordtune.com`, `app.wordtune.com` |

## Frische-Hinweis

Die DB wird monatlich aktualisiert via `.github/workflows/endpoint-db-update.yml` (cron `0 6 1 * *`). Ein zusätzlicher Review-Issue wird via `.github/workflows/db-review-issue.yml` erzeugt. Bei Frische-Signal 🟡/🔴 in der Settings-Page sollte ein DB-Review prioritisiert werden.


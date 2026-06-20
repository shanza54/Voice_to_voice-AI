# 🎙️ Voice-to-Voice AI Assistant
Live Demo:https://shanzaejaz-voice-to-voice-ai.hf.space

A high-performance, real-time voice-to-voice interactive application shell. The pipeline orchestrates local token processing via **Faster-Whisper** for rapid speech-to-text conversion, high-speed text completion utilizing **LLaMA 3.1 8B** via the **Groq API**, and dynamic audio translation streams built with Google Text-to-Speech (**gTTS**).

The wrapper is unified inside a fully customized, responsive dark-mode cybernetic **Gradio UI** built to operate seamlessly across both desktop and mobile layouts.

---

## ⚙️ Architectural Core & Features

* **Local Whisper Decoding:** Operates `faster-whisper` utilizing the `base` configuration mapped to `int8` quantization bounds—drastically dropping execution latency and system overhead.
* **Low-Latency LLM Pipelines:** Outsources conversational contextual logic straight into the Groq hardware-accelerated processing engine (`llama-3.1-8b-instant`).
* **Automated Audio Pipeline:** Seamless end-to-end routing framework where input voice signals translate to text, queue context strings, process textual outputs, and synthesize responsive speech audio arrays.
* **Bespoke CSS Glassmorphic Layout:** Overrides baseline UI styling rules to render responsive input groups, fluid font adjustments (`clamp()`), and structured viewport column organization.

---

## 🛠️ Tech Stack & Dependencies

* **Interface Architecture:** Gradio Framework
* **Transcription Engine:** `faster-whisper` (CTranslate2 backend optimizer)
* **Inference Platform:** Groq Cloud Client Architecture
* **Synthesis Core:** gTTS (Google Text-to-Speech API client)

---

## 📦 Production Installation & Local Setup

### 1. Clone the Application Repository
```bash
git clonehttps://github.com/YOUR_USERNAME/Voice_to_voice-AI.git
cd Voice_to_voice-AI
```

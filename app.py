import gradio as gr
from faster_whisper import WhisperModel
from groq import Groq
from gtts import gTTS
import os

print("Loading Whisper...")
whisper_model = WhisperModel("base", compute_type="int8")
client = Groq(api_key=os.environ["GROQ_API_KEY"])
print("Ready")

def voice_ai(audio_path):
    try:
        if audio_path is None:
            return None, "", ""
        segments, _ = whisper_model.transcribe(audio_path)
        user_text = "".join([seg.text for seg in segments])
        print("User:", user_text)

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = completion.choices[0].message.content
        print("AI:", reply)

        output_file = "response.mp3"
        tts = gTTS(reply)
        tts.save(output_file)
        return output_file, user_text, reply
    except Exception as e:
        print("ERROR:", e)
        return None, "error", str(e)

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    /* Prevent iOS font-size inflation */
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
}

body {
    background: #0a0a0f;
    font-family: 'Inter', sans-serif;
    color: #e8e8f0;
    min-height: 100vh;
    /* Prevent horizontal overflow at the root */
    overflow-x: hidden;
    width: 100%;
}

/* ── Gradio container ── */
.gradio-container {
    max-width: 780px !important;
    width: 100% !important;
    margin: 0 auto !important;
    /* Responsive padding: generous on desktop, tight on mobile */
    padding: 48px 20px !important;
    background: transparent !important;
    /* Prevent any child from bleeding out */
    overflow-x: hidden !important;
}

/* ── Header ── */
.app-header {
    text-align: center;
    margin-bottom: 40px;
    /* Ensure text wraps instead of overflowing */
    word-break: break-word;
}

.app-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 20px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    margin-bottom: 20px;
    font-size: 28px;
    /* Stop logo from stretching on tiny screens */
    flex-shrink: 0;
}

.app-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(22px, 6vw, 32px);   /* Fluid font: shrinks on small screens */
    font-weight: 600;
    color: #f0f0fa;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
    line-height: 1.2;
}

.app-subtitle {
    font-size: clamp(13px, 3.5vw, 15px);
    color: #7878a0;
    font-weight: 400;
    /* Let it wrap gracefully */
    white-space: normal;
    word-wrap: break-word;
}

/* ── Status badge ── */
.status-dot {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0f2818;
    border: 1px solid #1a4a2a;
    border-radius: 100px;
    padding: 4px 12px;
    font-size: clamp(11px, 2.8vw, 12px);
    color: #4ade80;
    margin-top: 16px;
    /* Prevent badge from breaking layout */
    max-width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4ade80;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Cards ── */
.card {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    /* Full width, no overflow */
    width: 100%;
    overflow: hidden;
}

.card-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #5050a0;
    margin-bottom: 12px;
}

/* ── Audio components ── */
.audio-component {
    background: #0d0d1a !important;
    border: 1.5px dashed #2a2a45 !important;
    border-radius: 12px !important;
    /* Never exceed card width */
    width: 100% !important;
    max-width: 100% !important;
    overflow: hidden !important;
}

/* Make inner Gradio audio waveform/controls fit */
.audio-component > * {
    max-width: 100% !important;
    overflow: hidden !important;
}

/* ── Generate button ── */
.generate-btn {
    width: 100% !important;
    height: 52px !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(14px, 3.5vw, 15px) !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    margin-top: 4px !important;
    box-shadow: 0 4px 24px rgba(99, 102, 241, 0.3) !important;
    /* Prevent button from overflowing */
    max-width: 100% !important;
    box-sizing: border-box !important;
}

.generate-btn:hover  { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.generate-btn:active { transform: translateY(0) !important; opacity: 1 !important; }

/* ── Text outputs ── */
.transcript-box textarea,
.reply-box textarea {
    background: #0d0d1a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #c8c8e8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: clamp(13px, 3.2vw, 14px) !important;
    line-height: 1.6 !important;
    padding: 14px 16px !important;
    resize: none !important;
    /* Always stay inside parent */
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

.transcript-box textarea::placeholder,
.reply-box textarea::placeholder {
    color: #3a3a6a !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: #1a1a2e;
    margin: 8px 0 24px;
    width: 100%;
}

/* ── RESPONSIVE: conversation columns ──
   Desktop → side-by-side  |  Mobile → stacked
   Gradio uses .gr-row / .row inside .gradio-container
*/
@media (max-width: 600px) {

    /* Tighter container padding on phone */
    .gradio-container {
        padding: 28px 12px !important;
    }

    /* Stack the two-column conversation row */
    .gradio-container .gr-row,
    .gradio-container .row,
    .gradio-container [class*="row"] {
        flex-direction: column !important;
        gap: 12px !important;
    }

    /* Each column takes full width */
    .gradio-container .gr-row > *,
    .gradio-container .row > *,
    .gradio-container [class*="row"] > * {
        width: 100% !important;
        min-width: 0 !important;
        flex: none !important;
    }

    /* Shrink logo a bit */
    .app-logo {
        width: 52px;
        height: 52px;
        font-size: 22px;
        border-radius: 16px;
    }

    /* Less bottom space on header */
    .app-header { margin-bottom: 28px; }

    /* Cards tighter on mobile */
    .card { padding: 16px; }

    /* Button slightly shorter on phone */
    .generate-btn { height: 48px !important; }
}

/* ── Gradio footer & default title ── */
footer { display: none !important; }
.gr-prose h1, .gr-prose p { display: none !important; }

/* Gradio label style */
label.svelte-1b6s6g {
    color: #7070b0 !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
"""

with gr.Blocks(css=css, title="Voice AI") as demo:

    gr.HTML("""
    <div class="app-header">
        <div class="app-logo">🎙</div>
        <h1 class="app-title">Voice AI Assistant</h1>
        <p class="app-subtitle">Speak naturally — powered by Whisper, LLaMA 3 &amp; gTTS</p>
        <div class="status-dot"><span class="dot"></span> Online · llama-3.1-8b-instant</div>
    </div>
    """)

    with gr.Group(elem_classes="card"):
        gr.HTML('<div class="card-label">🎤 &nbsp;Record your message</div>')
        mic = gr.Audio(
            type="filepath",
            label="",
            elem_classes="audio-component"
        )
        btn = gr.Button("Generate response →", elem_classes="generate-btn")

    gr.HTML('<div class="divider"></div>')

    gr.HTML('<div class="card-label" style="color:#5050a0; margin-bottom:12px;">💬 &nbsp;Conversation</div>')

    with gr.Row():
        with gr.Column():
            user_box = gr.Textbox(
                label="You said",
                placeholder="Your transcribed speech will appear here...",
                lines=4,
                elem_classes="transcript-box"
            )
        with gr.Column():
            ai_box = gr.Textbox(
                label="AI reply",
                placeholder="The AI's response will appear here...",
                lines=4,
                elem_classes="reply-box"
            )

    with gr.Group(elem_classes="card", visible=True):
        gr.HTML('<div class="card-label">🔊 &nbsp;Audio response</div>')
        out_audio = gr.Audio(label="", elem_classes="audio-component")

    gr.HTML('<div class="app-footer" style="text-align:center;margin-top:40px;font-size:12px;color:#3a3a5a;">Whisper STT · Groq LLM · gTTS · Built with Gradio</div>')

    btn.click(
        voice_ai,
        inputs=mic,
        outputs=[out_audio, user_box, ai_box]
    )

demo.launch()
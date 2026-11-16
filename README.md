<a name="readme-top"></a>

# NexusVoice — Sub-500ms Real-Time Conversational Voice AI

<p align="center">
    <a href="https://github.com/wtfear/NexusVoice" target="_blank">
        <img src="https://img.shields.io/badge/repo-wtfear%2FNexusVoice-blue.svg?logo=github" alt="GitHub Repository" />
    </a>
    <a href="https://github.com/wtfear/NexusVoice/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=green" alt="License" />
    </a>
    <a href="https://github.com/wtfear/NexusVoice/stargazers" target="_blank">
        <img src="https://img.shields.io/badge/latency-%3C500ms-brightgreen" alt="Sub-500ms Latency" />
    </a>
</p>

> **NexusVoice** is an enterprise-grade autonomous voice agent designed for ultra-low latency (<500ms) conversational AI over WebRTC and telephone lines. It combines **Silero VAD**, **Deepgram Nova-2**, **Groq / Cerebras (Llama-3.3-70b)**, and **Cartesia / Deepgram Aura** for human-like conversational fluidity with natural speech interruptions.

Part of the **Nexus Enterprise Suite** (alongside [NexusIQ](https://github.com/wtfear/NexusIQ)).

---

## ⚡ Key Highlights

* **Sub-500ms Turn Latency:** End-to-end response time under 500 milliseconds (VAD -> STT -> LLM -> TTS -> Audio playback).
* **Natural Interruptions:** With `allow_interruptions=True`, the AI instantly ceases talking when a user speaks over it.
* **100% Free-Tier Compatible:** Runs completely on free cloud allowances (LiveKit Cloud 50GB + Groq Free Tier + Deepgram \$200 credit).
* **Lightweight Architecture:** Consumes **less than 250 MB RAM** on standard host environments.
* **Dual LLM Routing:** Native support for **Groq Cloud** (Llama-3.3-70b) and **Cerebras AI** with automated fallback.

---

## 🏗️ Architecture Pipeline

```
                               ┌────────────────────────────────┐
                               │     Client Audio (WebRTC)      │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │       LiveKit Cloud Room       │
                               └───────────────┬────────────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
 ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
 │     Silero VAD (Local)    │   │    Deepgram Nova-2 (STT)  │   │  Groq / Cerebras (LLM)    │
 │ (Voice Activity Detection)│   │  (Real-Time Streaming)    │   │  (Llama-3.3 Sub-150ms)    │
 └───────────────────────────┘   └───────────────────────────┘   └─────────────┬─────────────┘
                                                                               │
                                                                               ▼
                                                                 ┌───────────────────────────┐
                                                                 │  Cartesia / Deepgram (TTS)│
                                                                 │  (Streaming Voice Audio)  │
                                                                 └───────────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
* Python 3.10+
* Free API accounts:
  * [LiveKit Cloud](https://cloud.livekit.io) (Free WebRTC server)
  * [Deepgram](https://deepgram.com) (\$200 free credit for STT & TTS)
  * [Groq Cloud](https://console.groq.com) (Free LLM inference at 300+ tok/s)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/wtfear/NexusVoice.git
cd NexusVoice

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Copy the example environment file and add your keys:
```bash
cp .env.example .env
```

Fill in `.env`:
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret

DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
```

### 4. Launch the Agent
```bash
python main.py dev
```

Test your live agent instantly using the **[LiveKit Agents Playground](https://agents-playground.livekit.io)** or connect it to your custom web / telephony client.

---

## 🌐 Web & Telephony Deployment

* **Web UI (Vercel):** Connect any Next.js voice client with `@livekit/components-react` hosted on Vercel for free.
* **SIP / Telephone Lines:** Hook NexusVoice up to **Twilio** or **Telnyx** via LiveKit SIP for automated inbound/outbound phone calls.

---

## 📄 License

Licensed under the **MIT License**.

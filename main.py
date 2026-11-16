import os
import asyncio
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli, JobProcess, Agent, AgentSession
from livekit.plugins import deepgram, silero, openai

load_dotenv()

# Select LLM Provider (Groq Free Tier by default or Cerebras)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

if LLM_PROVIDER == "cerebras":
    LLM_BASE_URL = "https://api.cerebras.ai/v1"
    LLM_API_KEY = os.getenv("CEREBRAS_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1-8b")
else:
    # Default to Groq (100% Free Tier, sub-200ms latency)
    LLM_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    LLM_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = os.getenv(
    "NEXUS_VOICE_SYSTEM_PROMPT",
    (
        "You are NexusVoice, an enterprise-grade autonomous voice AI assistant. "
        "You are participating in a live audio phone conversation. "
        "Keep your answers concise, natural, warm, and engaging. "
        "Never use bullet points, markdown formatting, or symbols—speak in clear, natural human sentences."
    )
)

GREETING_MESSAGE = os.getenv("NEXUS_VOICE_GREETING", "Hello! I am NexusVoice. How can I assist you today?")


def prewarm(proc: JobProcess):
    """Pre-warm Silero VAD (Voice Activity Detection) in memory for zero turn latency."""
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Entry point for incoming WebRTC live voice rooms."""
    
    # Initialize Text-to-Speech (Cartesia if key present, fallback to Deepgram Aura TTS)
    cartesia_key = os.getenv("CARTESIA_API_KEY")
    if cartesia_key:
        from livekit.plugins import cartesia
        tts_engine = cartesia.TTS(voice=os.getenv("CARTESIA_VOICE_ID", "248be419-c632-4f23-adf1-5324ed7dbf1d"))
    else:
        tts_engine = deepgram.TTS(model="aura-asteria-en")

    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model="nova-2-general"),
        llm=openai.LLM(
            base_url=LLM_BASE_URL,
            api_key=LLM_API_KEY,
            model=LLM_MODEL,
        ),
        tts=tts_engine,
        allow_interruptions=True,
    )

    agent = Agent(instructions=SYSTEM_PROMPT)

    await ctx.connect()
    await session.start(agent, room=ctx.room)
    await asyncio.sleep(0.5)
    await session.say(GREETING_MESSAGE, allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

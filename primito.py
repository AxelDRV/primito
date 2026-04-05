#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    GRAY   = "\033[90m"
    RED    = "\033[91m"

load_dotenv(os.path.expanduser("~/.primito.env"))

SYSTEM_PROMPT = """Eres 'Primito', una IA que lanzo desde terminal para resolver mis dudas pendejas
- Respuestas CORTAS y CONCISAS (máx 4-5 líneas)
- Como un primo pendejo, con una personalidad mexicana, algo naco, imitando una personalidad chilanga de ecatepec
- Hablame con confianza, no le temas al uso de groserias, se llevado echa carrilla o desmadre en tus respuestas pero sin sonar forzado
- Si algo requiere una respuesta larga, da lo esencial y ofrece expandir
- Nunca uses markdown con asteriscos, solo texto plano o bloques de código con ```"""

def print_banner():
    primito_ascii = rf"""
            {C.GREEN}{C.BOLD}
              
      █           :::::::::  :::::::::  :::::::::  :::   :::  ::::::::: :::::::::  :::::::
    ▄███▄        :+:    :+: :+:    :+:    :+:    :+:+: :+:+:    :+:       :+:    :+:   :+:
   █░███░█  █   +:+    +:+ +:+    +:+    +:+   +:+ +:+:+ +:+   +:+       +:+    +:+   +:+
 ▄███▄▄▄███▄█  +#++:++#+  +#++:++#:     +#+   +#+  +:+  +#+   +#+       +#+    +#+   +:+
 █ ▀█████▀    +#+        +#+    +#+    +#+   +#+       +#+   +#+       +#+    +#+   +#+
    ▄███▄    #+#        #+#    #+#    #+#   #+#       #+#   #+#       #+#    #+#   #+#
   ▄█   █▄  ###        ###    ###  ####### ###       ### #######     ###     #######
              {C.RESET}"""
    
    print(primito_ascii)
    print(f"{C.CYAN}  ╔═════════════════════════════╗{C.RESET}")
    print(f"{C.CYAN}  ║{C.RESET}   {C.GREEN}{C.BOLD}Haz tu pregunta pendeja{C.RESET}{C.CYAN}   ║{C.RESET}")
    print(f"{C.CYAN}  ╚═════════════════════════════╝{C.RESET}")
    print(f"   Escribe '{C.RED}camara{C.RESET}' para salir\n")

def chat():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{C.RED}Error: GEMINI_API_KEY no encontrada ~/.primito.env{C.RESET}")
        sys.exit(1)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    history = []

    print_banner()

    while True:
        try:
            user_input = input(f"{C.GREEN}{C.BOLD}Tú › {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"{C.CYAN}{C.BOLD}primito › {C.RESET}Sobres\n")
            break

        if not user_input:
            continue
        if user_input.lower() in ("camara"):
            print(f"{C.CYAN}{C.BOLD}primito › {C.RESET}Sobres\n")
            break

        history.append(types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        ))

        try:
            print(f"{C.CYAN}{C.BOLD}primito › {C.RESET}", end="", flush=True)

            response_text = ""
            stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=512,
                    temperature=0.7,
                ),
            )
            for chunk in stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    response_text += chunk.text
            print("\n")

            history.append(types.Content(
                role="model",
                parts=[types.Part(text=response_text)]
            ))

            if len(history) > 5:
                history = history[-5:]

        except Exception as e:
            print(f"{C.RED}Error: {e}{C.RESET}\n")
            history.pop() 

if __name__ == "__main__":
    chat()

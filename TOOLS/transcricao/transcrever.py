#!/usr/bin/env python
"""Transcricao local de audios (WhatsApp, mp3, m4a, opus, wav...) com faster-whisper.

Uso rapido:
    python transcrever.py <arquivo_ou_pasta> [opcoes]

Exemplos:
    python transcrever.py "C:\\Users\\renat\\Documents\\OPENCODE\\CARREIRA\\candidaturas\\audio.ogg"
    python transcrever.py "..\\candidaturas" --model small --md "..\\candidaturas\\VAGA_DOMO-MERCANTIL.md"
    python transcrever.py "..\\candidaturas" --termos "Airflow, PySpark, Kubernetes, Bacen" --srt

Saida: um .txt por audio na pasta --out (padrao: mesma pasta do audio).
Nao usa nuvem: everything roda local na CPU, sem API key.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

AUDIO_EXT = {
    ".opus", ".ogg", ".oga", ".m4a", ".mp3", ".wav", ".webm",
    ".aac", ".flac", ".mp4", ".m4v", ".mov", ".mkv", ".3gp", ".amr",
}
MARKER = "<!-- TRANSCRICOES -->"


def coletar_audio(alvo: Path) -> list[Path]:
    if alvo.is_file():
        return [alvo]
    if not alvo.is_dir():
        raise SystemExit(f"Alvo nao encontrado: {alvo}")
    return sorted(
        p for p in alvo.rglob("*")
        if p.is_file() and p.suffix.lower() in AUDIO_EXT
    )


def duracao_av(path: Path) -> str:
    try:
        import av

        with av.open(str(path)) as c:
            s = c.streams.audio[0]
            if s.duration and s.time_base:
                return f"{float(s.duration * s.time_base):.1f}s"
            return "~"
    except Exception:
        return "?"


def formatar_ts(seg: float) -> str:
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"


def bloco_markdown(audio: Path, corpo: str, meta: dict) -> str:
    return "\n".join([
        MARKER, "",
        f"### ÁUDIO — {audio.stem}", "",
        f"- **Arquivo:** `{audio.name}`",
        f"- **Duração:** {meta['duracao']} | **Modelo:** {meta['modelo']} (int8/CPU) | "
        f"**Idioma forçado:** {meta['idioma']} | **Transcrito em:** {meta['quando']}", "",
        "> Transcrição automática (faster-whisper). Trechos de baixa confiança podem conter erros.",
        "",
        corpo, "", "---", "",
    ])


def inserir_md(md_path: Path, bloco: str) -> None:
    if md_path.is_file() and MARKER in md_path.read_text(encoding="utf-8"):
        texto = md_path.read_text(encoding="utf-8").replace(MARKER, bloco, 1)
        md_path.write_text(texto, encoding="utf-8")
    else:
        with md_path.open("a", encoding="utf-8") as f:
            f.write("\n" + bloco)
    print(f"  -> contexto atualizado em {md_path}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="Transcreve audios locais com faster-whisper (CPU, offline).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("alvo", help="arquivo de audio ou pasta com audios")
    ap.add_argument("--model", default="small",
                    help="tiny | base | small | medium | large-v3 (padrao: small). "
                         "medium=melhor em portugues, mais lento na CPU")
    ap.add_argument("--lang", default="pt", help="idioma forcado (padrao: pt). Use 'auto' para detectar")
    ap.add_argument("--out", default=None, help="pasta de saida dos .txt (padrao: mesma do audio)")
    ap.add_argument("--md", default=None, help="arquivo .md para inserir a transcricao no contexto")
    ap.add_argument("--termos", default="",
                    help="termos de dominio a guiar oRecognition de nomes proprios "
                         '(ex.: "Airflow, PySpark, Kubernetes, Bacen")')
    ap.add_argument("--srt", action="store_true", help="gera tambem .srt com timestamps")
    ap.add_argument("--timestamps", action="store_true", help="inclui [mm:ss] no texto")
    ap.add_argument("--sem-vad", action="store_true", help="desliga o filtro de silencio (VAD)")
    ap.add_argument("--forcar", action="store_true", help="retranscreve mesmo que o .txt exista")
    ap.add_argument("--threads", type=int, default=0, help="threads de CPU (padrao: todos os cores)")
    args = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit(
            "faster-whisper nao encontrado. Rode:\n"
            "  python -m pip install faster-whisper"
        )

    alvo = Path(args.alvo).expanduser().resolve()
    audios = coletar_audio(alvo)
    if not audios:
        print(f"Nenhum arquivo de audio encontrado em {alvo}")
        print(f"Extensoes aceitas: {', '.join(sorted(AUDIO_EXT))}")
        return 1

    threads = args.threads or (os.cpu_count() or 4)
    print(f"Carregando modelo '{args.model}' (CPU, int8, {threads} threads)...")
    t0 = time.time()
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=threads,
    )
    print(f"Modelo pronto em {time.time() - t0:.1f}s\n")

    idioma = None if args.lang == "auto" else args.lang
    prompt = None
    if args.termos:
        prompt = f"Vocabulario do dominio: {args.termos}."

    erros = 0
    for i, audio in enumerate(audios, 1):
        out_dir = Path(args.out).expanduser().resolve() if args.out else audio.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        txt = out_dir / f"{audio.stem}.txt"
        srt = out_dir / f"{audio.stem}.srt"

        print(f"[{i}/{len(audios)}] {audio.name}  ({duracao_av(audio)})")
        if txt.exists() and not args.forcar:
            print(f"  .txt ja existe, pulando (use --forcar para refazer)")
        else:
            inicio = time.time()
            segmentos, info = model.transcribe(
                str(audio),
                language=idioma,
                initial_prompt=prompt,
                vad_filter=not args.sem_vad,
                beam_size=5,
                condition_on_previous_text=False,
            )
            partes, marcas, confs = [], [], []
            for seg in segmentos:
                if not seg.text.strip():
                    continue
                prefixo = f"[{formatar_ts(seg.start)[3:]}] " if args.timestamps else ""
                partes.append(prefixo + seg.text.strip())
                marcas.append((formatar_ts(seg.start), formatar_ts(seg.end), seg.text.strip()))
                if seg.avg_logprob is not None:
                    confs.append(seg.avg_logprob)

            if not partes:
                print("  !! nenhum segmento detectado (audio vazio ou silencio?)")
                erros += 1
                continue

            corpo = "\n\n".join(partes) + "\n"
            cabecalho = (
                f"# Transcricao — {audio.stem}\n\n"
                f"- Arquivo: {audio.name}\n"
                f"- Duracao: {info.duration:.1f}s\n"
                f"- Modelo: {args.model} (int8/CPU)\n"
                f"- Idioma detectado: {info.language} (prob {info.language_probability:.2f})\n"
                f"- Segmentos: {len(partes)}\n"
                f"- Transcrito em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                "---\n\n"
            )
            txt.write_text(cabecalho + corpo, encoding="utf-8")
            if args.srt:
                srt.write_text(
                    "\n\n".join(
                        f"{n}\n{a} --> {b}\n{c}" for n, (a, b, c) in enumerate(marcas, 1)
                    ),
                    encoding="utf-8",
                )
            dt = time.time() - inicio
            rtf = dt / max(info.duration, 0.01)
            print(f"  ok: {len(partes)} segmentos em {dt:.0f}s (rtf {rtf:.2f}x) -> {txt.name}")

        if args.md:
            linhas = txt.read_text(encoding="utf-8").splitlines()
            cortar = ("#", "- Arquivo:", "- Duracao:", "- Modelo:",
                      "- Idioma detectado:", "- Segmentos:", "- Transcrito em:", "---")
            corpo = "\n".join(l for l in linhas if not l.startswith(cortar)).strip()
            meta = {
                "duracao": duracao_av(audio),
                "modelo": args.model,
                "idioma": idioma or "auto",
                "quando": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
            inserir_md(Path(args.md).expanduser().resolve(),
                       bloco_markdown(audio, corpo, meta))
        print()

    print("Concluido." if not erros else f"Concluido com {erros} aviso(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Converte imagens para o formato 9:16 (ex.: 1080x1920)."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps, ImageFilter


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().split("x")
        w, h = int(width), int(height)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Use o formato LARGURAxALTURA, por exemplo: 1080x1920"
        ) from exc

    if w <= 0 or h <= 0:
        raise argparse.ArgumentTypeError("Largura e altura precisam ser maiores que zero")

    if w * 16 != h * 9:
        raise argparse.ArgumentTypeError("O tamanho informado precisa respeitar a proporção 9:16")

    return w, h


def list_images(input_path: Path) -> Iterable[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Arquivo não suportado: {input_path}")
        return [input_path]

    if input_path.is_dir():
        files = [
            p
            for p in sorted(input_path.iterdir())
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        if not files:
            raise ValueError(f"Nenhuma imagem encontrada em: {input_path}")
        return files

    raise ValueError(f"Caminho inválido: {input_path}")


def build_background(image: Image.Image, size: tuple[int, int], mode: str) -> Image.Image:
    if mode == "solid":
        return Image.new("RGB", size, (0, 0, 0))

    bg = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    return bg.filter(ImageFilter.GaussianBlur(radius=28))


def convert_to_916(
    image_path: Path,
    output_path: Path,
    size: tuple[int, int],
    fit_mode: str,
    background_mode: str,
) -> None:
    with Image.open(image_path) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")

        if fit_mode == "cover":
            final = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
        else:
            final = build_background(image, size, background_mode)
            foreground = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
            x = (size[0] - foreground.width) // 2
            y = (size[1] - foreground.height) // 2
            final.paste(foreground, (x, y))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        final.save(output_path, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transforma uma imagem ou pasta de imagens para 9:16"
    )
    parser.add_argument("input", type=Path, help="Arquivo de imagem ou pasta com imagens")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("saida_9x16"),
        help="Pasta de saída (default: ./saida_9x16)",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=parse_size,
        default=(1080, 1920),
        help="Resolução alvo 9:16. Exemplo: 1080x1920",
    )
    parser.add_argument(
        "--fit",
        choices=["contain", "cover"],
        default="contain",
        help=(
            "contain: mantém imagem inteira com fundo. "
            "cover: preenche 100%% cortando excesso"
        ),
    )
    parser.add_argument(
        "--background",
        choices=["blur", "solid"],
        default="blur",
        help="Fundo ao usar --fit contain",
    )

    args = parser.parse_args()

    images = list_images(args.input)
    for image in images:
        destination = args.output / f"{image.stem}_9x16.jpg"
        convert_to_916(image, destination, args.size, args.fit, args.background)
        print(f"OK: {image} -> {destination}")

    print(f"Concluído: {len(list(images))} arquivo(s) convertido(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

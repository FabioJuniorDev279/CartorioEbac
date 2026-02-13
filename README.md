# CartorioEbac

Projeto do curso de TI da Ebac.

## Conversor de imagens para 9:16

Foi adicionado um utilitário em Python para transformar imagens de tamanhos diferentes em uma saída 9:16 (vertical), ideal para stories/reels.

### Requisitos

```bash
python3 -m pip install -r requirements.txt
```

### Como usar

Converter uma imagem:

```bash
python3 image_to_916.py caminho/da/imagem.jpg
```

Converter todas as imagens de uma pasta:

```bash
python3 image_to_916.py caminho/da/pasta -o saida_9x16
```

### Opções úteis

- `--size 1080x1920`: define a resolução 9:16 de saída.
- `--fit contain` (padrão): mantém a imagem inteira e adiciona fundo.
- `--fit cover`: preenche toda a tela 9:16 cortando o excesso.
- `--background blur` (padrão): fundo desfocado no modo `contain`.
- `--background solid`: fundo preto no modo `contain`.

### Exemplo completo

```bash
python3 image_to_916.py ./fotos --size 1080x1920 --fit contain --background blur -o ./fotos_916
```

# vCard inside a QRcode

This script generates a vCard file and then encodes it into a qrcode so the user don't need to be online to get your
contact info.

To install dependencies:

```shell
pip install -r requirements.txt
```

Then:

```shell
python vcard_qrcode.py \
  --email josecarlos@dasilva.com \
  --organization 'Minha empresa Ltda' \
  --title 'Diretor de Tecnologia' \
  --nick 'Zé Carlos' \
  --lang 'pt-BR' \
  --phone '+55 11 999 888 777' \
  --phone_type 'Celular' \
  --url 'https://www.dasilva.com/' \
  'José Carlos' \
  'da Silva' \
  qrcode-zecarlos.png
```

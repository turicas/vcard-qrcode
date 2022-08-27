# vCard QRcode

- Gera arquivo do tipo vCard e anexa no QRcode
  - Ao ler o QRcode, usuário não precisa acessar um link (já tem as informações offline)

```shell
python vcard_qrcode.py \
  --email josecarlos@dasilva.com \
  --organization 'Minha empresa Ltda' \
  --title 'Diretor de Tecnologia' \
  --nick 'Zé Carlos' \
  -- lang 'pt-BR' \
  --phone '+55 11 999 888 777' \
  --phone_type 'Celular' \
  --url 'https://www.dasilva.com/' \
  'José Carlos' \
  'da Silva' \
  qrcode-zecarlos.png
```
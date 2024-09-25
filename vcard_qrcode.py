# pip install vobject qrcode[pil]

import argparse
import base64
import datetime

import vobject
import qrcode


def create_vcard(first_name, last_name, email=None, organizations=None,
        category=None, nickname=None, lang=None, pgp_key=None, phone=None,
        phone_type="cell", url=None, title=None, role=None, uid=None,
        organization_logo=None, photo=None, sound=None, photo_type="jpeg",
        organization_logo_type="jpeg", sound_type="ogg"):
    card = vobject.vCard()
    card.add("kind")
    card.kind.value = "individual"

    card.add("rev")
    card.rev.value = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")

    if lang is not None:
        card.add("lang")
        card.lang.value = lang

    card.add("n")  # structured representation of the name
    card.n.value = vobject.vcard.Name(given=first_name, family=last_name)
    card.add("fn")  # formatted name
    card.fn.value = f"{first_name} {last_name}"

    if photo is not None:
        card.add("photo")
        card.photo.type_param = photo_type
        card.photo.encoding_param = "B"
        card.photo.value = photo

    if sound is not None:
        card.add("sound")
        card.sound.type_param = sound_type
        card.sound.encoding_param = "B"
        card.sound.value = sound

    if nickname is not None:
        card.add("nickname")
        card.nickname.value = nickname

    if email is not None:
        card.add("email")
        card.email.value = email
        card.email.type_param = "Trabalho"

    if phone is not None:
        card.add("tel")
        card.tel.value = phone
        card.tel.type_param = phone_type

    if url is not None:
        card.add("url")
        card.url.value = url

    if pgp_key is not None:
        # TODO: should base64-encode key?
        card.add("key")
        card.key.value = f"data:application/pgp-keys;base64,{pgp_key}"

    if category is not None:
        card.add("category")
        card.category.value = category

    if organizations is not None:
        card.add("org")  # organizations
        card.org.value = organizations

    if organization_logo is not None:
        card.add("logo")
        card.logo.type_param = organization_logo_type
        card.logo.encoding_param = "B"
        card.logo.value = organization_logo

    if role is not None:
        card.add("role")
        card.role.value = role

    if title is not None:
        card.add("title")
        card.title.value = title

    if uid is not None:
        card.add("uid")
        card.uid.value = uid

    # TODO: address

    return card.serialize()


def read_file(filename):
    with open(filename, mode="rb") as fobj:
        return fobj.read()


if __name__ == "__main__":
    # TODO: pgp_key

    import argparse

    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import (
        CircleModuleDrawer,
        GappedSquareModuleDrawer,
        HorizontalBarsDrawer,
        RoundedModuleDrawer,
        SquareModuleDrawer,
        VerticalBarsDrawer,
    )
    from qrcode.image.styles.colormasks import RadialGradiantColorMask, VerticalGradiantColorMask

    DRAWERS = {
        "circle": CircleModuleDrawer,
        "gapped": GappedSquareModuleDrawer,
        "horizontal-bars": HorizontalBarsDrawer,
        "rounded": RoundedModuleDrawer,
        "square": SquareModuleDrawer,
        "vertical-bars": VerticalBarsDrawer,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--email")
    parser.add_argument("--drawer", default="square", choices=list(DRAWERS.keys()))
    parser.add_argument("--eye-drawer", default="square", choices=list(DRAWERS.keys()))
    parser.add_argument("--embedded-photo")
    parser.add_argument("--organization")
    parser.add_argument("--nickname")
    parser.add_argument("--lang", default="pt-BR")
    parser.add_argument("--phone")
    parser.add_argument("--phone_type", default="Celular")
    parser.add_argument("--url")
    parser.add_argument("--title")
    parser.add_argument("first_name")
    parser.add_argument("last_name")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    card_data = create_vcard(
        first_name=args.first_name,
        last_name=args.last_name,
        email=args.email,
        nickname=args.nickname,
        organizations=[args.organization] if args.organization else None,
        lang=args.lang,
        phone=args.phone,
        phone_type=args.phone_type,
        url=args.url,
        title=args.title,
    )
    if args.debug:
        print(card_data)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # TODO: configure qrcode:
    # version=1,
    # error_correction=qrcode.constants.ERROR_CORRECT_L,
    # box_size=10
    # border=4
    qr.add_data(card_data)
    qr.make(fit=True)
    # TODO: embedded ou embeded?
    # TODO: se passar module_drawer sem image_factory=StyledPilImage não dá erro
    # TODO: RadialGradiantColorMask or gradiEnt?
    img = qr.make_image(
        image_factory=StyledPilImage,
        back_color="white",  # TODO: change
        embeded_image_path=args.embedded_photo,
        fill_color="black",  # TODO: change
        module_drawer=DRAWERS[args.drawer](),
        eye_drawer=DRAWERS[args.eye_drawer](),
        #color_mask=VerticalGradiantColorMask(),
        #    back_color=(255, 255, 255),
        #    center_color=(22, 27, 34),
        #    edge_color=(38, 166, 65),
        #),  # TODO: change
    )
    img.save(args.output_filename)

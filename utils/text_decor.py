def head_formatting(text, *args, font="Sora", font_size="3rem", letter_spacing="0px", weight="700",padding= "0.5"):
    # Default gradient colors
    default_colors = ["#5900FF", "#0C71FF", "#00f7ff"]
    colors = list(args) if args else default_colors
    gradient = ", ".join(colors)

    # Font library — pick by style keyword or direct Google Font name
    font_map = {
        "sora":        "Sora",
        "inter":       "Inter",
        "dm":          "DM Sans",
        "jakarta":     "Plus Jakarta Sans",
        "outfit":      "Outfit",
        "raleway":     "Raleway",
        "nunito":      "Nunito",
        "poppins":     "Poppins",
    }

    resolved_font = font_map.get(font.lower(), font)  # fallback to raw font name if not in map
    google_font_url = resolved_font.replace(" ", "+")

    return f"""
    <link href="https://fonts.googleapis.com/css2?family=Anton+SC&family=Arbutus&family=Bebas+Neue&family=Dancing+Script:wght@400..700&family=Fontdiner+Swanky&family=Girassol&family=Give+You+Glory&family=Goldman:wght@400;700&family=Hanken+Grotesk:ital,wght@0,100..900;1,100..900&family=Leckerli+One&family=Nosifer&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Rajdhani:wght@300;400;500;600;700&family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Rubik+Vinyl&family=Sour+Gummy:ital,wght@0,100..900;1,100..900&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&family=Uncial+Antiqua&family=Zen+Dots&display=swap" rel="stylesheet">
    <h1 style="
        text-align: center;
        font-family: '{resolved_font}', sans-serif;
        background: linear-gradient(90deg, {gradient});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: {font_size};
        letter-spacing: {letter_spacing};
        font-weight: {weight};
        margin: 0.5rem auto 1.5rem auto;
        padding: 0.5rem 1rem;
        display: block;
        line-height: 1.3;
    ">{text}</h1>
"""

def sub_head_formatting(text:str,color,font='Hanken Grotesk',font_weight='500'):
    return f"""
    <p style="
        text-align: center;
        font-family:{font}, sans-serif;
        color: {color};
        font-size: 0.8rem;
        font-weight: {font_weight};
        letter-spacing: -0.5px;
        margin: -50px
    ">{text}</p>
"""
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
    <link href="https://fonts.googleapis.com/css2?family={google_font_url}:wght@{weight}&display=swap" rel="stylesheet">
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

def sub_head_formatting(text:str,color,font='Inter',font_weight='700'):
    return f"""
    <p style="
        text-align: center;
        font-family:{font}, sans-serif;
        color: {color};
        font-size: 1.5rem;
        font-weight: {font_weight};
        letter-spacing: 0.3px;
    ">{text}</p>
"""
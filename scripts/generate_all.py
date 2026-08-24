import os
import sys

def main():
    print("Executing all profile SVG generators...")
    
    import portrait
    portrait.generate_portrait_svg("hamza.png")

    import hero
    hero.main()
    
    import signature
    signature.main()

    import cards
    cards.main()

    import toolbox
    toolbox.main()

    import languages
    languages.main()

    import journey
    journey.main()

    import pulse
    pulse.main()

    print("All profile SVGs generated successfully!")

if __name__ == "__main__":
    main()

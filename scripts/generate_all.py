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

    import radars
    radars.main()

    import contributions_3d
    contributions_3d.main()

    import snake_local
    snake_local.main()

    import journey
    journey.main()

    import github_stats
    github_stats.main()

    print("All profile SVGs generated successfully!")

if __name__ == "__main__":
    main()

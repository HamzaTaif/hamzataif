import os
import sys

def main():
    print("Executing profile SVG generators...")
    
    # Only run portrait generator if source image hamza.png is present in workspace
    if os.path.exists("hamza.png"):
        try:
            import portrait
            portrait.generate_portrait_svg("hamza.png")
        except Exception as e:
            print(f"Skipping portrait generation: {e}")
    else:
        print("Notice: hamza.png not found. Preserving existing static portrait SVGs.")

    import name
    name.main()

    import signature
    signature.main()

    import cards
    cards.main()

    import toolbox
    toolbox.main()

    import radars
    radars.main()

    import journey
    journey.main()

    import github_stats
    github_stats.main()

    print("Profile SVGs generated successfully!")

if __name__ == "__main__":
    main()

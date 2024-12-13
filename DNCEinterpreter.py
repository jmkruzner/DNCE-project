from PIL import Image
import imageio
import os
import sys
import subprocess



def extract_frames(gif_path):
    """Extract all frames from a GIF."""
    gif = Image.open(gif_path)
    frames = []
    
    # Extract all frames
    try:
        while True:
            gif.seek(gif.tell())  # Move to the next frame
            frame = gif.copy()
            frames.append(frame)
            gif.seek(gif.tell() + 1)  # Try to move to the next frame
    except EOFError:
        pass  # Reached the end of the GIF
    
    return frames

def resize_frames(frames, size=(300, 300)):
    """Resize all frames to the same size and convert to RGB to ensure uniformity."""
    resized_frames = []
    for frame in frames:
        frame = frame.resize(size, Image.Resampling.LANCZOS)  # High-quality resizing
        frame = frame.convert("RGB")  # Convert to RGB to avoid transparency issues
        resized_frames.append(frame)
    return resized_frames

def parse_dance(file_name):
    
    moves = []
    style = ""
    name = ""
    file = open(file_name)
    lines = file.readlines()
    if not lines[0].startswith("dance"):
        print("Error: program must start with keyword \"dance\"")
        quit()
    if lines[-1].lower() != "end dance":
        print("Error: program has no end.")
        quit()
    for line in lines:
        line = line.strip()
        if line.lower() == "dance":
            continue
        elif line.startswith("style"):
            style = line.split("=")[1].strip()
        elif line.startswith("name"):
            name = line.split("=")[1].strip()
        elif line.lower() == "end dance":
            break
        elif line:  # Non-empty line, i.e., a move
            moves.append(line.replace(" ", ""))
    if not style:
        print("Error: a style has not been chosen.")
        quit()
    if not name:
        print("Error: the dance has no name")
        quit()
    return moves, style, name


def combine_gifs(dance_steps, gif_folder, output_gif):
    """Combine multiple GIFs (with multiple frames) into one longer looped GIF."""
    # gif_files = [f for f in os.listdir(gif_folder) if f.endswith('.gif')]
    # gif_files.sort()
    
    gifs = []
    
    for step in dance_steps:
        gif_path = os.path.join(gif_folder, f"{step}.gif")
        
        if os.path.exists(gif_path):
            # Extract all frames from the GIF
            frames = extract_frames(gif_path)
        
            # Resize all frames to the same size and convert to RGB
            resized_frames = resize_frames(frames, size=(300, 300))
        
            # Add the resized frames to the list of all frames
            gifs.extend(resized_frames)
        else:
            print(f"Error: '{step}' is either an invalid step or spelled wrong.")
            quit()

    
    # Save the combined GIF with 1-second delay between each frame (20 fps)
    imageio.mimsave(output_gif, gifs, duration=0.03, loop=0)  # 20 frames per second (fps)
    print(f"Combined GIF saved as {output_gif}")
    

def interpret(file_name):
    moves, style, name = parse_dance(file_name)
    if style not in ["breaking", "ballet", "dancehall"]:
        print(f"Error: {style} is either unavailable or is spelled wrong. Try again.")
        quit()
    gif_folder = os.path.join("/Applications", f"{style} gifs")
    combinedGif = name + ".gif"
    combine_gifs(moves, gif_folder, combinedGif)
    # Open the GIF in Google Chrome
    subprocess.run(["open", "-a", "Google Chrome", combinedGif])
    


args = sys.argv
if len(args) < 2:
    print("No filename provided to interpreter")
elif len(args) == 2:
    filename = args[1]
    interpret(filename)
else:
    print("Too many arguments inputted into interpreter")



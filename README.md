# Video Generation Script

This project contains a script to generate videos with text overlays, zoom effects, padding, noise, and motion blur.

## Features

- Add text overlays from text files
- Apply zoom in, zoom out, and zoom pan effects
- Add padding and noise to the video
- Simulate camera shake
- Apply motion blur

## Requirements

- Python 3.x
- `ffmpeg` installed and available in your system's PATH
- Required Python packages (can be installed via `requirements.txt`)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/<USERNAME>/<REPO>.git
    cd <REPO>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg` is installed and available in your system's PATH.

## Usage

1. Prepare your text files for the quotes and author.
2. Set the paths to these files and other parameters in the script.
3. Run the script:
    ```sh
    python generate_video.py
    ```

## Script Details

### Text Overlays

- The script checks for the existence of text files for quotes and author.
- If the files exist, it creates text overlays using `drawtext` filter in `ffmpeg`.

### Zoom Effects

- `zoom_in`: Gradually zooms in.
- `zoom_in_center`: Gradually zooms in, centered.
- `zoom_out`: Gradually zooms out.

### Other Effects

- `padding`: Adds padding around the video.
- `noise`: Adds noise to the video.
- `camera_shake`: Simulates a slight zoom and pan effect to mimic camera shake.
- `motion_blur`: Adds motion blur using `tblend`.

### Combining Filters

- The script combines non-empty filters into a single filter chain.

## Example

```python
# Example usage in generate_video.py
filters = [camera_shake, noise, motion_blur, padding]
if first_text_overlay:
    filters.append(first_text_overlay)
# Combine filters and apply to video

import streamlit as st
import os
import time
from typing import Literal
from moviepy import VideoFileClip
from pygifsicle import gifsicle

def convert_video_to_gif(movie, fps=10):
  output_file = os.path.join(OUTPUT_DIR, f"{st.session_state.filename}.gif")
  print(f"output to {output_file}")
  bytes_data = movie.read()
  input_file = os.path.join(OUTPUT_DIR, movie.name)
  with open(input_file, "wb") as f:
    f.write(bytes_data)
  clip = VideoFileClip(input_file)
  clip.write_gif(output_file, fps=fps)
  os.remove(input_file)
  st.success("Successflly converted Movie to GIF")
  st.image(output_file)
  st.download_button(
    label="Download (Original Size)",
    data=open(output_file, "br"),
    file_name="output.gif",
    mime="image/gif"
  )
  return True

def optimize_gif(optimize_level: Literal[1, 2, 3]=3):
  input_file = os.path.join(OUTPUT_DIR, f"{st.session_state.filename}.gif")
  output_file = os.path.join(OUTPUT_DIR, f"{st.session_state.filename}_optimized.gif")
  print(f"input from {input_file}")
  print(f"output to {output_file}")
  gifsicle(
    sources=input_file,
    destination=output_file,
    optimize=False,
    colors=256,
    options=[f"--optimize={optimize_level}"]
  )
  st.success("Successflly Optimized GIF")
  st.image(output_file)
  st.download_button(
    label="Download (Optimized)",
    data=open(output_file, "br"),
    file_name="output.gif",
    mime="image/gif"
  )

if "convert" not in st.session_state:
    st.session_state.convert = False
if "filename" not in st.session_state:
  st.session_state.filename = f"{time.time()}"

OUTPUT_DIR = "/tmp"

def main():
  st.title("Movie to GIF converter")
  movie = st.file_uploader("upload movie file", type=["mp4", "mov"], accept_multiple_files=False)
  st.video(movie)

  if movie:
    fps = st.slider("select frame rate", min_value=1, max_value=60, value=10)
    if st.button("convert"):
      with st.spinner("converting..."):
        st.session_state.filename = f"{time.time()}"
        convert_video_to_gif(movie, fps=fps)
        st.session_state.convert = True
    if st.session_state.convert:
      optimized_level = st.selectbox("Select Optimize Level", [1, 2, 3])
      if st.button("optimize"):
        with st.spinner("optimizing..."):
          optimize_gif(optimize_level=optimized_level)

if __name__ == "__main__":
  main()

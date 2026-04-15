import streamlit as st
import os
import time
from moviepy import VideoFileClip
import imageio
from PIL import Image
import numpy as np

# 一時ディレクトリの設定
OUTPUT_DIR = "/tmp"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def convert_media(input_path, output_ext, fps=10):
    """
    主要な変換ロジックを一括管理
    """
    output_filename = f"converted_{int(time.time())}.{output_ext}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    clip = VideoFileClip(input_path)
    
    try:
        if output_ext == "mp3":
            # 動画から音声を抽出
            if clip.audio is not None:
                clip.audio.write_audiofile(output_path)
            else:
                st.error("このファイルには音声が含まれていません。")
                return None
                
        elif output_ext == "gif":
            clip.write_gif(output_path, fps=fps, logger=None)
            
        elif output_ext == "apng":
            # 動画の全フレームをリスト化してAPNGとして保存
            frames = [np.array(frame) for frame in clip.iter_frames(fps=fps)]
            imageio.mimsave(output_path, frames, format='APNG', fps=fps)
            
        elif output_ext in ["mp4", "mov"]:
            # 動画フォーマット変換
            # MOVからMP4、またはその逆。codecを指定することで互換性を確保
            codec = "libx264" if output_ext == "mp4" else None
            clip.write_videofile(output_path, codec=codec, audio_codec="aac", logger=None)
            
        return output_path
    except Exception as e:
        st.error(f"変換エラー: {e}")
        return None
    finally:
        clip.close()

def main():
    st.title("マルチメディア・コンバーター Pro")
    st.markdown("MP3, MOV, MP4, GIF, APNG 相互変換アプリ")

    # ファイルアップロード
    supported_types = ["mp4", "mov", "gif", "apng", "mp3"]
    uploaded_file = st.file_uploader("ファイルをアップロード", type=supported_types)

    if uploaded_file:
        # 一時保存
        input_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # プレビュー表示
        if uploaded_file.name.endswith(("mp4", "mov")):
            st.video(uploaded_file)
        elif uploaded_file.name.endswith(("gif", "apng")):
            st.image(uploaded_file)

        # 変換設定
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            target_ext = st.selectbox("出力フォーマットを選択", supported_types)
        
        with col2:
            fps = st.slider("フレームレート (fps)", 1, 60, 10)

        if st.button("変換開始"):
            with st.spinner("変換中..."):
                result_path = convert_media(input_path, target_ext, fps)
                
                if result_path and os.path.exists(result_path):
                    st.success(f"変換完了: {target_ext}")
                    
                    # ダウンロードボタン
                    with open(result_path, "rb") as f:
                        btn = st.download_button(
                            label=f"{target_ext.upper()}をダウンロード",
                            data=f,
                            file_name=f"converted_file.{target_ext}",
                            mime=f"application/octet-stream"
                        )
                    
                    # 変換後のプレビュー
                    if target_ext in ["mp4", "mov"]:
                        st.video(result_path)
                    elif target_ext in ["gif", "apng"]:
                        st.image(result_path)
                    elif target_ext == "mp3":
                        st.audio(result_path)

if __name__ == "__main__":
    main()

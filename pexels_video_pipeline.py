name: Video Pipeline

on:
  workflow_dispatch:

jobs:
  run-video-pipeline:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install FFmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg

      - name: Install Dependencies
        run: pip install requests

      - name: Run Video Pipeline
        env:
          PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        run: python pexels_video_pipeline.py

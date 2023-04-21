# YouTube Speech-To-Text Module Using By [DerevoVoli.org](https://derevovoli.org)

Requires installed `python3.10` interpeter and `ffmpeg` tools by the next command
```
sudo apt-get install -y libav-tools
```

To use this reposetory please make the next steps:

Install virtual environment:
```
python3 -m venv venv
```

Virtual environment activation:
```
source venv/bin/activate
```

Dependencies installation:
```
pip3 install -r requirements.txt
```

To execute a program run next command:
```
python3 main.py --video <youtube-video-link>
```
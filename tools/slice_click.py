#!/usr/bin/env python3
"""Нарезает короткий звук клавиши на отдельные звуки.

    python3 tools/slice_click.py                      # mech_click.wav -> key_down_*.wav, key_up_*.wav
    python3 tools/slice_click.py my_recording.wav     # то же из своего файла (поправь окна ниже)

mech_click.wav длится 36 мс и содержит одно событие: главный удар (~11,5 мс) и слабый
второй контакт (~18,5 мс). Из удара получаются звуки нажатия (разной длины хвоста),
из второго контакта звуки отпускания. Окна заданы в миллисекундах от начала файла.
Если запись длинная и в ней много нажатий, добавь в DOWN/UP свои окна (начало, конец).
"""
import sys, wave, os
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'sounds', 'mech_click.wav')
OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'sounds')

DOWN = [(11.0, 15.5), (11.0, 18.0), (11.0, 26.0)]   # нажатие: только удар / с коротким хвостом / с хвостом и вторым контактом
UP   = [(17.8, 22.0), (17.8, 27.0)]                  # отпускание: второй контакт / он же с хвостом
PEAK = 0.9                                           # пик каждого куска; в приложении отпускание тише (см. click() в index.html)

w = wave.open(SRC)
sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
if w.getnchannels() > 1:
    x = x.reshape(-1, w.getnchannels()).mean(1)

def cut(a, b):
    s = x[int(a * sr / 1000):int(b * sr / 1000)].copy()
    fi, fo = max(1, int(sr * .0003)), max(1, int(len(s) * .35))
    s[:fi] *= np.linspace(0, 1, fi)
    s[-fo:] *= np.linspace(1, 0, fo)
    pk = np.abs(s).max()
    return s * (PEAK / pk) if pk > 0 else s

def save(name, s):
    with wave.open(os.path.join(OUT, name), 'wb') as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
        o.writeframes((np.clip(s, -1, 1) * 32767).astype('<i2').tobytes())
    print(name, '%.1f мс' % (len(s) * 1000 / sr))

for i, (a, b) in enumerate(DOWN, 1): save('key_down_%d.wav' % i, cut(a, b))
for i, (a, b) in enumerate(UP, 1):   save('key_up_%d.wav' % i, cut(a, b))

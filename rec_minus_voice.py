import numpy as np
from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav

fs = 48000  # частота дискретизації
recording = None
is_recording = False

voice_file = "minus_voice_record.wav"  # файл з голосом
minus_track = "MinusDuHast.mp3"  # мінусовка

# Індекс вбудованого мікрофона, може бути іншим
MIC_DEVICE_ID = 15
GAIN = 4.0   # гучність при запису, 1.0 — без змін, 2–4 — норм для голосу

# Pygame
init()
mixer.init()
mixer.music.set_volume(0.5)

window = display.set_mode((1200, 600))
display.set_caption("Запис голосу")
clock = time.Clock()

font.init()
font_big = font.SysFont("Arial", 32)

btn_rect = Rect(425, 250, 350, 80)
rect_color = "white"
btn_text = "Запис"


def start_voice_record():
    global recording
    recording = sd.rec(
        int(fs * 5),  # 5 секунд запису
        samplerate=fs,
        channels=1,  # МОНО
        dtype='int16',
        device=MIC_DEVICE_ID  # тільки мікрофон
    )


def stop_voice_record():
    global recording
    sd.wait()   # ЧЕКАЄМО, ПОКИ ЗАПИС ЗАВЕРШИТЬСЯ
    if recording is not None:
        # підсилення гучності
        recording = recording * GAIN
        # щоб не було "хрипів"
        recording = np.clip(recording, -32768, 32767)
        recording = recording.astype('int16')
        wav.write(voice_file, fs, recording)


def play_song_and_voice_together():
    mixer.music.load(minus_track)
    mixer.music.play()

    voice_sound = mixer.Sound(voice_file)
    voice_sound.play()

# Головний цикл
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):

                if not is_recording:
                    rect_color = "red"
                    btn_text = "Стоп і слухати"
                    is_recording = True

                    mixer.music.load(minus_track)
                    mixer.music.play()

                    start_voice_record()

                else:
                    rect_color = "white"
                    btn_text = "Запис"
                    is_recording = False

                    stop_voice_record()
                    play_song_and_voice_together()

    window.fill("grey")
    draw.rect(window, rect_color, btn_rect)
    text_surface = font_big.render(btn_text, True, "black")
    window.blit(text_surface, (btn_rect.x + 40, btn_rect.y + 25))

    display.update()
    clock.tick(30)

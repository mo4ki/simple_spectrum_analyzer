import pyaudio as pa
import numpy as np
import configs

# функция для прослушки микрофона
def listen():

    chunk = configs.chunk # чем меньше чанк - тем быстрее (1024 - минимум)
    sample_rate = configs.sample_rate
    format = pa.paInt16
    channels = 1

    p = pa.PyAudio()

    stream = p.open(
        format = format,
        channels = channels,
        rate = sample_rate,
        input = True,
        output = True,
        frames_per_buffer = chunk
    )
    
    return stream
    
# Функция, для расчёта fft и его фильтрации     
def fft(data):
    
    window = np.kaiser(configs.chunk, 5.5)

    frequencies = np.fft.fft(data)
    magnitudes = np.abs(frequencies)
    
    windowed_magnitudes = magnitudes * window
    result = filter(windowed_magnitudes, configs.fft_filter_multiplayer)
    
    return result

# простой фильтр украденный из просторов интернета
def filter(data, level):

    # Создание окна Хемминга
    window = np.hamming(level)

    # Нормализация окна Хемминга
    window /= np.sum(window)

    # Сглаживание данных с помощью фильтра Хемминга
    filtered = np.convolve(data, window, mode='same')

    return filtered
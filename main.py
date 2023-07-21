import pyaudio as pa
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
import configs

# ========alternative filter======
# def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    # from math import factorial
    # window_size = np.abs(np.int(window_size))
    # order = np.abs(np.int(order))
    # order_range = range(order+1)
    # half_window = (window_size -1) // 2
    # b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    # m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    # lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    # y = np.concatenate((firstvals, y, lastvals))
    # return np.convolve( m[::-1], y, mode='valid')

# Функция, для расчёта fft и его фильтрации     
def fft(data):
    
    window = np.kaiser(configs.chunk, 8)

    frequencies = np.fft.fft(data)
    magnitudes = np.abs(frequencies)
    
    windowed_magnitudes = magnitudes * window
    result = gaussian_filter(windowed_magnitudes, configs.fft_filter_multiplayer)
    
    # =====alternative fft=====
    # from scipy.fft import sfft 
    
    # window = np.kaiser(chunk, 8.5)
    # frequencies = sfft(data)
    # windowed_magnitudes = magnitudes * window
    
    # =====alternative filter====
    # result = savitzky_golay(windowed_magnitudes, 20, 5)
    
    return result
 
# функция для прослушки микрофона
def listen(function):

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
    
    # вызываем функцию из аргумента
    function(stream, chunk)
    
def wave(stream, chunk):

    # построение графика, для визуализации
    fig, ax = plt.subplots()
    
    ax.set_xlim(configs.wave_xlim)
    ax.set_ylim(configs.wave_ylim)

    # "Инициализируем" график.
    line, = ax.plot(np.zeros(chunk), '-')

    plt.show(block = False)

    while True:
        
        # Получаем данные из микрофона
        data = stream.read(chunk)
        data_int = np.frombuffer(data, dtype=np.int16)
        
        # сглаживаем данные
        result = gaussian_filter(data_int, config.wave_filter_multiplayer)
        
        # выводим данные
        line.set_ydata(result)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.update()
        fig.canvas.flush_events()

def frequencies(stream, chunk):

    # построение графика, для визуализации
    fig, ax = plt.subplots()

    ax.set_xlim(configs.frequencies_xlim)
    ax.set_ylim(configs.frequencies_ylim)

    # "Инициализируем" график.
    line, = ax.plot(np.zeros(chunk//2), '-')
    plt.show(block = False)

    while True:
        
        data = stream.read(chunk)
        data_int = np.frombuffer(data, dtype=np.int16) 
        
        # деление на 2 нужно
        # если его не будет, то график будет зеркалить
        # подробности в мат. части 
        result = fft(data_int)[:chunk//2]
        
        # выводим данные
        line.set_ydata(result)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.update()
        fig.canvas.flush_events()
        
def main():

    choice = input('\n Choice: \n\n [1]. Wave \n [2]. Frequencies \n >> ')
    
    if choice == '1':
        listen(wave)
        
    elif choice == '2':
        listen(frequencies)

    else:
        print('you made the wrong decision')
        exit()
        
if __name__ == '__main__':

    try:
        main()
        
    except KeyboardInterrupt:
        print('\n see you next time')
        exit()
        
    except Exception as e:
        print('\n', e)
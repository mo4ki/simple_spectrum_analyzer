import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import configs
import utils

def display_data(stream, work_type):

    chunk = configs.chunk
    
    # скрываем ненужное
    mpl.rcParams['toolbar'] = 'None'
    
    # перекрашиваем всё в чёрный
    plt.style.use("dark_background")
    
    # построение графика, для визуализации
    fig, ax = plt.subplots()
    
    if work_type == 'wave':
    
        ax.set_xlim(configs.wave_xlim)
        ax.set_ylim(configs.wave_ylim)
        
    elif work_type == 'frequencies':
    
        ax.set_xlim(configs.frequencies_xlim)
        ax.set_ylim(configs.frequencies_ylim)

    # "Инициализируем" график.
    line, = ax.plot(np.zeros(chunk), '-')

    # убираем циферки 
    plt.axis('off')
    
    # убираем отступы
    fig.tight_layout()
    plt.show(block = False)

    while True:
        
        # Получаем данные из микрофона
        data = stream.read(chunk)
        data_int = np.frombuffer(data, dtype=np.int16)

        # нормализуем данные
        
        if work_type == 'wave':
            result = utils.filter(data_int, configs.wave_filter_multiplayer)
        
        elif work_type == 'frequencies':
        
            # деление на 2 нужно
            # если его не будет, то график будет зеркалить
            # подробности в мат. части 
            result = utils.fft(data_int)
            
        # выводим данные
        line.set_ydata(result)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.update()
        fig.canvas.flush_events()

def main():

    choice = input('\n Choice: \n\n [1]. Wave \n [2]. Frequencies \n >> ')
    
    stream = utils.listen()
    
    if choice == '1':
        display_data(stream, 'wave')
        
    elif choice == '2':
        display_data(stream, 'frequencies')

    else:
        print('\n you made the wrong decision')
        exit()
        
if __name__ == '__main__':

    try:
        main()
        
    except KeyboardInterrupt:
        print('\n see you next time')
        exit()
        
    # except Exception as e:
        # print('\n', e)

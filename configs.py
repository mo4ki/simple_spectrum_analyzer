
chunk = 1024*2 # чем меньше чанк - тем быстрее (1024 - минимум)
sample_rate = 44100

# ylim -35000 на 35000 потому что при тестах больше волны не было
# если у вас это не так, то поменяйте
wave_xlim = (0, chunk)
wave_ylim = (-35000, 35000)

# для меня это - оптимальные значения
frequencies_xlim = (0, chunk//2.7)
frequencies_ylim = (0, 60000)

# множители для сглаживания
fft_filter_multiplayer = 7
wave_filter_multiplayer = 2
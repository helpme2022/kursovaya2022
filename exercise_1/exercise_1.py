from collections import defaultdict

with open("resourse_1.txt", "r", encoding="utf-8") as input_file:
    # Открываем файл и разбиваем текст на слова
    words = input_file.read().split()
    wdict = defaultdict(int)
    # Записываем из послученного списка в словарь после чего перебираем их в цикле
    for word in words:
        if word.isalpha():
            wdict[word] += 1
    # Сортируем сравнивая второе значение в обратном порядке (от большего к меньшему), иначе по первому
    sorted_words = sorted(wdict.items(), key=lambda x: (-x[1], x[0]))

    # Записываем полученный результат в файл
    with open("result_1.txt", "w", encoding="utf-8") as output_file:
        for word, count in sorted_words:
            print(word, count, file=output_file)

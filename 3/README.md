# Задание №3

## Постановка задачи:

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.

Входной текст на **учебном конфигурационном языке** принимается из
стандартного ввода. Выходной текст на **языке toml** попадает в файл, путь к
которому задан ключом командной строки.

Массивы:  
```list( значение, значение, значение, ... )```

Словари:  
```
$[
 имя : значение,
 имя : значение,
 имя : значение,
 ...
]
```

Имена:  
```[a-z]+```

Значения:
- Числа.
- Строки.
- Массивы.
- Словари.

Строки:  
```"Это строка"```

Объявление константы на этапе трансляции:  
```имя <- значение;```

Вычисление константного выражения на этапе трансляции (постфиксная
форма), пример:  
```#{имя 1 +}```

Результатом вычисления константного выражения является значение.

Для константных вычислений определены операции и функции:

1. Сложение.
2. Вычитание.
3. Умножение.
4. Деление.
5. max().

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

## Использованные технологии:

- Python
- toml
def simple_hash(input_string):
    # Простая функция хеширования без использования сторонних библиотек
    hash_value = 0
    
    # Простое смешивание символов исходной строки
    for char in input_string:
        hash_value = ord(char) + (hash_value << 6) + (hash_value << 16) - hash_value
    
    return hash_value

# Пример использования функции
input_string = "Hello, World!ahfkjhsdahfhasdhfkhk"
hashed_output = simple_hash(input_string)
print("Хеш для строки '{}' равен: {}".format(input_string, hashed_output))



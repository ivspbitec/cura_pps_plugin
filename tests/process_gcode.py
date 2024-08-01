import re

def process_gcode(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()

    skin_blocks = {}
    skin_top_layers = []

    block_id = 1
    inside_skin=False

    # Собираем все SKIN-блоки со всех слоев
    for layer_index in range(len(data)):
        line = data[layer_index].strip()
        
        if ";TYPE:SKIN" in line:
            inside_skin = True
            data[layer_index] = line + f" ;SKIN_BLOCK_ID:{block_id}\n"
            block_id += 1
            continue
             
       
        if inside_skin and (";TYPE:" in line or ";LAYER:" in line ):
            inside_skin = False
            continue
             

        if inside_skin:
            #match = re.search(r"X([\d\.]+) Y([\d\.]+) E([\d\.]+)", line)
            match = re.search(r"G1 X([\d\.]+) Y([\d\.]+) E([\d\.]+)", line)
 

            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                e = float(match.group(3))

                if layer_index not in skin_blocks:
                    skin_blocks[block_id] = []

                skin_blocks[block_id].append({
                    "id": block_id,
                    "x": x,
                    "y": y,
                    "e": e,
                    "line_index": layer_index
                })

          

    # Определяем верхние SKIN-блоки
    for layer_index in skin_blocks:
        for skin_block in skin_blocks[layer_index]:
            is_top = True
            for next_layer_index in range(layer_index + 1, len(data)):
                if next_layer_index in skin_blocks:
                    for next_skin_block in skin_blocks[next_layer_index]:
                        if (next_skin_block["x"] == skin_block["x"] and
                            next_skin_block["y"] == skin_block["y"]):
                            is_top = False
                            break
                if not is_top:
                    break

            if is_top:
                skin_top_layers.append(skin_block)

    # Выводим номера верхних слоев SKIN
    print("Номера верхних слоев `SKIN` блоков:", [block["id"] for block in skin_top_layers])

    with open('processed_' + file_path, 'w') as file:
        file.writelines(data)

# Запуск обработки
process_gcode('example.gcode')

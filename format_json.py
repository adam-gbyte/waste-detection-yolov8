import json

def json_satu_baris_ke_multi_baris(input_file, output_file, indent=4):
    """
    Membaca file JSON satu baris dan menulis ulang menjadi multi-baris.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

    print(f"File berhasil diformat ulang: {output_file}")


if __name__ == "__main__":
    input_file = "annotations.json"      # ganti sesuai nama file Anda
    output_file = "annotations_new.json"

    json_satu_baris_ke_multi_baris(input_file, output_file)

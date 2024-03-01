import matplotlib.pyplot as plt
import json

# Chuyển đổi dữ liệu từ tệp graph.txt sang graph.json
input_file_path = 'graph.txt'
output_file_path = 'graph.json'

# Đọc dữ liệu từ file graph.txt và chuyển đổi thành định dạng JSON
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

data = []
for line in lines:
    parts = line.split(", ")
    run_number = int(parts[0].split(": ")[0].split(" ")[1])
    time = float(parts[0].split(": ")[1][:-1])  # Loại bỏ ký tự 's' ở cuối
    incorrect = int(parts[1].split(":")[1])
    correct = int(parts[2].split(":")[1])
    data.append({"run": run_number, "elapsed_time": time, "incorrect": incorrect, "correct": correct})

# Ghi dữ liệu vào file graph.json
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)

# Đọc dữ liệu từ file graph.json và tạo biểu đồ
with open(output_file_path, 'r') as file:
    loaded_data = json.load(file)

# Trích xuất thông tin liên quan
incorrect_data = [entry["incorrect"] for entry in loaded_data]
elapsed_time_data = [entry["elapsed_time"] for entry in loaded_data]

# Vẽ biểu đồ
plt.scatter(incorrect_data, elapsed_time_data, marker='o', color='blue')
plt.xlabel('Number of Incorrect')
plt.ylabel('Elapsed Time (seconds)')
plt.title('Number of Incorrect vs Elapsed Time')
plt.grid(True)
plt.show()

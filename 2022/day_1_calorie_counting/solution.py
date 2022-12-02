calories = [0]
with open("input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line:
            calories[-1] += int(line)
        else:
            calories.append(0)

print(max(calories))

top_three_calories = 0
for i in range(3):
    top_three_calories += max(calories)
    idx = calories.index(max(calories))
    calories.pop(idx)

print(top_three_calories)

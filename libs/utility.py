import io


def file_to_array(path):
    with io.open(path, mode="r", encoding="utf-8") as f:
        lines = f.read()
    if lines[-1] == '\n':
        lines = lines[: -1]
    return lines.split('\n')


def array_to_file(path, data, delimiter):
    with io.open(path, mode="w", encoding="utf-8") as f:
        for line in data:
            for field in line[:-1]:
                if type(field) == int:
                    field = str(field).decode("utf-8")
                f.write(field + delimiter)
            f.write(line[-1] + '\n')

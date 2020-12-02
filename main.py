import importlib
import sys
import click


@click.command()
@click.argument("day", type=click.IntRange(1, 25))
@click.option("--parta", "part", flag_value="a")
@click.option("--partb", "part", flag_value="b")
def main(day, part):
    day = f"{int(day):02}"
    import_path = f"solutions.day{day}"
    data_path = f"day{day}.txt"

    try:
        day_module = importlib.import_module(import_path)
    except ModuleNotFoundError:
        print(f"Module {day} is not yet available")
        sys.exit(-65)

    print("Results:")
    print(run_day(data_path, day, day_module, part))


def run_day(data_path, day, day_module, part):
    if part == "a":
        return run_part(data_path, day, day_module, "A")
    elif part == "b":
        return run_part(data_path, day, day_module, "B")
    else:
        a = run_part(data_path, day, day_module, "A")
        b = run_part(data_path, day, day_module, "B")

        return f"Part A: \t {a}\r\nPart B: \t {b}\r\n"


def run_part(data_path, day, day_module, part):
    result = getattr(day_module, f"Day{day}Part{part}")()(data_path)
    return result


if __name__ == "__main__":
    main()

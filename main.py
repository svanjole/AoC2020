import importlib
import sys
import click
import timeit
import tqdm


@click.command()
@click.argument("day", type=click.IntRange(1, 25))
@click.option("--parta", "part", flag_value="a")
@click.option("--partb", "part", flag_value="b")
@click.option("--parte_a", "part", flag_value="ea")
@click.option("--parte_b", "part", flag_value="eb")
@click.option("-t", "--timeit", "timeit_", type=click.INT)
def main(day, part, timeit_):
    day = f"{int(day):02}"
    import_path = f"solutions.day{day}"
    data_path = f"day{day}.txt"

    try:
        day_module = importlib.import_module(import_path)
    except ModuleNotFoundError:
        print(f"Module {day} is not yet available")
        sys.exit(-65)

    if timeit_:
        execution_times = []
        results = ""
        for _ in tqdm.trange(timeit_):
            time_prior = timeit.default_timer()

            results = run_day(data_path, day, day_module, part)

            time_after = timeit.default_timer()
            execution_times.append(time_after - time_prior)

        average_time = sum(execution_times) / len(execution_times)

        print("Results:")
        print(results)
        print(
            f"Average running time: {average_time:.6f} seconds ({timeit_} iterations)"
        )

    else:
        print("Results:")
        print(run_day(data_path, day, day_module, part))


def run_day(data_path, day, day_module, part):
    if part == "a":
        return run_part(data_path, day, day_module, "A")
    elif part == "b":
        return run_part(data_path, day, day_module, "B")
    elif part == "ea":
        data_path = "example_" + data_path
        return run_part(data_path, day, day_module, "ExampleA")
    elif part == "eb":
        data_path = "example_" + data_path
        return run_part(data_path, day, day_module, "ExampleB")
    else:
        a = run_part(data_path, day, day_module, "A")
        b = run_part(data_path, day, day_module, "B")

        return f"Part A: \t {a}\r\nPart B: \t {b}\r\n"


def run_part(data_path, day, day_module, part):
    result = getattr(day_module, f"Day{day}Part{part}")()(data_path)

    return result


if __name__ == "__main__":
    main()

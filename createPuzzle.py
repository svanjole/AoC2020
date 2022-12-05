import os
import click


@click.command()
@click.argument("day", type=click.IntRange(1, 26))
@click.argument("year", type=click.IntRange(2022, 2026), default=2022)
def main(day, year):
    day = f"{int(day):02}"
    year = f"{int(year):04}"
    data_filename = f"day{day}.txt"
    puzzle_filename = f"day{day}.py"
    base_directory = f"solutions/{year}";
    data_base_directory = f"{base_directory}/data"

    if not os.path.isdir(base_directory):
        print("Year does not exist, creating folder structure")
        os.mkdir(base_directory)
        os.mkdir(data_base_directory)

    if os.path.isfile(f"{base_directory}/{puzzle_filename}"):
        print("Puzzle already exists, exiting program")
        exit()

    with open(f"{data_base_directory}/{data_filename}", 'w') as fp:
        pass

    with open('resources/puzzleTemplate.py') as f:
        lines = f.read()
    lines = lines.replace("##DAY##", day)

    with open(f"{base_directory}/{puzzle_filename}", 'w') as fp:
        fp.write(lines)

if __name__ == "__main__":
    main()

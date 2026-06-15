import csv
import random
from pathlib import Path


EMPTY = ""
MAX_ATTEMPTS = 20_000


def pause():
    input("\nEnter 키를 누르면 메뉴로 돌아갑니다...")


def ask_int(message, minimum=1, maximum=None):
    while True:
        raw = input(message).strip()
        try:
            value = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue

        if value < minimum:
            print(f"{minimum} 이상의 숫자를 입력해 주세요.")
            continue
        if maximum is not None and value > maximum:
            print(f"{maximum} 이하의 숫자를 입력해 주세요.")
            continue
        return value


def parse_names_from_text(text):
    names = []
    for chunk in text.replace(",", "\n").splitlines():
        name = chunk.strip()
        if name:
            names.append(name)
    return names


def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def input_students():
    print("\n학생 이름을 입력하세요.")
    print("쉼표 또는 줄바꿈으로 구분할 수 있습니다.")
    print("예: 김민수, 이서연, 박지훈")
    print("입력이 끝나면 빈 줄에서 Enter를 누르세요.\n")

    lines = []
    while True:
        line = input("> ")
        if not line.strip():
            break
        lines.append(line)

    return remove_duplicates(parse_names_from_text("\n".join(lines)))


def load_students_from_file():
    path = Path(input("불러올 파일 경로(.txt 또는 .csv): ").strip()).expanduser()
    if not path.exists():
        print("파일을 찾을 수 없습니다.")
        return None

    if path.suffix.lower() == ".csv":
        names = []
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                for cell in row:
                    cell = cell.strip()
                    if cell:
                        names.append(cell)
        return remove_duplicates(names)

    text = path.read_text(encoding="utf-8-sig")
    return remove_duplicates(parse_names_from_text(text))


def set_classroom():
    rows = ask_int("교실 행 수: ")
    cols = ask_int("교실 열 수: ")
    return rows, cols


def show_students(students):
    if not students:
        print("등록된 학생이 없습니다.")
        return

    print("\n등록된 학생:")
    for index, name in enumerate(students, start=1):
        print(f"{index:2}. {name}")


def manage_fixed_seats(students, rows, cols, fixed_seats):
    if not students:
        print("먼저 학생을 입력하거나 불러와 주세요.")
        pause()
        return fixed_seats

    while True:
        print("\n[고정 자리 설정]")
        print_fixed_seats(fixed_seats)
        print("1. 고정 자리 추가/수정")
        print("2. 고정 자리 삭제")
        print("3. 전체 삭제")
        print("0. 돌아가기")
        choice = input("선택: ").strip()

        if choice == "0":
            return fixed_seats
        if choice == "1":
            name = input("학생 이름: ").strip()
            if name not in students:
                print("학생 목록에 없는 이름입니다.")
                continue
            row = ask_int("행 번호: ", 1, rows)
            col = ask_int("열 번호: ", 1, cols)
            seat = (row - 1, col - 1)

            occupant = next((n for n, s in fixed_seats.items() if s == seat and n != name), None)
            if occupant:
                print(f"이미 {occupant} 학생이 고정된 자리입니다.")
                continue

            fixed_seats[name] = seat
            print("고정 자리를 저장했습니다.")
        elif choice == "2":
            name = input("삭제할 학생 이름: ").strip()
            if name in fixed_seats:
                del fixed_seats[name]
                print("삭제했습니다.")
            else:
                print("해당 학생의 고정 자리가 없습니다.")
        elif choice == "3":
            fixed_seats.clear()
            print("고정 자리를 모두 삭제했습니다.")
        else:
            print("메뉴 번호를 다시 선택해 주세요.")


def print_fixed_seats(fixed_seats):
    if not fixed_seats:
        print("고정 자리: 없음")
        return

    print("고정 자리:")
    for name, (row, col) in fixed_seats.items():
        print(f"- {name}: {row + 1}행 {col + 1}열")


def manage_forbidden_pairs(students, forbidden_pairs):
    if not students:
        print("먼저 학생을 입력하거나 불러와 주세요.")
        pause()
        return forbidden_pairs

    while True:
        print("\n[분리할 학생 설정]")
        print_forbidden_pairs(forbidden_pairs)
        print("1. 학생쌍 추가")
        print("2. 학생쌍 삭제")
        print("3. 전체 삭제")
        print("0. 돌아가기")
        choice = input("선택: ").strip()

        if choice == "0":
            return forbidden_pairs
        if choice == "1":
            first = input("첫 번째 학생 이름: ").strip()
            second = input("두 번째 학생 이름: ").strip()
            if first == second:
                print("서로 다른 학생을 입력해 주세요.")
                continue
            if first not in students or second not in students:
                print("학생 목록에 없는 이름이 있습니다.")
                continue
            forbidden_pairs.add(tuple(sorted((first, second))))
            print("분리할 학생쌍을 추가했습니다.")
        elif choice == "2":
            first = input("첫 번째 학생 이름: ").strip()
            second = input("두 번째 학생 이름: ").strip()
            pair = tuple(sorted((first, second)))
            if pair in forbidden_pairs:
                forbidden_pairs.remove(pair)
                print("삭제했습니다.")
            else:
                print("등록된 학생쌍이 아닙니다.")
        elif choice == "3":
            forbidden_pairs.clear()
            print("분리할 학생쌍을 모두 삭제했습니다.")
        else:
            print("메뉴 번호를 다시 선택해 주세요.")


def print_forbidden_pairs(forbidden_pairs):
    if not forbidden_pairs:
        print("분리할 학생쌍: 없음")
        return

    print("분리할 학생쌍:")
    for first, second in sorted(forbidden_pairs):
        print(f"- {first} / {second}")


def is_near(pos_a, pos_b):
    row_a, col_a = pos_a
    row_b, col_b = pos_b
    return max(abs(row_a - row_b), abs(col_a - col_b)) <= 1


def validate_arrangement(grid, forbidden_pairs):
    positions = {}
    for row_index, row in enumerate(grid):
        for col_index, name in enumerate(row):
            if name:
                positions[name] = (row_index, col_index)

    for first, second in forbidden_pairs:
        if first in positions and second in positions and is_near(positions[first], positions[second]):
            return False
    return True


def arrange_seats(students, rows, cols, fixed_seats, forbidden_pairs):
    if len(students) > rows * cols:
        raise ValueError("학생 수가 자리 수보다 많습니다.")

    unknown_fixed = [name for name in fixed_seats if name not in students]
    if unknown_fixed:
        raise ValueError(f"학생 목록에 없는 고정 자리 이름: {', '.join(unknown_fixed)}")

    fixed_positions = set(fixed_seats.values())
    if len(fixed_positions) != len(fixed_seats):
        raise ValueError("같은 자리에 여러 학생이 고정되어 있습니다.")

    movable_students = [name for name in students if name not in fixed_seats]
    empty_count = rows * cols - len(students)
    fill_items = movable_students + [EMPTY] * empty_count
    open_seats = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if (row, col) not in fixed_positions
    ]

    for _ in range(MAX_ATTEMPTS):
        random.shuffle(fill_items)
        grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

        for name, (row, col) in fixed_seats.items():
            grid[row][col] = name

        for (row, col), item in zip(open_seats, fill_items):
            grid[row][col] = item

        if validate_arrangement(grid, forbidden_pairs):
            return grid

    raise ValueError("조건을 만족하는 배치를 찾지 못했습니다. 고정 자리나 분리 조건을 줄여 보세요.")


def print_grid(grid):
    if not grid:
        print("아직 배치 결과가 없습니다.")
        return

    width = max(6, max((len(name) for row in grid for name in row if name), default=0) + 2)
    line = "+" + "+".join("-" * width for _ in grid[0]) + "+"

    print("\n[자리 배치 결과]")
    print("칠판")
    print(line)
    for row in grid:
        cells = []
        for name in row:
            label = name if name else "빈자리"
            cells.append(label.center(width))
        print("|" + "|".join(cells) + "|")
        print(line)


def print_status(students, rows, cols, fixed_seats, forbidden_pairs):
    print("\n" + "=" * 40)
    print("자리 뽑기 프로그램")
    print("=" * 40)
    print(f"학생 수: {len(students)}명")
    print(f"교실: {rows}행 x {cols}열 = {rows * cols}자리")
    print(f"고정 자리: {len(fixed_seats)}개")
    print(f"분리할 학생쌍: {len(forbidden_pairs)}개")
    print("-" * 40)


def main():
    students = []
    rows, cols = 5, 6
    fixed_seats = {}
    forbidden_pairs = set()
    last_grid = []

    while True:
        print_status(students, rows, cols, fixed_seats, forbidden_pairs)
        print("1. 학생 이름 직접 입력")
        print("2. 학생 이름 파일에서 불러오기")
        print("3. 학생 목록 보기")
        print("4. 교실 행/열 설정")
        print("5. 특정 학생 고정 자리 지정")
        print("6. 같이 앉으면 안 되는 학생 분리")
        print("7. 랜덤 자리 배치")
        print("8. 결과 화면 출력")
        print("0. 종료")

        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        if choice == "1":
            students = input_students()
            fixed_seats = {name: seat for name, seat in fixed_seats.items() if name in students}
            forbidden_pairs = {pair for pair in forbidden_pairs if pair[0] in students and pair[1] in students}
            last_grid = []
            print(f"{len(students)}명을 등록했습니다.")
            pause()
        elif choice == "2":
            loaded = load_students_from_file()
            if loaded is not None:
                students = loaded
                fixed_seats = {name: seat for name, seat in fixed_seats.items() if name in students}
                forbidden_pairs = {pair for pair in forbidden_pairs if pair[0] in students and pair[1] in students}
                last_grid = []
                print(f"{len(students)}명을 불러왔습니다.")
            pause()
        elif choice == "3":
            show_students(students)
            pause()
        elif choice == "4":
            rows, cols = set_classroom()
            fixed_seats = {
                name: seat
                for name, seat in fixed_seats.items()
                if seat[0] < rows and seat[1] < cols
            }
            last_grid = []
            print("교실 크기를 저장했습니다.")
            pause()
        elif choice == "5":
            fixed_seats = manage_fixed_seats(students, rows, cols, fixed_seats)
            last_grid = []
        elif choice == "6":
            forbidden_pairs = manage_forbidden_pairs(students, forbidden_pairs)
            last_grid = []
        elif choice == "7":
            try:
                last_grid = arrange_seats(students, rows, cols, fixed_seats, forbidden_pairs)
            except ValueError as error:
                print(f"배치 실패: {error}")
            else:
                print_grid(last_grid)
            pause()
        elif choice == "8":
            print_grid(last_grid)
            pause()
        else:
            print("메뉴 번호를 다시 선택해 주세요.")
            pause()


if __name__ == "__main__":
    main()

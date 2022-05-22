# Лист 1. Задание 8

start_dist = 10


def distance(day):
    return start_dist * 1.1 ** (day - 1)


def main():
    day = 1
    day_20 = None
    day_100 = None
    total_dist_100 = 0
    while True:
        dist_today = distance(day)
        total_dist_100 += dist_today
        if day_20 is None and dist_today >= 20:
            day_20 = day
            print(f'День, когда лыжник пробежал более 20 км за день - {day_20} ({dist_today} км)')
        if day_100 is None and total_dist_100 >= 100:
            day_100 = day
            print(f'День, когда лыжник суммарно за все дни пробежал более 100 км - {day_100} ({total_dist_100} км)')
        if (day_20 is not None) and (day_100 is not None):
            break
        day += 1


if __name__ == "__main__":
    main()

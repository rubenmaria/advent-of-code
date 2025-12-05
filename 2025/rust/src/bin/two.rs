use std::ops::RangeInclusive;

fn main() {
    let ranges = include_str!("real.input")
        .split(",")
        .map(|x| (x.split("-").nth(0).unwrap(), x.split("-").nth(1).unwrap()))
        .map(|(x, y)| (x.trim(), y.trim()))
        .map(|(x, y)| (x.parse::<i64>().unwrap(), y.parse::<i64>().unwrap()))
        .map(|(x, y)| x..=y)
        .collect::<Vec<RangeInclusive<i64>>>();
    println!("{:?}", ranges);
    part_one(&ranges);
    part_two(&ranges);
}

fn part_one(ranges: &Vec<RangeInclusive<i64>>) {
    let mut invalid_id_sum = 0;
    let mut number_string: String;
    let mut number_length: usize;
    let mut first_half: String;
    let mut second_half: String;
    for range in ranges {
        for number in range.clone() {
            number_string = number.to_string();
            number_length = number_string.len();

            if number_length % 2 != 0 {
                continue;
            }

            first_half = number_string[..number_length.div_euclid(2)].to_string();
            second_half = number_string[number_length.div_euclid(2)..].to_string();

            if first_half == second_half {
                invalid_id_sum += number
            }
        }
    }
    println!("solution1={}", invalid_id_sum)
}

fn part_two(ranges: &Vec<RangeInclusive<i64>>) {
    let mut invalid_id_sum = 0;
    let mut number_string;
    let mut number_length;
    for range in ranges {
        for number in range.clone() {
            number_string = number.to_string();
            number_length = number_string.len();
            for part_length in 1..=number_length.div_euclid(2) {
                if number_length % part_length != 0 {
                    continue;
                }
                if number_string[..part_length].repeat(number_length / part_length) == number_string
                {
                    invalid_id_sum += number;
                    break;
                }
            }
        }
    }
    println!("solution2={}", invalid_id_sum)
}

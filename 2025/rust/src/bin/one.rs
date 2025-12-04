fn main() {
    let rotations: Vec<&str> = include_str!("real.input")
        .split("\n")
        .filter(|x| !x.is_empty())
        .collect::<Vec<&str>>();

    part_one(&rotations);
    part_two(&rotations);
}

fn part_one(rotations: &Vec<&str>) {
    let mut current_value: i32 = 50;
    let mut last_value: i32;
    let mut zero_count = 0;
    let mut current_rotation: i32;

    for rotation in rotations.iter() {
        last_value = current_value;
        if rotation.starts_with("R") {
            current_rotation = rotation.strip_prefix("R").unwrap().parse::<i32>().unwrap();
            current_value += current_rotation;
        } else {
            current_rotation = rotation.strip_prefix("L").unwrap().parse::<i32>().unwrap();
            current_value -= current_rotation;
        }
        current_value = current_value.rem_euclid(100);
        if current_value.rem_euclid(100) == 0 {
            zero_count += 1;
        }
    }
    println!("solution1={}", zero_count)
}

fn part_two(rotations: &Vec<&str>) {
    let mut position: i32 = 50;
    let mut through_zero = 0;
    let mut rotation_amount: i32;
    let mut forward_in_direction: fn(i32) -> i32;

    for rotation in rotations.iter() {
        rotation_amount = rotation[1..].parse::<i32>().unwrap();
        forward_in_direction = if rotation.starts_with("R") {
            |x: i32| x + 1
        } else {
            |x: i32| x - 1
        };
        for _ in 0..rotation_amount {
            position = forward_in_direction(position);
            if position.rem_euclid(100) == 0 {
                through_zero += 1;
            }
        }
    }
    println!("solution2={}", through_zero)
}

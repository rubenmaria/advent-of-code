

fn main() {
    let rotations: Vec<&str> = include_str!("real.input")
    .split("\n")
    .filter(|x| !x.is_empty())
    .collect:: <Vec<&str>>();

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
        if current_value.rem_euclid(100) == 0{
            zero_count += 1;
        }
        println!(
            "last_value={}; current_value={}; rotation={}; zero_count={}",
            last_value, current_value, current_rotation, zero_count
        )
    }
    println!("solution={}", zero_count)
}

fn part_two(rotations: &Vec<&str>) {
    let mut position: i32 = 50;
    let mut last_position: i32;
    let mut through_zero = 0;
    let mut rotation_amount: i32;
    let mut current_laps: i32;
    let mut current_value: i32;

    for rotation in rotations.iter() {
        last_position = position;
        rotation_amount = rotation[1..].parse::<i32>().unwrap();

        if rotation.starts_with("R") {
            position += rotation_amount;
            current_value = last_position.rem_euclid(100) + rotation_amount;
        } else {
            position -= rotation_amount;
            current_value = last_position.rem_euclid(100) - rotation_amount;
        }

        current_laps = rotation_amount.div_euclid(100).abs();

        if last_position.rem_euclid(100) == 0 {
            through_zero += current_laps;
        } else if position.rem_euclid(100)  == 0 {
            through_zero += 1 + current_laps;
        } else if current_value < 0 || current_value > 100 {
            through_zero += 1+ current_laps;
        }
        
        println!(
            "last_position={}; current_position={}; rotation={}; zero_count={}, current_laps={}, current_value={}",
            last_position, position, rotation_amount, through_zero, current_laps, current_value
        );

        println!("=========================================");
    }
    println!("solution={}", through_zero)
}
use std::{collections::HashSet, u32};

fn main() {
    let banks = include_str!("test.input")
        .split("\n")
        .filter(|x| !x.is_empty())
        .map(|x| {
            x.chars()
                .map(|x| x.to_digit(10).unwrap())
                .collect::<Vec<u32>>()
        })
        .collect::<Vec<Vec<u32>>>();

    println!("solution1={}", biggest_joltages_sum(&banks, 2))
}

fn biggest_joltages_sum(banks: &Vec<Vec<u32>>, joltage_size: u32) -> u32 {
    let mut visited_joltage = (0..joltage_size)
        .map(|_| HashSet::<usize>::new())
        .collect::<Vec<HashSet<usize>>>();
    return banks
        .iter()
        .map(|x| {
            biggest_joltage(
                x,
                joltage_size,
                &mut visited_joltage,
                0,
                &mut vec![],
                u32::MIN,
            )
        })
        .sum();
}

fn biggest_joltage(
    bank: &Vec<u32>,
    joltage_size: u32,
    visited: &mut Vec<HashSet<usize>>,
    current_index: usize,
    current_values: &mut Vec<u32>,
    current_max: u32,
) -> u32 {
    if current_values.len() == joltage_size as usize {
        let value = current_values
            .iter()
            .map(|x| x.to_string())
            .fold(String::new(), |acc, x| acc + &x)
            .parse::<u32>()
            .unwrap();
        if current_max > value {
            println!("{}", current_max);
            for visit in visited {
                visit.clear()
            }
            return current_max;
        } else {
            current_values.clear();
            return biggest_joltage(bank, joltage_size, visited, 0, current_values, value);
        }
    }

    if let Some((index, value)) =
        get_valid_argmax(bank, joltage_size, &visited[current_index], current_index)
    {
        current_values.push(value);
        visited[current_index].insert(index);
        return biggest_joltage(
            bank,
            joltage_size,
            visited,
            current_index + 1,
            current_values,
            current_max,
        );
    } else {
        println!("{:?}", current_values);
        return current_values
            .iter()
            .map(|x| x.to_string())
            .fold(String::new(), |acc, x| acc + &x)
            .parse::<u32>()
            .unwrap();
    }
}

fn get_valid_argmax(
    bank: &Vec<u32>,
    joltage_size: u32,
    current_visited: &HashSet<usize>,
    current_index: usize,
) -> Option<(usize, u32)> {
    let mut max = u32::MIN;
    let mut max_index = 0;
    for i in current_index + 1..bank.len() {
        if i > bank.len() - joltage_size as usize + current_index {
            break;
        }
        if bank[i] > max && !current_visited.contains(&i) {
            max = bank[i];
            max_index = i;
        }
    }
    if max == u32::MIN {
        None
    } else {
        Some((max_index, max))
    }
}

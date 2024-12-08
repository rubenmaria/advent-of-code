 use std::time::Instant;

#[derive(Debug)]
struct ReportRow {
    springs: Vec<u8>,
    spring_group_count: Vec<u8>,
    question_mark_positions: Vec<usize>
}

fn main() {
    let reports = parse_report(include_str!("records.input"));
    let arrangements_sum = reports.iter()
        .map(|x| get_valid_possiblities(
                    &x.spring_group_count,
                    &x.question_mark_positions,
                    0,
                    springs_to_bits(&x.springs)
                )
            ).sum::<u128>();
    println!("{:?}", arrangements_sum);

    let mut reports_times_five = times_five(&reports);

    println!("max {:?}", reports_times_five.iter()
             .map(|x| x.question_mark_positions.len()).max().unwrap());
    
    {
        reports_times_five.sort_by_key(|x| x.question_mark_positions.len());
        let now = Instant::now();
        let max_questions = &reports_times_five[89];
        println!("{:?}", max_questions.question_mark_positions.len());
        let x = get_valid_possiblities(
            &max_questions.spring_group_count,
            &max_questions.question_mark_positions,
            0,
            springs_to_bits(&max_questions.springs)
        );
        let elapsed = now.elapsed();
        println!("Elapsed: {:.2?}", elapsed);
        /*
        let arrangements_sum = reports_times_five.iter()
            .map(|x| get_valid_possiblities(
                        &x.spring_group_count,
                        &x.question_mark_positions,
                        0,
                        springs_to_bits(&x.springs)
                    )
                ).sum::<u128>();
        println!("{:?}", arrangements_sum);
        */
    }
    /*
    let test = parse_report_row("????.#...#...?\
            ????.#...#...?????.#...#...?????.#...#...?\
            ????.#...#... 4,1,1,4,1,1,4,1,1,4,1,1,4,1,1");
    
    println!("bits: {:#032b}", springs_to_bits(&test.springs));
    println!("valid possib: {}", get_valid_possiblities(
                &test.spring_group_count,
                &test.question_mark_positions,
                0,
                springs_to_bits(&test.springs)
            )
    );
    */
}

fn times_five(reports: &Vec<ReportRow>) -> Vec<ReportRow>{
    let mut new_reports = vec![];
    for row in reports {
        let mut new_springs = vec![];
        let mut new_group_count = vec![];
        for i in 0..5 {
            new_group_count.extend(row.spring_group_count.clone());
            new_springs.extend(row.springs.clone());
            if i < 4 {
                new_springs.push(b'?')
            }             
        }
        new_reports.push(
            ReportRow {
                spring_group_count: new_group_count,
                question_mark_positions: new_springs.iter()
                    .enumerate()
                    .filter(|(_,x)| **x == b'?')
                    .map(|(i,_)| i)
                    .collect(),
                springs: new_springs
            }
            
        );
    }
    new_reports
}

fn parse_report(raw: &str) -> Vec<ReportRow> {
    raw.split("\n")
        .filter(|x| !x.is_empty())
        .map(parse_report_row)
        .collect()
}

fn parse_report_row(raw: &str) -> ReportRow {
    let (springs_raw, counts_raw) = raw.split_once(" ").unwrap();
    ReportRow {
        springs: springs_raw.bytes().collect(),
        spring_group_count: counts_raw.split(",")
            .map(|x| x.parse::<u8>().unwrap())
            .collect(),
        question_mark_positions: springs_raw.bytes()
            .enumerate()
            .filter(|(_,x)| *x == b'?')
            .map(|(i,_)| i)
            .collect()
    }
}

fn is_already_not_possible(group_counts: &[u8], question_marks: &[usize], 
                           question_mark_index: usize, springs: u128) -> bool { 
    let remaining_possible_ones = question_marks.len() - question_mark_index;
    let possible_ones = springs.count_ones() as usize + remaining_possible_ones;
    if (possible_ones as u8) < group_counts.iter().sum() {
        return true
    }
    let lower_bound = springs.trailing_zeros() as usize;
    let higher_bound = 128 - springs.leading_zeros() as usize;
    let mut current_ones = 0;
    let mut current_group_index = 0;
    for i in lower_bound..higher_bound {
        if ! (0..group_counts.len()).contains(&current_group_index) {
            if question_marks[question_mark_index] > i {
                return true
            } 
            break
        }
        if (springs & set_nth_bit(0, i)) > 0 {
            current_ones += 1;
        } else if current_ones != 0 {
            if group_counts[current_group_index] != current_ones && 
                question_marks[question_mark_index] > i{
                return true
            }
            current_group_index += 1;
            current_ones = 0;
        }
    }
    false
}


fn get_valid_possiblities(groups: &[u8], question_marks: &[usize], 
                          question_mark_index: usize, current_spirng:u128)
    -> u128 {

    if question_marks.len() <= question_mark_index {
        //println!("current_spring: {:#032b}", current_spirng);
        //println!("is_valid: {}", is_spring_bits_valid(current_spirng, groups));
        return is_spring_bits_valid(current_spirng, groups) as u128
    }

    if is_already_not_possible(groups, question_marks, question_mark_index,
                               current_spirng) {
        return 0
    }
    //println!("{:?}", question_marks);
    //println!("current_spring: {:#032b}", current_spirng);

    let one_set = set_nth_bit(
        current_spirng,
        question_marks[question_mark_index]
    );
    let new_index = question_mark_index + 1;
    get_valid_possiblities(groups, question_marks, new_index, current_spirng)
        + get_valid_possiblities(groups, question_marks, new_index, one_set)
}

fn is_spring_bits_valid(springs: u128, group_counts: &[u8]) -> bool {
    if springs.count_ones() as u8 != group_counts.iter().sum()  {
        return false
    }
    let lower_bound = springs.trailing_zeros() as usize;
    let higher_bound = 128 - springs.leading_zeros() as usize;
    let mut current_ones = 0;
    let mut current_group_index = 0;
    for n in lower_bound..higher_bound {
        if ! (0..group_counts.len()).contains(&current_group_index) {
            return false
        }

        if (springs & set_nth_bit(0, n)) > 0 {
            current_ones += 1;
            //println!("one at pos: {}", n);
            //println!("current ones: {}", current_ones);
        } else if current_ones != 0 {
            //println!("{} == {}", group_counts[current_group_index], current_ones);
            if group_counts[current_group_index] != current_ones {
                return false
            }
            current_group_index += 1;
            current_ones = 0;
        }
    }
    //println!("index end: {}", current_group_index);
    group_counts[current_group_index] == group_counts[group_counts.len()-1]
        &&  current_group_index == group_counts.len() -1
}

fn springs_to_bits(springs: &[u8]) -> u128 {
    springs.iter()
        .enumerate()
        .fold(0, |x,(i,&v)| 
              if v == b'#' {
                  //println!("index: {}", i);
                  set_nth_bit(x,i)
              } else {
                  x
              })
}

fn set_nth_bit(x: u128, n: usize) -> u128 {
    x | (1 << n)
}




fn main() {
    let sequence = include_str!("sequence-test").split(",")
        .map(|x| x.trim())
        .map(str::to_string)
        .collect::<Vec<String>>();
    println!("{:?}", sequence);
    let hash_sum: usize = sequence.iter()
        .map(|x| hash(&x))
        .sum();
    println!("hash sum: {}", hash_sum);
    println!("hash: qp= {}", hash("qp"))
}

fn hash(str: &str) -> usize {
    let mut current_hash_value = 0;
    for ch in str.bytes() {
        current_hash_value += ch as usize;
        current_hash_value *= 17;
        current_hash_value %= 256;
    }
    current_hash_value
}

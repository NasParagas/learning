fn main() {
    for input_line in std::io::stdin().lines() {
        if let Ok(line) = input_line {
            let words: Vec<_> = line.split(" ").collect();
            println!("Line: {words:?}")
        }
    }
}

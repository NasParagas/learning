// 標準入力が数字かそうでないかで処理を分ける
fn main() {
    for input_line in std::io::stdin().lines() {
        let mut stack: Vec<i32> = vec![];
        if let Ok(line) = input_line {
            let words: Vec<_> = line.split(" ").collect();
            // println!("Line: {words:?}")
            for word in words {
                if let Ok(parsed_word) = word.parse::<i32>() {
                    stack.push(parsed_word);
                } else {
                    match word {
                        "+" => add(&mut stack),
                        "-" => sub(&mut stack),
                        "*" => mul(&mut stack),
                        "/" => div(&mut stack),
                        _ => panic!("{word:?} could not be parsed"),
                    }
                }
            }
            println!("stack: {stack:?}")
        }
    }
}

fn add(stack: &mut Vec<i32>) {
    // pop().expect("error")の方が安全
    let lhs = stack.pop().unwrap();
    let rhs = stack.pop().unwrap();
    stack.push(lhs + rhs)
}
fn sub(stack: &mut Vec<i32>) {
    // pop().expect("error")の方が安全
    let lhs = stack.pop().unwrap();
    let rhs = stack.pop().unwrap();
    stack.push(lhs - rhs)
}
fn mul(stack: &mut Vec<i32>) {
    // pop().expect("error")の方が安全
    let lhs = stack.pop().unwrap();
    let rhs = stack.pop().unwrap();
    stack.push(lhs * rhs)
}
fn div(stack: &mut Vec<i32>) {
    // pop().expect("error")の方が安全
    let lhs = stack.pop().unwrap();
    let rhs = stack.pop().unwrap();
    stack.push(lhs + rhs)
}

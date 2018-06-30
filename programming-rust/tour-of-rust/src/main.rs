use std::io::Write;
use std::str::FromStr;

fn main() {
    // get empty vector/array
    let mut numbers = Vec::new();

    // take args. skip program name which is first arg.
    for arg in std::env::args().skip(1) {
        numbers.push(u64::from_str(&arg)
                     .expect("error parsing argument"));
    }

    if numbers.len() == 0 {
        // unwrap checks that print does not fail. similar to expect above but terse.
        writeln!(std::io::stderr(), "Usage: gcd NUMBER...").unwrap();
        std::process::exit(1); // what's arg for exit mean?
    }

    let mut d = numbers[0];
    for m in &numbers[1..] { // "&" borrows a reference.
        d = gcd(d, *m); // "*" dereferences and returns the value.
    }
    println!("The greatest common divisor of {:?} is {}",
             numbers, d);
}

fn gcd(mut n: u64, mut m: u64) -> u64 {
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            // swap m and n
            let t = m;
            m = n;
            n = t;
        }
        m = m % n; // euclidean algo
    }
    n
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(14,15), 1);
    assert_eq!(gcd(2*3*5*11*17,
                   3*7*11*13*19),
               3*11);
}

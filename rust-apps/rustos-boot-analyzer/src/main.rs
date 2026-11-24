
use std::fs::File;
use std::io::{self, Write};
use std::process::Command;

fn run_command(program: &str, args: &[&str]) -> String {
    match Command::new(program).args(args).output() {
        Ok(output) if output.status.success() => {
            String::from_utf8_lossy(&output.stdout).trim().to_string()
        }
        Ok(output) => {
            format!(
                "Command failed:\n{}",
                String::from_utf8_lossy(&output.stderr).trim()
            )
        }
        Err(error) => format!("Unavailable: {}", error),
    }
}

fn section(title: &str, content: &str) -> String {
    format!(
        "\n========================================\n\
         {}\n\
         ========================================\n{}\n",
        title, content
    )
}

fn generate_report() -> String {
    let mut report = String::new();

    report.push_str("========================================\n");
    report.push_str("          RUSTOS BOOT ANALYZER\n");
    report.push_str("========================================\n");

    report.push_str(&section(
        "SYSTEM INFORMATION",
        &run_command("uname", &["-a"]),
    ));

    report.push_str(&section(
        "TOTAL BOOT TIME",
        &run_command("systemd-analyze", &["time"]),
    ));

    report.push_str(&section(
        "TOP 15 SLOWEST SERVICES",
        &run_command("systemd-analyze", &["blame", "--no-pager"])
            .lines()
            .take(15)
            .collect::<Vec<_>>()
            .join("\n"),
    ));

    report.push_str(&section(
        "FAILED SYSTEMD UNITS",
        &run_command(
            "systemctl",
            &["--failed", "--no-pager", "--plain"],
        ),
    ));

    report.push_str(&section(
        "CRITICAL STARTUP CHAIN",
        &run_command(
            "systemd-analyze",
            &["critical-chain", "--no-pager"],
        )
        .lines()
        .take(30)
        .collect::<Vec<_>>()
        .join("\n"),
    ));

    report.push_str("\n========================================\n");
    report.push_str("           RustOS Debian Edition\n");
    report.push_str("========================================\n");

    report
}

fn main() {
    let report = generate_report();
    println!("{}", report);

    println!("\nSave this report to a text file? (y/n): ");

    let mut input = String::new();

    if io::stdin().read_line(&mut input).is_err() {
        eprintln!("Could not read input.");
        return;
    }

    if input.trim().eq_ignore_ascii_case("y") {
        let filename = "rustos-boot-report.txt";

        match File::create(filename) {
            Ok(mut file) => {
                if let Err(error) = file.write_all(report.as_bytes()) {
                    eprintln!("Failed to save report: {}", error);
                } else {
                    println!("Report saved to {}", filename);
                }
            }
            Err(error) => eprintln!("Failed to create report: {}", error),
        }
    }
}

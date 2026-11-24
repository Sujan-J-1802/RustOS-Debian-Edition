
use std::fs;
use std::process::Command;

fn run_command(program: &str, args: &[&str]) -> String {
    match Command::new(program).args(args).output() {
        Ok(output) if output.status.success() => {
            String::from_utf8_lossy(&output.stdout).trim().to_string()
        }
        Ok(output) => format!(
            "Command failed: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ),
        Err(error) => format!("Unavailable: {}", error),
    }
}

fn main() {
    println!("==========================================");
    println!("          RUSTOS SYSTEM DASHBOARD");
    println!("==========================================");

    println!("\n[OPERATING SYSTEM]");
    let os = fs::read_to_string("/etc/os-release")
        .unwrap_or_else(|_| "OS information unavailable".to_string());

    if let Some(name) = os.lines().find(|line| line.starts_with("PRETTY_NAME=")) {
        println!("{}", name.trim_start_matches("PRETTY_NAME=").trim_matches('"'));
    }

    println!("\n[KERNEL]");
    println!("{}", run_command("uname", &["-r"]));

    println!("\n[CPU]");
    let cpuinfo = fs::read_to_string("/proc/cpuinfo").unwrap_or_default();
    if let Some(cpu) = cpuinfo.lines().find(|line| line.starts_with("model name")) {
        println!("{}", cpu);
    }

    println!("\n[MEMORY]");
    println!("{}", run_command("free", &["-h"]));

    println!("\n[DISK USAGE]");
    println!("{}", run_command("df", &["-h", "/"]));

    println!("\n[UPTIME]");
    println!("{}", run_command("uptime", &["-p"]));

    println!("\n[NETWORK INTERFACES]");
    println!("{}", run_command("ip", &["-br", "addr"]));

    println!("\n[BOOT PERFORMANCE]");
    println!("{}", run_command("systemd-analyze", &["time"]));

    println!("\n==========================================");
    println!("             RustOS Debian Edition");
    println!("==========================================");
}


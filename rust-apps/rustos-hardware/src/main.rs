
use std::fs;
use std::process::Command;

fn run_command(program: &str, args: &[&str]) -> String {
    match Command::new(program).args(args).output() {
        Ok(output) if output.status.success() => {
            String::from_utf8_lossy(&output.stdout).trim().to_string()
        }
        Ok(output) => {
            format!("Command failed: {}", String::from_utf8_lossy(&output.stderr))
        }
        Err(error) => format!("Unavailable: {}", error),
    }
}

fn section(title: &str, content: &str) {
    println!("\n========================================");
    println!(" {}", title);
    println!("========================================");
    println!("{}", content);
}

fn main() {
    println!("========================================");
    println!("       RUSTOS HARDWARE INFORMATION");
    println!("========================================");

    let cpuinfo = fs::read_to_string("/proc/cpuinfo").unwrap_or_default();

    let cpu = cpuinfo
        .lines()
        .find(|line| line.starts_with("model name"))
        .unwrap_or("CPU information unavailable");

    section("CPU INFORMATION", cpu);

    section("MEMORY", &run_command("free", &["-h"]));

    section("PCI DEVICES", &run_command("lspci", &[]));

    section("USB DEVICES", &run_command("lsusb", &[]));

    section("STORAGE DEVICES", &run_command("lsblk", &[
        "-o", "NAME,SIZE,TYPE,MOUNTPOINTS"
    ]));

    section("NETWORK HARDWARE", &run_command("ip", &[
        "-br", "link"
    ]));

    section("KERNEL", &run_command("uname", &["-a"]));

    println!("\n========================================");
    println!("           RustOS Debian Edition");
    println!("========================================");
}

use crate::query::Query;
use log::info;
use serde::{Deserialize, Serialize};
use std::io::Write;
use std::path::PathBuf;
use std::process::{Command, Stdio};

#[derive(Debug, Serialize, Deserialize)]
pub struct Plugin {
    pub id: String,
    pub executable: PathBuf,
}

impl Plugin {
    pub fn query(&self, query: &Query) -> Result<String, std::io::Error> {
        info!("Executing query on plugin '{}'", self.id);

        let mut command = Command::new(&self.executable);

        command
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());

        let mut child = command.spawn()?;

        if let Some(stdin) = child.stdin.as_mut() {
            stdin.write_all(serde_json::to_string(query).unwrap().as_bytes())?;
        }

        let output = child.wait_with_output()?;

        if output.status.success() {
            Ok(String::from_utf8_lossy(&output.stdout).to_string())
        } else {
            let error_msg = String::from_utf8_lossy(&output.stderr);
            Err(std::io::Error::new(
                std::io::ErrorKind::Other,
                format!("Plugin execution failed: {}", error_msg),
            ))
        }
    }
}

use crate::plugin::Plugin;
use confy::ConfyError;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub plugins: Option<Vec<Plugin>>,
}

impl Default for Config {
    fn default() -> Self {
        Self { plugins: None }
    }
}

pub fn load_config(path: Option<PathBuf>) -> Result<Config, ConfyError> {
    let cfg = match path {
        Some(p) => {
            log::info!("Attempting to load config from CLI path: {:?}", &p);
            confy::load_path(p)?
        }
        None => {
            let default_path = confy::get_configuration_file_path("tapyre", Some("config"))?;
            log::info!(
                "Attempting to load config from default path: {:?}",
                default_path
            );
            confy::load("tapyre", Some("config"))?
        }
    };
    Ok(cfg)
}

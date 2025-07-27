use log::{error, info, warn};
use serde::Serialize;

use crate::plugin::Plugin;

#[derive(Debug, Serialize)]
pub struct Query {
    pub plugin_id: String,
    pub mode: String,
    pub text: String,
}

pub fn handle_query(query: &Query, plugins: &Option<Vec<Plugin>>) {
    info!("Handling the query: {query:?}");

    if let Some(plugins_vec) = plugins {
        match plugins_vec.iter().find(|p| p.id == query.plugin_id) {
            Some(plugin) => match plugin.query(query) {
                Ok(result) => {
                    info!("Plugin '{}' executed successfully.", plugin.id);
                    println!("{}", result);
                }
                Err(e) => {
                    error!("Plugin '{}' returned an error: {}", plugin.id, e);
                    std::process::exit(1);
                }
            },
            None => {
                warn!("No plugin found with ID: '{}'", query.plugin_id);
            }
        }
    } else {
        warn!("No plugins are available.");
    }
}

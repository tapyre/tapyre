mod cli;
mod config;
mod plugin;
mod query;

use cli::Command;
use config::Config;
use log::{error, info};
use query::Query;

fn main() {
    env_logger::init();

    let args = cli::parse();

    let cfg: Config = match config::load_config(args.config) {
        Ok(config) => {
            info!("Configuration loaded successfully.");
            config
        }
        Err(e) => {
            error!("Failed to load configuration file: {}", e);
            std::process::exit(1);
        }
    };

    match &args.command {
        Command::Query {
            plugin_id,
            mode,
            text,
        } => {
            let query = Query {
                plugin_id: plugin_id.to_string(),
                mode: mode.to_string(),
                text: text.to_string(),
            };
            query::handle_query(&query, &cfg.plugins);
        }
    }
}

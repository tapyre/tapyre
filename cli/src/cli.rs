use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
pub struct Args {
    #[command(subcommand)]
    pub command: Command,

    /// Sets a custom config file path.
    #[arg(short, long, value_name = "FILE")]
    pub config: Option<PathBuf>,
}

#[derive(Subcommand, Debug)]
pub enum Command {
    /// Query a plugin
    Query {
        /// The id of the plugin to query
        plugin_id: String,
        /// The mode in which to query the plugin
        mode: String,
        /// The query string
        text: String,
    },
}

pub fn parse() -> Args {
    Args::parse()
}

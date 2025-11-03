mod mcp_client;

use eframe::egui;
use mcp_client::{McpClient, Tool};
use std::sync::Arc;
use tracing_subscriber::{fmt, EnvFilter};

struct EddaDesktopApp {
    runtime: tokio::runtime::Runtime,
    client: Option<Arc<McpClient>>,
    tools: Vec<Tool>,
    status: String,
    error_message: Option<String>,
}

impl Default for EddaDesktopApp {
    fn default() -> Self {
        Self {
            runtime: tokio::runtime::Runtime::new().unwrap(),
            client: None,
            tools: Vec::new(),
            status: "Not connected".to_string(),
            error_message: None,
        }
    }
}

impl EddaDesktopApp {
    fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        let mut app = Self::default();
        app.connect_to_mcp();
        app
    }

    fn connect_to_mcp(&mut self) {
        self.status = "Connecting...".to_string();
        self.error_message = None;

        let binary_path = self.get_binary_path();

        match self.runtime.block_on(async {
            let client = McpClient::spawn(&binary_path).await?;
            let tools = client.list_tools().await?;
            Ok::<_, anyhow::Error>((client, tools))
        }) {
            Ok((client, tools)) => {
                self.client = Some(Arc::new(client));
                self.tools = tools;
                self.status = format!("Connected - {} tools available", self.tools.len());
            }
            Err(e) => {
                self.status = "Connection failed".to_string();
                self.error_message = Some(format!("Error: {:#}", e));
            }
        }
    }

    fn get_binary_path(&self) -> String {
        // in development, use the workspace-built binary
        let workspace_binary = std::env::current_dir()
            .unwrap()
            .join("target/release/edda_mcp");

        if workspace_binary.exists() {
            return workspace_binary.to_string_lossy().to_string();
        }

        // fallback to bundled binary (for production builds)
        "edda_mcp".to_string()
    }
}

impl eframe::App for EddaDesktopApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("Edda MCP Desktop");

            ui.separator();

            // status bar
            ui.horizontal(|ui| {
                ui.label("Status:");
                ui.label(&self.status);

                if ui.button("Reconnect").clicked() {
                    self.connect_to_mcp();
                }
            });

            ui.separator();

            if let Some(error) = &self.error_message {
                ui.colored_label(egui::Color32::RED, error);
                ui.separator();
            }

            // tools list
            if self.tools.is_empty() {
                ui.label("No tools available");
            } else {
                ui.heading(format!("Available Tools ({})", self.tools.len()));

                egui::ScrollArea::vertical().show(ui, |ui| {
                    for tool in &self.tools {
                        ui.group(|ui| {
                            ui.label(egui::RichText::new(&tool.name).strong().size(16.0));

                            if let Some(desc) = &tool.description {
                                ui.label(desc);
                            }

                            ui.collapsing("Input Schema", |ui| {
                                let schema_str = serde_json::to_string_pretty(&tool.input_schema)
                                    .unwrap_or_else(|_| "Invalid schema".to_string());
                                ui.code(&schema_str);
                            });
                        });

                        ui.add_space(8.0);
                    }
                });
            }
        });
    }

    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        // client will be dropped and cleaned up automatically
        self.client = None;
    }
}

fn main() -> eframe::Result<()> {
    // initialize logging
    fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("edda_desktop=info"))
        )
        .init();

    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([800.0, 600.0])
            .with_title("Edda MCP Desktop"),
        ..Default::default()
    };

    eframe::run_native(
        "Edda MCP Desktop",
        options,
        Box::new(|cc| Ok(Box::new(EddaDesktopApp::new(cc)))),
    )
}

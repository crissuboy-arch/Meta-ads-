// Casca desktop fina: o app roda hospedado (Vercel), esta janela so exibe a
// URL de producao configurada em tauri.conf.json. Nao ha comandos Tauri
// customizados - sem ponte JS<->Rust, sem precisar de allowlist de IPC remota.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o Ofensiva Tráfego IA (desktop)");
}

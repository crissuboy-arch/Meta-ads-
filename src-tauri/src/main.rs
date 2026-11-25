// Casca desktop (Tauri): o app roda hospedado (app.ofensivacriativa.com /
// meta-ads-unmc.vercel.app, mesmo backend), esta janela exibe a URL de
// producao. Fase III/IV (Modo Local) adiciona comandos para o motor local
// independente (local_engine/, processo Python filho em 127.0.0.1 - nunca
// exposto publicamente) e para detectar/abrir as CLIs oficiais de IA
// (claude/codex/opencode) ja instaladas e autenticadas pelo PROPRIO
// usuario. Nenhum login/senha/token e lido, guardado ou proxied por este
// shell - ver docs/motor-local.md para o que foi validado por teste real
// e o que ainda depende de confirmacao manual (este ambiente de
// desenvolvimento nao tem cargo/rustc; a build real roda no CI).
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::collections::HashMap;
use std::io::{BufRead, BufReader};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;

use tauri::{Manager, State};

struct LocalEngineState(Mutex<Option<(Child, u16)>>);

const CLI_PROVIDERS: [&str; 3] = ["claude", "codex", "opencode"];

fn find_on_path(bin: &str) -> bool {
    let path = match std::env::var_os("PATH") {
        Some(p) => p,
        None => return false,
    };
    let suffixes: &[&str] = if cfg!(target_os = "windows") {
        &["", ".exe", ".cmd", ".bat"]
    } else {
        &[""]
    };
    for dir in std::env::split_paths(&path) {
        for suf in suffixes {
            if dir.join(format!("{bin}{suf}")).is_file() {
                return true;
            }
        }
    }
    false
}

#[tauri::command]
fn detect_providers() -> HashMap<String, bool> {
    CLI_PROVIDERS
        .iter()
        .map(|p| ((*p).to_string(), find_on_path(p)))
        .collect()
}

#[tauri::command]
fn open_provider_terminal(provider: String) -> Result<(), String> {
    if !CLI_PROVIDERS.contains(&provider.as_str()) {
        return Err(format!("provedor desconhecido: {provider}"));
    }
    if !find_on_path(&provider) {
        return Err(format!(
            "{provider} nao esta instalado/no PATH. Instale o CLI oficial primeiro."
        ));
    }
    let spawn_result = if cfg!(target_os = "windows") {
        Command::new("cmd").args(["/c", "start", "cmd", "/k", &provider]).spawn()
    } else if cfg!(target_os = "macos") {
        let script = format!("tell application \"Terminal\" to do script \"{provider}\"");
        Command::new("osascript").args(["-e", &script]).spawn()
    } else {
        Command::new("x-terminal-emulator").args(["-e", &provider]).spawn()
    };
    spawn_result
        .map(|_| ())
        .map_err(|e| format!("falha ao abrir terminal: {e}"))
}

fn python_bin() -> &'static str {
    if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    }
}

#[tauri::command]
fn start_local_engine(
    app: tauri::AppHandle,
    state: State<LocalEngineState>,
) -> Result<u16, String> {
    let mut guard = state.0.lock().map_err(|e| e.to_string())?;
    if let Some((_, port)) = &*guard {
        return Ok(*port);
    }
    // Em producao, local_engine/ chega copiado para resource_dir() (ver
    // bundle.resources em tauri.conf.json). Em desenvolvimento, cai no
    // repo local, um nivel acima de src-tauri/.
    let resource_dir = app
        .path()
        .resource_dir()
        .map_err(|e| format!("resource_dir indisponivel: {e}"))?;
    let base_dir = if resource_dir.join("local_engine").join("server.py").is_file() {
        resource_dir
    } else {
        std::env::current_dir()
            .map_err(|e| e.to_string())?
            .parent()
            .ok_or_else(|| "sem diretorio pai do repositorio".to_string())?
            .to_path_buf()
    };

    let mut child = Command::new(python_bin())
        .args(["-m", "local_engine.server"])
        .current_dir(&base_dir)
        .env("LOCAL_ENGINE_PORT", "0")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("falha ao iniciar o motor local (Python instalado?): {e}"))?;

    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "sem stdout do motor local".to_string())?;
    let mut line = String::new();
    BufReader::new(stdout)
        .read_line(&mut line)
        .map_err(|e| format!("falha ao ler a porta do motor local: {e}"))?;
    let port: u16 = line
        .trim()
        .strip_prefix("LOCAL_ENGINE_PORT=")
        .and_then(|p| p.parse().ok())
        .ok_or_else(|| format!("resposta inesperada do motor local: {line:?}"))?;

    *guard = Some((child, port));
    Ok(port)
}

#[tauri::command]
fn stop_local_engine(state: State<LocalEngineState>) -> Result<(), String> {
    let mut guard = state.0.lock().map_err(|e| e.to_string())?;
    if let Some((mut child, _)) = guard.take() {
        let _ = child.kill();
    }
    Ok(())
}

#[tauri::command]
fn local_engine_port(state: State<LocalEngineState>) -> Option<u16> {
    state.0.lock().ok().and_then(|g| g.as_ref().map(|(_, p)| *p))
}

fn main() {
    tauri::Builder::default()
        .manage(LocalEngineState(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![
            detect_providers,
            open_provider_terminal,
            start_local_engine,
            stop_local_engine,
            local_engine_port
        ])
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o Ofensiva Tráfego IA (desktop)");
}

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use std::collections::HashMap;
use std::io::{BufRead, BufReader};
use std::process::{Child, Command, Stdio};
use std::sync::{mpsc, Mutex};
use std::time::Duration;
use tauri::{Manager, State};

struct Engine { child: Child, port: u16, token: String }
struct LocalEngineState(Mutex<Option<Engine>>);
const PROVIDERS: [&str; 3] = ["claude", "codex", "opencode"];

fn find_on_path(bin: &str) -> bool {
    std::env::var_os("PATH").map(|path| std::env::split_paths(&path).any(|dir| {
        let suffixes: &[&str] = if cfg!(windows) { &["", ".exe", ".cmd", ".bat"] } else { &[""] };
        suffixes.iter().any(|s| dir.join(format!("{bin}{s}")).is_file())
    })).unwrap_or(false)
}

#[tauri::command]
fn detect_providers() -> HashMap<String, bool> {
    PROVIDERS.iter().map(|p| (p.to_string(), find_on_path(p))).collect()
}

#[tauri::command]
fn open_provider_terminal(provider: String) -> Result<(), String> {
    if !PROVIDERS.contains(&provider.as_str()) || !find_on_path(&provider) {
        return Err("CLI oficial nao instalada/no PATH".into());
    }
    let result = if cfg!(windows) {
        Command::new("cmd").args(["/c", "start", "cmd", "/k", &provider]).spawn()
    } else if cfg!(target_os="macos") {
        Command::new("osascript").args(["-e", &format!("tell application \"Terminal\" to do script \"{provider}\"")]).spawn()
    } else {
        Command::new("x-terminal-emulator").args(["-e", &provider]).spawn()
    };
    result.map(|_| ()).map_err(|e| e.to_string())
}

fn start_engine(app: &tauri::AppHandle, state: &LocalEngineState) -> Result<u16, String> {
    let mut guard = state.0.lock().map_err(|e| e.to_string())?;
    if let Some(engine) = guard.as_mut() {
        if matches!(engine.child.try_wait(), Ok(None)) { return Ok(engine.port); }
        *guard = None;
    }
    let resources = app.path().resource_dir().map_err(|e| e.to_string())?;
    let binary = resources.join("runtime").join("local-engine").join(if cfg!(windows) {"local-engine.exe"} else {"local-engine"});
    let mut command = if binary.is_file() {
        Command::new(binary)
    } else if cfg!(debug_assertions) {
        let mut cmd = Command::new(if cfg!(windows) {"python"} else {"python3"});
        cmd.args(["-m", "local_engine.server"]).current_dir(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap());
        cmd
    } else { return Err("Motor local ausente. Reinstale usando o instalador completo.".into()); };
    #[cfg(windows)] {
        use std::os::windows::process::CommandExt;
        command.creation_flags(0x08000000);
    }
    let mut child = command.env("LOCAL_ENGINE_PORT", "0").stdout(Stdio::piped()).stderr(Stdio::inherit())
        .spawn().map_err(|e| format!("Nao foi possivel iniciar o motor: {e}"))?;
    let stdout = child.stdout.take().ok_or("stdout indisponivel")?;
    let (sender, receiver) = mpsc::channel();
    std::thread::spawn(move || {
        let mut line = String::new();
        let result = BufReader::new(stdout).read_line(&mut line).map(|_| line);
        let _ = sender.send(result);
    });
    let ready = match receiver.recv_timeout(Duration::from_secs(20)) {
        Ok(Ok(line)) => line.strip_prefix("LOCAL_ENGINE_READY=").and_then(|s| serde_json::from_str::<serde_json::Value>(s).ok()),
        _ => None
    };
    let parsed = ready.and_then(|v| Some((u16::try_from(v.get("port")?.as_u64()?).ok()?, v.get("token")?.as_str()?.to_owned())));
    if let Some((port, token)) = parsed {
        if port > 0 && token.len() >= 32 {
            *guard = Some(Engine { child, port, token });
            return Ok(port);
        }
    }
    let _ = child.kill(); let _ = child.wait();
    Err("O motor local nao iniciou no prazo esperado".into())
}

#[tauri::command]
async fn start_local_engine(app: tauri::AppHandle) -> Result<u16, String> {
    tauri::async_runtime::spawn_blocking(move || start_engine(&app, &app.state::<LocalEngineState>()))
        .await.map_err(|e| e.to_string())?
}

fn stop_engine(state: &LocalEngineState) -> Result<(), String> {
    if let Some(mut engine) = state.0.lock().map_err(|e| e.to_string())?.take() {
        let _ = engine.child.kill(); let _ = engine.child.wait();
    }
    Ok(())
}

#[tauri::command]
fn stop_local_engine(state: State<LocalEngineState>) -> Result<(), String> { stop_engine(&state) }

#[tauri::command]
fn local_engine_port(state: State<LocalEngineState>) -> Option<u16> {
    state.0.lock().ok().and_then(|g| g.as_ref().map(|e| e.port))
}

#[tauri::command]
async fn local_chat(app: tauri::AppHandle, payload: serde_json::Value) -> Result<serde_json::Value, String> {
    tauri::async_runtime::spawn_blocking(move || {
        let state = app.state::<LocalEngineState>();
        let port = start_engine(&app, &state)?;
        let token = state.0.lock().map_err(|e| e.to_string())?.as_ref().ok_or("Motor indisponivel")?.token.clone();
        let client = reqwest::blocking::Client::builder().no_proxy().timeout(Duration::from_secs(75)).build().map_err(|e| e.to_string())?;
        let response = client.post(format!("http://127.0.0.1:{port}/chat")).bearer_auth(token).json(&payload).send().map_err(|e| e.to_string())?;
        response.json::<serde_json::Value>().map_err(|e| e.to_string())
    }).await.map_err(|e| e.to_string())?
}

fn main() {
    let app = tauri::Builder::default().manage(LocalEngineState(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![detect_providers, open_provider_terminal, start_local_engine, stop_local_engine, local_engine_port, local_chat])
        .build(tauri::generate_context!()).expect("Erro ao iniciar Ofensiva");
    app.run(|handle, event| { if let tauri::RunEvent::Exit = event { let _ = stop_engine(&handle.state::<LocalEngineState>()); } });
}

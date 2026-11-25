# App instalável (Fase G)

O app web já roda hospedado (Vercel). Esta fase dá duas formas de "instalar"
sem depender de terminal no dia a dia.

## 1. PWA (já funciona agora, sem precisar mesclar nada no desktop)

Abra o app no navegador (Chrome, Edge ou Safari) e:

- **Windows/Mac/Linux (Chrome/Edge):** clique no ícone de instalar na barra
  de endereço (ou menu → "Instalar Ofensiva Tráfego IA"). Cria um atalho na
  área de trabalho/menu iniciar, abre numa janela própria, sem abas do
  navegador.
- **Android (Chrome):** menu → "Adicionar à tela inicial".
- **iPhone/iPad (Safari):** botão de compartilhar → "Adicionar à Tela de Início".

Funciona offline para a tela principal (o resto depende de internet, já que
os dados são reais e vêm do servidor).

## 2. Instalador desktop (Windows/macOS)

Gerado automaticamente pelo GitHub Actions
(`.github/workflows/desktop-release.yml`) a cada tag `v*` criada no
repositório, ou manualmente em **Actions → Build desktop installers (Tauri)
→ Run workflow**.

1. Vá em **Releases** no GitHub do repositório.
2. Baixe:
   - Windows: o arquivo `.msi` ou o instalador `.exe` (NSIS).
   - macOS: o arquivo `.dmg`.
3. **Os builds não são assinados** (não há certificado de desenvolvedor
   Apple/Microsoft configurado - custam dinheiro e exigem conta própria).
   Isso é normal para uso pessoal, mas o sistema vai avisar na primeira vez:
   - **Windows:** SmartScreen mostra "Editor desconhecido". Clique em
     "Mais informações" → "Executar assim mesmo".
   - **macOS:** Gatekeeper bloqueia na primeira abertura. Vá em
     **Preferências do Sistema → Privacidade e Segurança** e clique em
     "Abrir assim mesmo" (ou clique com o botão direito no app → Abrir).
4. Depois de aberto, o app é só uma janela que mostra o site de produção
   (`https://meta-ads-unmc.vercel.app`, configurável em
   `src-tauri/tauri.conf.json`) - conecte suas contas (Meta, provedores de
   IA) normalmente, como no navegador.

### Por que Tauri e não Electron

O backend já roda hospedado; o instalador não precisa empacotar Python/
FastAPI, só um navegador embutido (webview nativo do sistema) apontando
para a URL de produção. Isso elimina o maior risco técnico (rodar um
servidor Python dentro de um app desktop) e deixa o instalador bem menor
que um equivalente em Electron.

### Gerando os instaladores você mesmo (opcional)

Requer Rust instalado (`rustup.rs`) e a CLI do Tauri:

```bash
cargo install tauri-cli --version "^2.0.0" --locked
cargo tauri icon src-tauri/icons/icon-source.png -o src-tauri/icons
cargo tauri build
```

Os instaladores saem em `src-tauri/target/release/bundle/`.

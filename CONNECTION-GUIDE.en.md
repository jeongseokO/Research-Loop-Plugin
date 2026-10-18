# Connecting your AI

If this is your first connection, use the **Codex or Claude Code plugin**. In ChatGPT and the Claude apps, a single connector opens the Research Loop panel inside the conversation. Follow only the steps for the tool you use.

| How you connect | What you get | API key |
| --- | --- | --- |
| Plugin | MCP connection + task guidance + figure-making tools | Not needed · you sign in to Research Loop |
| MCP only | Tools to read and edit research, with the server's guidance | Not needed when the tool supports OAuth |
| API key | A compatible connection for tools without OAuth | Needed |

If you installed the plugin, don't add the same MCP server separately. One AI connection can reach every project it has been allowed into.

## 1. Before you start

1. Sign in to [Research Loop](https://airesearchloop.com/) with **your own account**.
2. Create the project you will work in, or accept the invitation you received.
3. Sign in to the Codex or Claude Code you will use. Your AI subscription and your Research Loop account are connected separately.

Don't share accounts or API keys with colleagues. When each person connects their own, the record shows who worked with which AI. You never need to touch Supabase or Google Cloud admin settings.

## 2. Codex · VS Code plugin

### Install from the interface

1. In the Codex extension for VS Code, open **Plugins → Add plugin marketplace**. Menu names may differ between versions.
2. Fill in the three fields below.

| Field | Value |
| --- | --- |
| Source | `https://github.com/jeongseokO/Research-Loop-Plugin.git` |
| Git ref | `codex/public-release` |
| Sparse path | **Leave empty** |

3. In the marketplace you added, choose **Research Loop** (the green loop icon) and install it.
4. When the account window opens, sign in to Research Loop, check the AI's name and permissions, and approve.
5. Reopen Codex and, in a **new conversation**, ask: "Check my account connected to Research Loop and the projects I can reach."

**Check the connection:** if your name and the projects you expect appear, you're set. If a team project is missing, see "Project access" below.

### Install from a terminal

Instead of the interface, run these in a terminal where a Codex CLI with plugin support is installed. You don't need both.

```sh
codex plugin marketplace add jeongseokO/Research-Loop-Plugin --ref codex/public-release
codex plugin add research-loop@research-loop
```

If no sign-in window opens, connect with the command below. The plugin's server is named `research-loop-plugin`.

```sh
codex mcp login research-loop-plugin --scopes email --oauth-client-registration dcr
```

**On a remote server (SSH, VS Code Remote):** install and sign in on the server where Codex runs. The server has no browser, so sign in with `--no-browser`.

```sh
codex mcp login research-loop-plugin --no-browser --scopes email --oauth-client-registration dcr
```

Open the printed address in your own computer's browser and approve. The browser then fails to load an address that starts with `127.0.0.1`: copy that whole address and paste it into the server's terminal to finish signing in. No port forwarding is needed.

For the install format and commands, see the [OpenAI plugin docs](https://developers.openai.com/plugins/build/plugins); for remote connections and OAuth, the [Codex MCP docs](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

## 3. Claude Code plugin

1. In the terminal where you use Claude Code, run these commands in order.

```sh
claude plugin marketplace add jeongseokO/Research-Loop-Plugin
claude plugin install research-loop@research-loop
```

2. Restart Claude Code.
3. Type `/mcp` in the conversation input and choose the sign-in item for the Research Loop connection.
4. In the browser, sign in with **your own Research Loop account** and approve the connection.
5. In a new conversation, type `/research-loop:brief`, or ask: "Check my Research Loop account and the projects I can reach."

Use the `claude ...` commands in an ordinary terminal and `/mcp` in the Claude Code conversation input. Connectors in Claude on the web and desktop install differently from Claude Code plugins. [Claude Code plugin guide](https://code.claude.com/docs/en/discover-plugins)

## 4. MCP only, without the plugin

If you already connected with the plugin, skip this step. With MCP alone you can read and edit research pages, but the plugin's local figure-making scripts are not installed.

**Server address · Streamable HTTP**

```text
https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
```

### Codex

1. Add the server in a terminal where the Codex CLI is installed.

```sh
codex mcp add research-loop --url https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
codex mcp login research-loop --scopes email --oauth-client-registration dcr
```

2. Approve the Research Loop account connection in the browser.
3. In a new conversation, check your account and projects. The direct connection's server is named `research-loop`, distinct from the plugin's `research-loop-plugin`.

### Claude Code

1. Run this in a terminal.

```sh
claude mcp add --transport http --scope user research-loop https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
```

2. In Claude Code's `/mcp`, choose Research Loop and sign in.
3. Check that your own account and projects appear. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp)

### Claude on the web, desktop and iOS

The Research Loop panel opens inside the Claude app. It is the same panel as the Research Loop app in ChatGPT: you can view and edit record lists and pages, table charts, diagrams and equations, to-dos and schedules, saved presentations and AI collaboration without leaving it.

1. In Claude, open **Settings → Connectors** and choose **Add custom connector**. Whether the menu is offered depends on your plan and your organization's policy.
2. Enter **Research Loop** as the name and the remote MCP server address above exactly as it is. Don't enter the app's address or the GitHub repository address.
3. Press **Connect**, sign in with your Research Loop account and approve.
4. In a new conversation, ask "Open the Research Loop panel" or "Show the latest records in my project." If Claude asks to allow the panel, choose **Allow**.

By Claude's security policy, the panel does not embed the website. Attachments, the calendar and team settings are handled on the website through the panel's **Open site ↗**. The same connector opens the panel in Claude desktop and on iOS.

### Other MCP tools

1. Add a new remote connection in the tool's connector or MCP settings. Whether that menu is offered depends on your plan and your organization's policy.
2. Enter **Research Loop** as the name and the address above as the server. If you are asked for a transport, choose **Streamable HTTP**.
3. Press connect or sign in, and sign in with your Research Loop account. Don't put the app's address or the GitHub repository address in the MCP server field.
4. Check your account and the projects you can reach. Only tools without OAuth use the API key steps below. In tools that support MCP Apps, the Research Loop panel opens too.

## 5. Project access

1. Open **My AI** in the Research Loop web app.
2. Find the AI you just connected and check its access to each project.
3. **Projects where you are the Owner or a Semi-Owner:** your AI can work there without asking.
4. **Projects you were invited to as an Editor or Viewer:** press **Request access** on that AI. It can work there once the project's Owner approves. Accepting a person's invitation does not approve their AI.
5. After approval, ask the AI to check its project list again. You don't need a new key.

What the AI can actually do is bounded by **your permissions × your project role × the AI access that was approved**. An edit sent as a review request isn't applied until someone who can review it, such as the Owner, approves it.

## 6. Only when you need an API key

If you connected with OAuth, skip this step. The key here is not an OpenAI or Anthropic API key: it is **a key for reaching Research Loop**.

1. In the web app, open **My AI → API key · compatible connection**.
2. Choose the AI's name, the client, the permissions it needs and an expiry, then issue the key.
3. The key is shown only once: keep it in your own secure secret store. Don't paste it into chats, notes or Git repositories.
4. On the same screen, press **Copy settings** for the tool you use. The default environment variable is `RESEARCH_LOOP_API_KEY`.
5. Put the copied settings in that tool's MCP configuration, and provide the key through that environment variable **where the AI runs**. Don't write the key into a settings file in plain text. VS Code may not pick up environment variables set in another terminal.
6. Restart the tool, check the connection, then request access to the projects you need.

If a key was exposed, or you no longer use an AI, remove it with **My AI → Delete AI** and recreate only the connections you need. Once deleted, that AI connection stops working.

## 7. Updates and staying signed in

You don't fetch new versions yourself.

- **Codex** checks the marketplace when it starts and moves the plugin to the new version. A Codex that was already open uses it once you reopen it (in VS Code, reload the window). If it doesn't change, update Codex itself.
- **Claude Code** needs auto-update turned on once: in a conversation, `/plugin` → Marketplaces → research-loop → Enable auto-update.

Don't uninstall and reinstall the plugin to update it: a reinstall means signing in again. A plugin installed from a local folder (`research-loop@personal`) doesn't update by itself, so move it once to the marketplace install above.

When you sign in again, pick the AI you were using under **Connect as** on the approval screen. Its name, permissions and project approvals carry over. Choosing **New AI** adds one more connection to **My AI**.

Signing out of the website keeps your AI connections. Changing your password or deleting a connection under **My AI** ends them; then sign in again in that environment.

## 8. When it doesn't connect

| Symptom | Check first |
| --- | --- |
| The plugin isn't in the marketplace | Repository address and Git ref → leave Sparse empty → refresh the marketplace |
| No plugin menu or command | Whether your Codex or Claude Code version supports plugins, and your organization's policy. If not supported, connect MCP only |
| No projects after signing in | The account you signed in with → the person's project invitation accepted → that AI's project access approved, in that order |
| An edit didn't take effect | Whether the AI sent a review request rather than "applied" → check the request in Notifications |
| `instructions_required` | Have the AI read the current project's working guidelines again, then retry only what is still needed |
| Service account connection settings missing | A problem with how the service is run. Don't ask users for Supabase settings or repeated keys: contact the administrator |
| Asked to sign in again | Whether you changed your password or deleted the connection under My AI → sign in again in that environment (`--no-browser` on a remote server) and pick the AI you were using on the approval screen |
| The same AI appears several times in My AI | Those connections were approved as **New AI** when signing in again. Delete the ones you don't use under My AI, and pick the AI you were using next time |
| Old guidance or icon keeps showing | Reopen Codex or Claude Code and start a new conversation. An existing conversation may keep its old guidance. In Claude Code, check that auto-update is on |

When you contact us, say which tool and version you used, the step that failed and the error message. Don't send API keys, OAuth tokens, passwords or unpublished research. [Contact support](mailto:jeongseok0112@gmail.com)

# Marco Core

The local-first assistant engine used by Marco clients. It deliberately has no
framework or model SDK dependency: a desktop app supplies a chat model, optional
memory store, and tool executor through small adapter interfaces.

The product source of truth lives in the sibling `marco-docs` repository.

## MVP scope

- Preserve a bounded, ordered conversation history.
- Retrieve relevant local memories before a model request.
- Let the model request a tool, execute it, then continue the response.
- Stream simple lifecycle events for a desktop UI.
- Run with a local Ollama-compatible model endpoint by default.

Out of scope for this package: window management, credentials, permissions UI,
durable storage, and cloud synchronization. Those responsibilities belong to
the desktop, memory, and cloud repositories respectively.

## Quick start

```js
import { AssistantSession, createOllamaChatModel } from "@marco-ai/core";

const session = new AssistantSession({
  model: createOllamaChatModel({ model: "llama3.2" }),
  systemPrompt: "You are Marco, a focused local desktop assistant."
});

const reply = await session.send("Summarize my open tasks.");
console.log(reply.content);
```

The Ollama adapter expects a running server at `http://127.0.0.1:11434`.
Pass a custom `baseUrl` when needed.

## Contracts

`model.complete({ messages, memories })` returns a response with `content` and
an optional `toolCall` of `{ name, arguments }`.

`memory.search(query, { limit })` returns relevant strings or objects with a
`content` field. `tools.execute(name, arguments)` executes an approved tool and
returns JSON-serializable output.

## Development

```sh
npm test
```

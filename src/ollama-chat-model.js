/**
 * Creates a minimal adapter for Ollama's local /api/chat endpoint.
 */
export function createOllamaChatModel({ baseUrl = "http://127.0.0.1:11434", model, tools = [], fetchImpl = fetch } = {}) {
  if (typeof model !== "string" || !model.trim()) {
    throw new TypeError("createOllamaChatModel requires a model name.");
  }
  if (typeof fetchImpl !== "function") {
    throw new TypeError("fetchImpl must be a function.");
  }

  const endpoint = `${baseUrl.replace(/\/$/, "")}/api/chat`;

  return {
    async complete({ messages, memories = [] }) {
      const context = memories.length
        ? `Relevant local memory:\n${memories.map((memory) => `- ${memory}`).join("\n")}`
        : null;
      const requestMessages = context
        ? [...messages, { role: "system", content: context }]
        : messages;

      const response = await fetchImpl(endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ model, messages: requestMessages, tools, stream: false })
      });
      if (!response.ok) {
        throw new Error(`Ollama request failed (${response.status} ${response.statusText}).`);
      }

      const payload = await response.json();
      const content = payload?.message?.content;
      if (typeof content !== "string") {
        throw new Error("Ollama returned no assistant message.");
      }
      const call = payload?.message?.tool_calls?.[0]?.function;
      return {
        content,
        toolCall: call ? { name: call.name, arguments: call.arguments ?? {} } : undefined
      };
    }
  };
}

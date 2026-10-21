const DEFAULT_MEMORY_LIMIT = 5;
const DEFAULT_HISTORY_LIMIT = 24;
const MAX_TOOL_ROUNDS = 3;

/**
 * Model-agnostic conversation orchestrator for Marco clients.
 */
export class AssistantSession {
  #model;
  #memory;
  #tools;
  #systemPrompt;
  #historyLimit;
  #memoryLimit;
  #messages = [];
  #listeners = new Set();

  constructor({ model, memory, tools, systemPrompt = "You are Marco, a helpful local assistant.", historyLimit = DEFAULT_HISTORY_LIMIT, memoryLimit = DEFAULT_MEMORY_LIMIT } = {}) {
    if (!model || typeof model.complete !== "function") {
      throw new TypeError("AssistantSession requires a model with a complete method.");
    }
    if (memory && typeof memory.search !== "function") {
      throw new TypeError("memory must expose a search method.");
    }
    if (tools && typeof tools.execute !== "function") {
      throw new TypeError("tools must expose an execute method.");
    }

    this.#model = model;
    this.#memory = memory;
    this.#tools = tools;
    this.#systemPrompt = systemPrompt;
    this.#historyLimit = positiveInteger(historyLimit, "historyLimit");
    this.#memoryLimit = positiveInteger(memoryLimit, "memoryLimit");
  }

  get messages() {
    return this.#messages.map((message) => ({ ...message }));
  }

  clear() {
    this.#messages = [];
    this.#emit({ type: "conversation.cleared" });
  }

  subscribe(listener) {
    if (typeof listener !== "function") {
      throw new TypeError("listener must be a function.");
    }
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  async send(content) {
    if (typeof content !== "string" || !content.trim()) {
      throw new TypeError("content must be a non-empty string.");
    }

    const userMessage = makeMessage("user", content.trim());
    this.#append(userMessage);
    this.#emit({ type: "message.created", message: userMessage });

    const memories = await this.#retrieveMemories(userMessage.content);
    let response;

    for (let round = 0; round <= MAX_TOOL_ROUNDS; round += 1) {
      response = await this.#model.complete({
        messages: this.#requestMessages(),
        memories
      });
      validateModelResponse(response);

      if (!response.toolCall) break;
      if (!this.#tools) {
        throw new Error(`Model requested tool '${response.toolCall.name}', but no tool executor is configured.`);
      }
      if (round === MAX_TOOL_ROUNDS) {
        throw new Error("Model exceeded the maximum number of tool rounds.");
      }

      this.#emit({ type: "tool.requested", toolCall: response.toolCall });
      const result = await this.#tools.execute(response.toolCall.name, response.toolCall.arguments ?? {});
      const toolMessage = makeMessage("tool", JSON.stringify(result), { name: response.toolCall.name });
      this.#append(toolMessage);
      this.#emit({ type: "tool.completed", toolCall: response.toolCall, result });
    }

    const assistantMessage = makeMessage("assistant", response.content);
    this.#append(assistantMessage);
    this.#emit({ type: "message.created", message: assistantMessage });
    return assistantMessage;
  }

  async #retrieveMemories(query) {
    if (!this.#memory) return [];
    const matches = await this.#memory.search(query, { limit: this.#memoryLimit });
    if (!Array.isArray(matches)) {
      throw new TypeError("memory.search must return an array.");
    }
    const memories = matches.map(normalizeMemory).filter(Boolean);
    this.#emit({ type: "memory.retrieved", query, count: memories.length });
    return memories;
  }

  #requestMessages() {
    return [
      makeMessage("system", this.#systemPrompt),
      ...this.#messages
    ];
  }

  #append(message) {
    this.#messages.push(message);
    if (this.#messages.length > this.#historyLimit) {
      this.#messages.splice(0, this.#messages.length - this.#historyLimit);
    }
  }

  #emit(event) {
    for (const listener of this.#listeners) {
      try {
        listener(event);
      } catch {
        // UI listeners must not be able to interrupt an assistant turn.
      }
    }
  }
}

function makeMessage(role, content, extra = {}) {
  return { id: crypto.randomUUID(), role, content, createdAt: new Date().toISOString(), ...extra };
}

function normalizeMemory(memory) {
  if (typeof memory === "string") return memory;
  if (memory && typeof memory.content === "string") return memory.content;
  return null;
}

function positiveInteger(value, name) {
  if (!Number.isInteger(value) || value < 1) {
    throw new TypeError(`${name} must be a positive integer.`);
  }
  return value;
}

function validateModelResponse(response) {
  if (!response || typeof response.content !== "string") {
    throw new TypeError("model.complete must return an object with string content.");
  }
  if (response.toolCall && typeof response.toolCall.name !== "string") {
    throw new TypeError("toolCall must include a tool name.");
  }
}

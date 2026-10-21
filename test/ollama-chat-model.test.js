import assert from "node:assert/strict";
import test from "node:test";
import { createOllamaChatModel } from "../src/index.js";

test("sends messages and memories to the Ollama chat endpoint", async () => {
  let url;
  let options;
  const model = createOllamaChatModel({
    model: "llama3.2",
    tools: [{ type: "function", function: { name: "task.capture" } }],
    baseUrl: "http://localhost:11434/",
    fetchImpl: async (receivedUrl, receivedOptions) => {
      url = receivedUrl;
      options = receivedOptions;
      return { ok: true, json: async () => ({ message: { content: "Hello" } }) };
    }
  });

  const response = await model.complete({
    messages: [{ role: "user", content: "Hi" }],
    memories: ["The user is in India."]
  });

  assert.equal(response.content, "Hello");
  assert.equal(url, "http://localhost:11434/api/chat");
  const body = JSON.parse(options.body);
  assert.equal(body.model, "llama3.2");
  assert.equal(body.tools[0].function.name, "task.capture");
  assert.equal(body.messages.at(-1).role, "system");
  assert.match(body.messages.at(-1).content, /Relevant local memory/);
});

test("normalizes an Ollama tool call", async () => {
  const model = createOllamaChatModel({
    model: "llama3.2",
    fetchImpl: async () => ({
      ok: true,
      json: async () => ({ message: { content: "", tool_calls: [{ function: { name: "task.capture", arguments: { content: "Buy milk" } } }] } })
    })
  });

  const response = await model.complete({ messages: [] });
  assert.deepEqual(response.toolCall, { name: "task.capture", arguments: { content: "Buy milk" } });
});

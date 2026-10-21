import assert from "node:assert/strict";
import test from "node:test";
import { AssistantSession } from "../src/index.js";

test("includes local memories and returns the assistant response", async () => {
  let request;
  const session = new AssistantSession({
    model: { complete: async (value) => { request = value; return { content: "Here is your plan." }; } },
    memory: { search: async () => [{ content: "Prince prefers a concise daily plan." }] },
    systemPrompt: "You are Marco."
  });

  const reply = await session.send("What should I do today?");

  assert.equal(reply.role, "assistant");
  assert.equal(reply.content, "Here is your plan.");
  assert.deepEqual(request.memories, ["Prince prefers a concise daily plan."]);
  assert.deepEqual(request.messages.map((message) => message.role), ["system", "user"]);
});

test("executes a requested tool and gives its result back to the model", async () => {
  const calls = [];
  const session = new AssistantSession({
    model: {
      complete: async ({ messages }) => {
        calls.push(messages);
        return calls.length === 1
          ? { content: "", toolCall: { name: "tasks.list", arguments: { status: "open" } } }
          : { content: "You have two open tasks." };
      }
    },
    tools: { execute: async (name, args) => ({ name, args, count: 2 }) }
  });

  const reply = await session.send("What is open?");

  assert.equal(reply.content, "You have two open tasks.");
  assert.equal(calls.length, 2);
  assert.equal(calls[1].at(-1).role, "tool");
  assert.match(calls[1].at(-1).content, /\"count\":2/);
});

test("caps retained history without losing the newest messages", async () => {
  const session = new AssistantSession({
    model: { complete: async () => ({ content: "ok" }) },
    historyLimit: 3
  });

  await session.send("one");
  await session.send("two");

  assert.equal(session.messages.length, 3);
  assert.deepEqual(session.messages.map((message) => message.content), ["ok", "two", "ok"]);
});

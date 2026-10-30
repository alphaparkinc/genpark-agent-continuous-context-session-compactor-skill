import sys
import json

class ContextCompactor:
    @staticmethod
    def compact(messages, budget=4000):
        total_tokens = sum(max(1, len(m.get("content", "").split())) for m in messages)
        if total_tokens <= budget:
            return {"compacted": False, "messages": messages, "tokens": total_tokens}

        cut = max(1, len(messages) // 2)
        older = messages[:cut]
        recent = messages[cut:]

        summary_text = f"Context compressed ({len(older)} messages)."
        summary_msg = {"role": "system", "content": summary_text}
        compacted = [summary_msg] + recent
        new_tokens = sum(max(1, len(m.get("content", "").split())) for m in compacted)

        return {
            "compacted": True,
            "original_tokens": total_tokens,
            "compacted_tokens": new_tokens,
            "messages": compacted
        }

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compact_messages",
                        "description": "Compact conversation history against token budget.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "messages": {"type": "array", "items": {"type": "object"}},
                                "budget": {"type": "integer", "default": 4000}
                            },
                            "required": ["messages"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "compact_messages":
            res = ContextCompactor.compact(args.get("messages", []), int(args.get("budget", 4000)))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

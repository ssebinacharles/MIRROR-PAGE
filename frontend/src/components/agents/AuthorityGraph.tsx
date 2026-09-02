import type { Agent } from "@/types/models";

function getAllowedTools(scope: unknown): string[] {
  if (!scope || typeof scope !== "object") return [];

  const value = (scope as { allowed_tools?: unknown }).allowed_tools;

  return Array.isArray(value)
    ? value.filter((item): item is string => typeof item === "string")
    : [];
}

export function AuthorityGraph({ agents }: { agents: Agent[] }) {
  return (
    <div className="authority-graph">
      <div className="authority-node root">
        <span>Human</span>
      </div>

      {agents.map((agent) => {
        const allowedTools = getAllowedTools(agent.authority_scope);

        return (
          <div className="authority-branch" key={agent.id}>
            <div className="connector" />

            <div className="authority-node">
              <div>
                <strong>{agent.name}</strong>

                <span>
                  {allowedTools.length > 0
                    ? allowedTools.join(" · ")
                    : "no scope"}
                </span>
              </div>

              <small>{agent.status}</small>
            </div>
          </div>
        );
      })}
    </div>
  );
}
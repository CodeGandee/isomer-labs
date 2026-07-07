import { workbenchCommands$ } from "../../events";
import type { TopicGraphView } from "../../types";

export function openRecordFromNode(topicId: string, graph: TopicGraphView | undefined, nodeId: string) {
  const node = graph?.nodes.find((candidate) => candidate.id === nodeId);
  if (!node) {
    return;
  }
  const sourceIdeaId = typeof node.source?.idea_id === "string" ? node.source.idea_id : undefined;
  const ideaId = node.idea_id || sourceIdeaId;
  if (node.material_kind === "idea" && ideaId) {
    workbenchCommands$.next({ type: "open-idea", topicId, ideaId });
    return;
  }
  if (node.record_id) {
    workbenchCommands$.next({ type: "open-record", topicId, recordId: node.record_id });
  }
}

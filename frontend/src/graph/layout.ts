import dagre from 'dagre'
import type { Node, Edge } from 'reactflow'
import { nodeWidth, nodeHeight } from './constants'

export interface LayoutOptions {
  rankdir?: 'TB' | 'LR' | 'BT' | 'RL'
  nodesep?: number
  ranksep?: number
}

export function layoutGraph(
  nodes: Node[],
  edges: Edge[],
  opts: LayoutOptions = {}
): { nodes: Node[]; edges: Edge[] } {
  const dagreGraph = new dagre.graphlib.Graph()
  dagreGraph.setDefaultEdgeLabel(() => ({}))
  dagreGraph.setGraph({
    rankdir: opts.rankdir ?? 'TB',
    nodesep: opts.nodesep ?? 100,
    ranksep: opts.ranksep ?? 100,
  })

  for (const node of nodes) {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight })
  }
  for (const e of edges) {
    dagreGraph.setEdge(e.source, e.target)
  }

  dagre.layout(dagreGraph)

  const layouted = nodes.map((node) => {
    const n = dagreGraph.node(node.id)
    return {
      ...node,
      position: { x: n.x - nodeWidth / 2, y: n.y - nodeHeight / 2 },
    }
  })

  return { nodes: layouted, edges }
}

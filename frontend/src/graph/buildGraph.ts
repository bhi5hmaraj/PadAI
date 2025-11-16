import type { Node, Edge } from 'reactflow'
import type { Task } from '../types'
import { MarkerType } from 'reactflow'
import { normalizeStatus } from '../utils/status'
import { nodeWidth, nodeHeight } from './constants'

export interface GraphBuildOptions {
  nodeTypeForTask?: (task: Task) => string
  animateReadyEdges?: boolean
  rankdir?: 'TB' | 'LR' | 'BT' | 'RL'
}

export function buildNodes(
  tasks: Task[],
  updatedIds: Set<string>,
  opts: GraphBuildOptions = {}
): Node[] {
  return tasks.map((task) => {
    const status = normalizeStatus(task.status)
    const nodeType = opts.nodeTypeForTask ? opts.nodeTypeForTask(task) : 'task'
    return {
      id: task.id,
      type: nodeType,
      data: {
        label: task.title,
        status,
        assignee: task.assignee,
        taskId: task.id,
        description: (task as any).description,
        issueType: (task as any).issue_type,
        priority: (task as any).priority,
      },
      position: { x: 0, y: 0 },
      className: `task-node status-${status}${updatedIds.has(task.id) ? ' pulse' : ''}`,
      style: { width: nodeWidth, height: nodeHeight },
    } as Node
  })
}

export function buildEdges(tasks: Task[], opts: GraphBuildOptions = {}): Edge[] {
  const edges: Edge[] = []
  const idSet = new Set(tasks.map((t) => t.id))
  const rankdir = opts.rankdir ?? 'TB'
  let sourceHandleId: string = 'b'
  let targetHandleId: string = 't'
  if (rankdir === 'LR') { sourceHandleId = 'r'; targetHandleId = 'l' }
  else if (rankdir === 'RL') { sourceHandleId = 'l-src'; targetHandleId = 'r-tgt' }
  else if (rankdir === 'BT') { sourceHandleId = 't-src'; targetHandleId = 'b-tgt' }
  for (const task of tasks) {
    const deps = (task as any).dependencies || []
    for (const dep of deps) {
      const src = dep.depends_on_id
      const tgt = task.id
      if (!src || !tgt || !idSet.has(src) || !idSet.has(tgt)) continue
      const depType = String(dep.type || '').toLowerCase()
      // Style by dependency type
      let stroke = '#6b7280'
      let dash: string | undefined
      let width = 2
      let marker: any | undefined = { type: MarkerType.ArrowClosed, width: 20, height: 20 }
      let label = ''
      switch (depType) {
        case 'blocks':
          stroke = '#ef4444' // red
          width = 2.5
          label = '🔒'
          break
        case 'related':
          stroke = '#9ca3af' // gray
          dash = '6 4'
          marker = undefined
          break
        case 'parent':
          stroke = '#a855f7' // purple
          width = 2
          break
        case 'discovered-from':
          stroke = '#60a5fa' // blue
          dash = '2 4'
          break
      }

      edges.push({
        id: `${src}-${tgt}`,
        source: src,
        target: tgt,
        sourceHandle: sourceHandleId,
        targetHandle: targetHandleId,
        type: 'smoothstep',
        animated: opts.animateReadyEdges ? normalizeStatus(task.status) === 'ready' : false,
        label,
        markerEnd: marker,
        style: { strokeWidth: width, stroke, strokeDasharray: dash },
      })
    }
  }
  return edges
}

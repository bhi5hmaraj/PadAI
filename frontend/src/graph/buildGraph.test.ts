import { describe, it, expect } from 'vitest'
import { buildNodes, buildEdges } from './buildGraph'
import type { Task } from '../types'

describe('buildGraph helpers', () => {
  const tasks: Task[] = [
    { id: 'a', title: 'A', status: 'open', issue_type: 'task' },
    { id: 'b', title: 'B', status: 'in_progress', issue_type: 'bug', dependencies: [
      { issue_id: 'b', depends_on_id: 'a', type: 'blocks' }
    ] },
    { id: 'c', title: 'C', status: 'closed', issue_type: 'epic', dependencies: [
      { issue_id: 'c', depends_on_id: 'x', type: 'related' } // invalid source (ignored)
    ] },
    { id: 'd', title: 'D', status: 'ready', issue_type: 'feature', dependencies: [
      { issue_id: 'd', depends_on_id: 'a', type: 'related' }
    ] },
  ]

  it('buildNodes returns a node for each task with normalized status and type', () => {
    const nodes = buildNodes(tasks, new Set(['b']), {
      nodeTypeForTask: (t) => (t.issue_type as string) || 'task',
    })
    expect(nodes).toHaveLength(4)
    // ids preserved
    expect(nodes.map(n => n.id)).toEqual(['a','b','c','d'])
    // type mapping applied
    const types = new Map(nodes.map(n => [n.id, n.type]))
    expect(types.get('b')).toBe('bug')
    expect(types.get('d')).toBe('feature')
    expect(types.get('c')).toBe('epic')
    // pulse class applied to updated id
    const b = nodes.find(n => n.id === 'b')!
    expect(String(b.className)).toContain('pulse')
    // status normalized (closed -> completed)
    const c = nodes.find(n => n.id === 'c')!
    expect((c.data as any).status).toBe('completed')
  })

  it('buildEdges connects valid deps only and animates edges into ready tasks when enabled', () => {
    const edges = buildEdges(tasks, { animateReadyEdges: true })
    // c->x ignored (x not found); a->b and a->d remain
    const ids = edges.map(e => e.id).sort()
    expect(ids).toEqual(['a-b','a-d'])
    // animation only for edge into a ready task (d is ready)
    const ab = edges.find(e => e.id === 'a-b')!
    const ad = edges.find(e => e.id === 'a-d')!
    expect(Boolean(ab.animated)).toBe(false)
    expect(Boolean(ad.animated)).toBe(true)
  })
})


import { describe, it, expect, vi } from 'vitest'

// Mock dagre layout to avoid depending on algorithm or DOM
vi.mock('dagre', () => ({
  __esModule: true,
  default: {
    graphlib: {
      Graph: class MockGraph {
        setDefaultEdgeLabel() {}
        setGraph() {}
        setNode() {}
        setEdge() {}
        node() { return { x: 100, y: 200 } }
      },
    },
    layout: () => {},
  },
}))

import { layoutGraph } from './layout'

describe('layoutGraph', () => {
  it('returns nodes with numeric positions and preserves edges', () => {
    const nodes = [
      { id: 'n1', data: {}, position: { x: 0, y: 0 } } as any,
      { id: 'n2', data: {}, position: { x: 0, y: 0 } } as any,
    ]
    const edges = [
      { id: 'n1-n2', source: 'n1', target: 'n2' } as any,
    ]
    const { nodes: outNodes, edges: outEdges } = layoutGraph(nodes, edges, { rankdir: 'LR' })
    expect(outNodes).toHaveLength(2)
    expect(outEdges).toHaveLength(1)
    for (const n of outNodes) {
      expect(typeof n.position.x).toBe('number')
      expect(typeof n.position.y).toBe('number')
    }
  })
})


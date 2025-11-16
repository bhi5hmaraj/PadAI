// Modular TaskGraph: uses layoutTasks, TaskNode, SidePanel
import { useEffect, useMemo, useRef, useState } from 'react'
import ReactFlow, { Background, Controls, MiniMap, useNodesState, useEdgesState } from 'reactflow'
import { Task } from '../types'
import 'reactflow/dist/style.css'
import './TaskGraph.css'
import TaskNode from './TaskNode'
import BugNode from './nodes/BugNode'
import FeatureNode from './nodes/FeatureNode'
import EpicNode from './nodes/EpicNode'
import SidePanel from './SidePanel'
import { buildNodes, buildEdges } from '../graph/buildGraph'
import { layoutGraph } from '../graph/layout'
import { useTaskUpdates } from './hooks/useTaskUpdates'
import { statusToColor } from '../utils/status'
import { useWindowSize } from '../hooks/useWindowSize'
import { HORIZONTAL_LAYOUT_MIN_WIDTH } from '../graph/constants'
import { getTransitiveDeps, getBlockingDeps } from '../graph/deps'

interface TaskGraphProps { tasks: Task[]; debug?: boolean; rankdir?: 'TB'|'BT'|'LR'|'RL' }

// Pluggable node types; all map to TaskNode for now
const nodeTypes = {
  default: TaskNode,
  task: TaskNode,
  bug: BugNode,
  feature: FeatureNode,
  epic: EpicNode,
  chore: TaskNode,
}

export default function TaskGraph({ tasks, debug, rankdir: rankdirProp }: TaskGraphProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [panelOpen, setPanelOpen] = useState<boolean>(true)
  const [panelWidth, setPanelWidth] = useState<number>(380)
  const [panelHeight, setPanelHeight] = useState<number>(260)
  const containerRef = useRef<HTMLDivElement | null>(null)
  const selectedTask = useMemo(() => tasks.find((t) => t.id === selectedId), [tasks, selectedId])

  // Detect updated tasks via updated_at
  // Modular hook: track updated nodes and compute change summaries
  const { updatedIds, updateSummaries } = useTaskUpdates(tasks)

  // Responsive orientation: left-right when wide, top-down when narrow
  const { width } = useWindowSize()
  const rankdir: 'TB'|'BT'|'LR'|'RL' = rankdirProp ?? (width >= HORIZONTAL_LAYOUT_MIN_WIDTH ? 'LR' : 'TB')
  const mobilePanel = width <= 900

  // Transitive dependency highlights for the selected task
  const depIds = useMemo(() => (selectedId ? getTransitiveDeps(tasks, selectedId) : new Set<string>()), [tasks, selectedId])
  const blockedDepIds = useMemo(() => (selectedId ? getBlockingDeps(tasks, selectedId) : new Set<string>()), [tasks, selectedId])


  const { nodes: layoutedNodes, edges: layoutedEdges } = useMemo(() => {
    const nodes = buildNodes(tasks, updatedIds, {
      nodeTypeForTask: (t) => (t.issue_type as string) || 'task',
    })
    const edges = buildEdges(tasks, { animateReadyEdges: true, rankdir })
    // Debug logging can be added if needed
    // Attach change summaries to node data when available
    const withSummaries = {
      nodes: nodes.map((n) => {
        const inDeps = depIds.has(n.id)
        const isSel = n.id === selectedId
        const mods: string[] = []
        if (selectedId && !(inDeps || isSel)) mods.push('dimmed')
        if (inDeps) mods.push('highlight-dep')
        if (blockedDepIds.has(n.id)) mods.push('highlight-blocked')
        return {
          ...n,
          data: { ...(n.data as any), updateSummary: updateSummaries.get(n.id), extraClasses: mods.join(' ') },
        }
      }),
      edges: edges.map((e) => {
        const srcIn = depIds.has(e.source as string)
        const tgtIn = depIds.has(e.target as string) || e.target === selectedId
        const cls = [String((e as any).className || '')]
        let style = e.style
        if (srcIn && tgtIn) {
          cls.push('highlight-edge')
          style = { ...(style || {}), strokeWidth: 4, stroke: '#22d3ee', opacity: 1 }
        }
        return { ...e, className: cls.join(' ').trim(), style }
      }),
    }
    return layoutGraph(withSummaries.nodes, withSummaries.edges, { rankdir })
  }, [tasks, updatedIds, updateSummaries, rankdir, depIds, blockedDepIds, selectedId])

  const [nodes, setNodes, onNodesChange] = useNodesState(layoutedNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(layoutedEdges)

  useEffect(() => {
    setNodes(layoutedNodes)
    setEdges(layoutedEdges)
  }, [layoutedNodes, layoutedEdges, setNodes, setEdges])

  if (!tasks.length) return <div className="empty-state"><p>No tasks found</p></div>

  // Resizer handlers
  function onResizeXStart(e: React.MouseEvent) {
    e.preventDefault()
    const startX = e.clientX
    const startW = panelWidth
    function onMove(ev: MouseEvent) {
      const dx = startX - ev.clientX // dragging left -> positive
      const next = Math.max(240, Math.min(800, startW + dx))
      setPanelWidth(next)
    }
    function onUp() {
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseup', onUp)
    }
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)
  }

  function onResizeYStart(e: React.MouseEvent) {
    e.preventDefault()
    const startY = e.clientY
    const startH = panelHeight
    function onMove(ev: MouseEvent) {
      const dy = ev.clientY - startY // dragging down -> positive
      const next = Math.max(120, Math.min(600, startH + dy))
      setPanelHeight(next)
    }
    function onUp() {
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseup', onUp)
    }
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)
  }

  const containerStyle: React.CSSProperties = mobilePanel
    ? (panelOpen ? { gridTemplateRows: `${panelHeight}px 1fr` } : { gridTemplateRows: `40px 1fr` })
    : (panelOpen ? { gridTemplateColumns: `1fr ${panelWidth}px` } : { gridTemplateColumns: `1fr 0px` })

  return (
    <div ref={containerRef} className={`task-graph static ${panelOpen ? 'panel-open' : 'panel-collapsed'} layout-${rankdir}`} style={containerStyle}>
      <div className="graph-area">
        {debug && (
          <div className="debug-overlay">
            <div>Selected: <code>{selectedId || '—'}</code></div>
            <div>Deps: {depIds.size} · Blocked: {blockedDepIds.size}</div>
          </div>
        )}
        <ReactFlow
          style={{ width: '100%', height: '100%' }}
          nodes={nodes}
          edges={edges}
        onNodeClick={(_, node) => { setSelectedId(node.id); setPanelOpen(true) }}
        onPaneClick={() => setSelectedId(null)}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          minZoom={0.1}
          maxZoom={2}
        >
          <Background color="var(--background-grid)" gap={16} />
          <Controls />
          <MiniMap
          nodeColor={(node) => {
            // Prefer normalized status from node data
            const st = (node.data as any)?.status as any
            return statusToColor(st ?? 'open')
          }}
          maskColor="var(--minimap-mask)"
          />
        </ReactFlow>
      </div>

      <SidePanel
        staticMode
        open={panelOpen}
        task={selectedTask || null}
        onClose={() => setSelectedId(null)}
        onClear={() => setSelectedId(null)}
        onToggle={() => setPanelOpen((v) => !v)}
        resizableX={!mobilePanel}
        resizableY={mobilePanel}
        onResizeXStart={onResizeXStart}
        onResizeYStart={onResizeYStart}
      />
    </div>
  )
}

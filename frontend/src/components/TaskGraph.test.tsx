import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Theme } from '@radix-ui/themes'
import TaskGraph from './TaskGraph'
import type { Task } from '../types'

// Mock ReactFlow to avoid canvas/dom rendering issues in tests
vi.mock('reactflow', () => ({
  __esModule: true,
  default: ({ children, onNodeClick, nodes }: any) => (
    <div data-testid="react-flow">
      <div data-testid="node-count">{nodes?.length || 0}</div>
      {nodes?.map((node: any) => (
        <button
          key={node.id}
          data-testid={`node-${node.id}`}
          onClick={() => onNodeClick?.(null, node)}
        >
          {node.id}
        </button>
      ))}
      {children}
    </div>
  ),
  Background: () => <div data-testid="background" />,
  Controls: () => <div data-testid="controls" />,
  MiniMap: () => <div data-testid="minimap" />,
  useNodesState: (initial: any) => [initial, vi.fn(), vi.fn()],
  useEdgesState: (initial: any) => [initial, vi.fn(), vi.fn()],
  MarkerType: { ArrowClosed: 'arrowclosed' },
  Position: { Top: 'top', Bottom: 'bottom' },
  Handle: () => null,
}))

// Mock dagre to avoid layout computation in tests
vi.mock('dagre', () => ({
  __esModule: true,
  default: {
    graphlib: {
      Graph: class MockGraph {
        setDefaultEdgeLabel = vi.fn()
        setGraph = vi.fn()
        setNode = vi.fn()
        setEdge = vi.fn()
        node = vi.fn(() => ({ x: 100, y: 100 }))
      },
    },
    layout: vi.fn(),
  },
}))

const mockTasks: Task[] = [
  {
    id: 'task-1',
    title: 'First Task',
    status: 'pending',
    assignee: 'Alice',
  },
  {
    id: 'task-2',
    title: 'Second Task',
    status: 'in_progress',
    assignee: 'Bob',
  },
  {
    id: 'task-3',
    title: 'Third Task',
    status: 'completed',
    assignee: 'Charlie',
  },
]

describe('TaskGraph', () => {
  it('renders empty state when no tasks are provided', () => {
    render(
      <Theme>
        <TaskGraph tasks={[]} />
      </Theme>
    )
    expect(screen.getByText('No tasks found')).toBeInTheDocument()
  })

  it('renders ReactFlow with correct number of tasks', () => {
    render(
      <Theme>
        <TaskGraph tasks={mockTasks} />
      </Theme>
    )

    expect(screen.getByTestId('react-flow')).toBeInTheDocument()
    expect(screen.getByTestId('node-count')).toHaveTextContent('3')
  })

  it('renders ReactFlow components (Background, Controls, MiniMap)', () => {
    render(
      <Theme>
        <TaskGraph tasks={mockTasks} />
      </Theme>
    )

    expect(screen.getByTestId('background')).toBeInTheDocument()
    expect(screen.getByTestId('controls')).toBeInTheDocument()
    expect(screen.getByTestId('minimap')).toBeInTheDocument()
  })

  it('opens side panel when a node is clicked', () => {
    render(
      <Theme>
        <TaskGraph tasks={mockTasks} />
      </Theme>
    )

    // Initially, side panel should not show task details
    expect(screen.queryByText('First Task')).not.toBeInTheDocument()

    // Click on a node
    const nodeButton = screen.getByTestId('node-task-1')
    fireEvent.click(nodeButton)

    // Now the side panel should show the task details
    expect(screen.getAllByText('First Task').length).toBeGreaterThan(0)
  })

  it('collapses side panel when collapse button is clicked', () => {
    render(
      <Theme>
        <TaskGraph tasks={mockTasks} />
      </Theme>
    )

    // Click on a node to open side panel
    const nodeButton = screen.getByTestId('node-task-1')
    fireEvent.click(nodeButton)
    expect(screen.getAllByText('First Task').length).toBeGreaterThan(0)

    // Click collapse button
    const collapseBtn = screen.getByText(/Collapse|Expand/)
    fireEvent.click(collapseBtn)

    // Panel should be collapsed
    const panel = document.querySelector('.sidepanel.static')
    expect(panel).toHaveClass('collapsed')
  })

  it('displays correct task information in side panel', () => {
    render(
      <Theme>
        <TaskGraph tasks={mockTasks} />
      </Theme>
    )

    // Click on task-2
    const nodeButton = screen.getByTestId('node-task-2')
    fireEvent.click(nodeButton)

    // Verify task details are shown
    expect(screen.getAllByText('Second Task').length).toBeGreaterThan(0)
    // task-2 appears multiple times (button + side panel), so we use getAllByText
    expect(screen.getAllByText('task-2').length).toBeGreaterThan(0)
    expect(screen.getAllByText('in_progress').length).toBeGreaterThan(0)
    expect(screen.getAllByText('Bob').length).toBeGreaterThan(0)
  })
})

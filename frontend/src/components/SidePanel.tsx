import { Text, Badge } from '@radix-ui/themes'
import type { Task } from '../types'

interface Props {
  task: Task | null
  onClose: () => void
  staticMode?: boolean
  open?: boolean
  onToggle?: () => void
  onClear?: () => void
  // Resizer (optional in static mode)
  resizableX?: boolean
  resizableY?: boolean
  onResizeXStart?: (e: React.MouseEvent) => void
  onResizeYStart?: (e: React.MouseEvent) => void
}

// Helper to format relative time
function formatRelativeTime(timestamp: string): string {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'just now'
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    if (diffDays < 30) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
    return date.toLocaleDateString()
  } catch {
    return timestamp
  }
}

// Helper to build update history from task data
function buildUpdateHistory(task: Task) {
  const events: Array<{ timestamp: string; event: string; detail: string }> = []

  const createdAt = (task as any).created_at
  const updatedAt = (task as any).updated_at

  if (createdAt) {
    events.push({
      timestamp: createdAt,
      event: 'Created',
      detail: `Task created${task.assignee ? ` and assigned to ${task.assignee}` : ''}`
    })
  }

  if (updatedAt && updatedAt !== createdAt) {
    const statusText = task.status ? ` (status: ${task.status})` : ''
    events.push({
      timestamp: updatedAt,
      event: 'Updated',
      detail: `Task modified${statusText}`
    })
  }

  // Sort by timestamp (most recent first)
  events.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())

  return events
}

export default function SidePanel({ task, onClose, staticMode, open: openProp, onToggle, onClear, resizableX, resizableY, onResizeXStart, onResizeYStart }: Props) {
  const open = staticMode ? Boolean(openProp) : !!task
  const history = task ? buildUpdateHistory(task) : []

  function renderJsonTable(data: any) {
    if (!data) return <div style={{ fontSize: 12, color: 'var(--label-color)' }}>—</div>
    const entries = Object.entries(data as Record<string, any>)
    const renderValue = (val: any) => {
      const t = typeof val
      if (val == null) return <span className="muted">null</span>
      if (t === 'string' || t === 'number' || t === 'boolean') return <span>{String(val)}</span>
      if (Array.isArray(val)) {
        const summary = `${val.length} item${val.length !== 1 ? 's' : ''}`
        return (
          <details>
            <summary>{summary}</summary>
            <pre style={{ fontSize: 11, marginTop: 6 }}>{JSON.stringify(val, null, 2)}</pre>
          </details>
        )
      }
      const keys = Object.keys(val)
      const summary = `${keys.length} field${keys.length !== 1 ? 's' : ''}`
      return (
        <details>
          <summary>{summary}</summary>
          <pre style={{ fontSize: 11, marginTop: 6 }}>{JSON.stringify(val, null, 2)}</pre>
        </details>
      )
    }

    return (
      <table className="kv-table">
        <tbody>
          {entries.map(([k, v]) => (
            <tr key={k}>
              <th>{k}</th>
              <td>{renderValue(v)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )
  }

  if (staticMode) {
    return (
      <div className={`sidepanel static ${open ? 'open' : 'collapsed'}`}>
        {resizableX && <div className="panel-resizer resizer-x" onMouseDown={onResizeXStart} />}
        {resizableY && <div className="panel-resizer resizer-y" onMouseDown={onResizeYStart} />}
        <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
          <Text size="3" weight="bold">{task ? task.title : 'Details'}</Text>
          <div style={{ display: 'flex', gap: 8 }}>
            {task && <button className="btn" onClick={onClear}>Clear</button>}
            <button className="btn" onClick={onToggle}>{open ? 'Collapse' : 'Expand'}</button>
          </div>
        </header>
        <div className="body">
          {task ? (
            <>
              <div className="row"><span className="label">ID</span><span>{task.id}</span></div>
              <div className="row"><span className="label">Status</span><span>{task.status}</span></div>
              {(task as any).assignee && <div className="row"><span className="label">Assignee</span><span>{(task as any).assignee}</span></div>}
              {typeof (task as any).priority !== 'undefined' && (
                <div className="row">
                  <span className="label">Priority</span>
                  <span>
                    <Badge
                      variant="soft"
                      color={((p:number)=> p===0?'red':p===1?'yellow':p===2?'green':'gray')((task as any).priority)}
                      className="badge prio"
                    >
                      P{(task as any).priority}
                    </Badge>
                  </span>
                </div>
              )}
              {(task as any).issue_type && <div className="row"><span className="label">Type</span><span>{(task as any).issue_type}</span></div>}

              <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Description</div>
              <div style={{ whiteSpace: 'pre-wrap', fontSize: 13 }}>{(task as any).description || '—'}</div>

              {(task as any).dependencies && (task as any).dependencies.length > 0 && (
                <>
                  <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Dependencies</div>
                  <ul style={{ paddingLeft: 16, margin: 0 }}>
                    {(task as any).dependencies.map((d: any) => (
                      <li key={`${d.depends_on_id}-${task.id}`} style={{ fontSize: 13 }}>
                        {d.type}: {d.depends_on_id}
                      </li>
                    ))}
                  </ul>
                </>
              )}

              {history.length > 0 && (
                <>
                  <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Update History</div>
                  <div className="history-timeline">
                    {history.map((event, idx) => (
                      <div key={idx} className="history-event">
                        <div className="history-marker" />
                        <div className="history-content">
                          <div className="history-header">
                            <span className="history-event-name">{event.event}</span>
                            <span className="history-time">{formatRelativeTime(event.timestamp)}</span>
                          </div>
                          <div className="history-detail">{event.detail}</div>
                          <div className="history-timestamp">{event.timestamp}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}

              <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Raw Data</div>
              {renderJsonTable(task)}
            </>
          ) : (
            <div style={{ fontSize: 12, color: 'var(--label-color)' }}>Select a node to view details</div>
          )}
        </div>
      </div>
    )
  }

  return (
    <>
      <div className={`sidepanel-overlay ${open ? 'open' : ''}`} onClick={onClose} />
      <div className={`sidepanel ${open ? 'open' : ''}`}>
        {task && (
          <>
            <header>
              <Text size="3" weight="bold">{task.title}</Text>
              <button className="btn" onClick={onClose}>Close</button>
            </header>
            <div className="body">
              <div className="row"><span className="label">ID</span><span>{task.id}</span></div>
              <div className="row"><span className="label">Status</span><span>{task.status}</span></div>
              {(task as any).assignee && <div className="row"><span className="label">Assignee</span><span>{(task as any).assignee}</span></div>}
              {typeof (task as any).priority !== 'undefined' && (
                <div className="row">
                  <span className="label">Priority</span>
                  <span>
                    <Badge
                      variant="soft"
                      color={((p:number)=> p===0?'red':p===1?'yellow':p===2?'green':'gray')((task as any).priority)}
                      className="badge prio"
                    >
                      P{(task as any).priority}
                    </Badge>
                  </span>
                </div>
              )}
              {(task as any).issue_type && <div className="row"><span className="label">Type</span><span>{(task as any).issue_type}</span></div>}

              <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Description</div>
              <div style={{ whiteSpace: 'pre-wrap', fontSize: 13 }}>{(task as any).description || '—'}</div>

              {(task as any).dependencies && (task as any).dependencies.length > 0 && (
                <>
                  <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Dependencies</div>
                  <ul style={{ paddingLeft: 16, margin: 0 }}>
                    {(task as any).dependencies.map((d: any) => (
                      <li key={`${d.depends_on_id}-${task.id}`} style={{ fontSize: 13 }}>
                        {d.type}: {d.depends_on_id}
                      </li>
                    ))}
                  </ul>
                </>
              )}

              {history.length > 0 && (
                <>
                  <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Update History</div>
                  <div className="history-timeline">
                    {history.map((event, idx) => (
                      <div key={idx} className="history-event">
                        <div className="history-marker" />
                        <div className="history-content">
                          <div className="history-header">
                            <span className="history-event-name">{event.event}</span>
                            <span className="history-time">{formatRelativeTime(event.timestamp)}</span>
                          </div>
                          <div className="history-detail">{event.detail}</div>
                          <div className="history-timestamp">{event.timestamp}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}

              <div style={{ margin: '12px 0 8px 0', fontSize: 12, color: 'var(--label-color)' }}>Raw Data</div>
              {renderJsonTable(task)}
            </div>
          </>
        )}
      </div>
    </>
  )
}

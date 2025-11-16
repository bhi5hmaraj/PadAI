import { Card, Flex, Text, Badge } from '@radix-ui/themes'
import { Handle, Position } from 'reactflow'

export default function NodeBase({ data }: { data: any }) {
  const { label, status, assignee, taskId, description, issueType, priority, updateSummary, extraClasses } = data
  const prioColor = typeof priority === 'number'
    ? (priority === 0 ? 'red' : priority === 1 ? 'yellow' : priority === 2 ? 'green' : 'gray')
    : 'gray'
  const typeClass = issueType ? `type-${String(issueType).toLowerCase()}` : ''
  return (
    <Card variant="surface" className={`task-card ${typeClass} status-${status} ${extraClasses || ''}`}>
      {/* Handles for all orientations and both directions */}
      {/* TB / TD */}
      <Handle type="target" position={Position.Top} id="t" style={{ opacity: 0 }} />
      <Handle type="source" position={Position.Bottom} id="b" style={{ opacity: 0 }} />
      {/* BT / DT */}
      <Handle type="source" position={Position.Top} id="t-src" style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Bottom} id="b-tgt" style={{ opacity: 0 }} />
      {/* LR */}
      <Handle type="target" position={Position.Left} id="l" style={{ opacity: 0 }} />
      <Handle type="source" position={Position.Right} id="r" style={{ opacity: 0 }} />
      {/* RL */}
      <Handle type="source" position={Position.Left} id="l-src" style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Right} id="r-tgt" style={{ opacity: 0 }} />
      <span className={`status-dot status-${status}`} title={status} />
      <Flex align="center" justify="between" className="task-header">
        <div className="title-wrap">
          <Text as="div" size="3" weight="bold" className="task-title" title={label}>{label}</Text>
          <Badge variant="soft" color="gray" className="id-badge">{taskId}</Badge>
        </div>
      </Flex>
      <Flex gap="2" className="task-meta">
        {issueType && <Badge variant="soft" color="gray" className="badge type">{String(issueType).toUpperCase()}</Badge>}
        {priority !== undefined && <Badge variant="soft" color={prioColor as any} className="badge prio">P{priority}</Badge>}
      </Flex>
      <Text as="div" size="2" className="task-desc" title={description || 'No description'}>
        {description && String(description).trim().length > 0 ? description : 'No description'}
      </Text>
      {updateSummary && (
        <Text as="div" size="1" className="update-summary" title={updateSummary}>
          Updated: {updateSummary}
        </Text>
      )}
      <div className="task-footer">
        <Text as="div" size="2" className="task-assignee">{assignee ? <>👤 {assignee}</> : <span className="muted">Unassigned</span>}</Text>
      </div>
    </Card>
  )
}

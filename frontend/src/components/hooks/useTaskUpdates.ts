import { useEffect, useRef, useState } from 'react'
import type { Task } from '../../types'

function normStatus(s?: string): string {
  if (!s) return 'open'
  const v = s.toLowerCase()
  if (v === 'closed' || v === 'completed') return 'completed'
  if (v === 'in_progress' || v === 'in-progress') return 'in_progress'
  if (v === 'ready') return 'ready'
  return v
}

export function useTaskUpdates(tasks: Task[]) {
  const lastUpdatedAt = useRef<Map<string, string>>(new Map())
  const prevTasks = useRef<Map<string, Task>>(new Map())
  const [updatedIds, setUpdatedIds] = useState<Set<string>>(new Set())
  const [updateSummaries, setUpdateSummaries] = useState<Map<string, string>>(new Map())

  useEffect(() => {
    const newUpdatedAt = new Map<string, string>()
    const newPrevTasks = new Map<string, Task>()
    const changed = new Set<string>()
    const summaries = new Map<string, string>()

    for (const t of tasks) {
      const prev = lastUpdatedAt.current.get(t.id)
      const cur = (t as any).updated_at || ''
      newUpdatedAt.set(t.id, cur)
      newPrevTasks.set(t.id, t)
      if (prev && cur && prev !== cur) {
        changed.add(t.id)

        const prevTask = prevTasks.current.get(t.id)
        const changes: string[] = []
        if (prevTask) {
          if (normStatus(prevTask.status) !== normStatus(t.status)) {
            changes.push(`status: ${normStatus(prevTask.status)} → ${normStatus(t.status)}`)
          }
          const prevAssignee = prevTask.assignee || 'none'
          const curAssignee = t.assignee || 'none'
          if (prevAssignee !== curAssignee) {
            changes.push(`assignee: ${prevAssignee} → ${curAssignee}`)
          }
          if (prevTask.priority !== t.priority && typeof t.priority !== 'undefined') {
            const p0 = typeof prevTask.priority === 'number' ? `P${prevTask.priority}` : '—'
            const p1 = `P${t.priority}`
            changes.push(`priority: ${p0} → ${p1}`)
          }
          if (prevTask.title !== t.title) {
            changes.push('title updated')
          }
          if ((prevTask.description || '') !== (t.description || '')) {
            changes.push('description updated')
          }
        } else {
          changes.push('created')
        }

        const summary = changes.slice(0, 2).join(', ')
        if (summary) summaries.set(t.id, summary)
      }
    }

    lastUpdatedAt.current = newUpdatedAt
    prevTasks.current = newPrevTasks
    if (changed.size) setUpdatedIds(changed)
    if (summaries.size) setUpdateSummaries(summaries)
  }, [tasks])

  return { updatedIds, updateSummaries }
}


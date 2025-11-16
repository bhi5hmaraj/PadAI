import type { Task } from '../types'
import { normalizeStatus } from '../utils/status'

export function getTransitiveDeps(tasks: Task[], targetId: string): Set<string> {
  const byId = new Map<string, Task>()
  for (const t of tasks) byId.set(t.id, t)

  const depsMap = new Map<string, string[]>() // id -> depends_on_ids
  for (const t of tasks) {
    const deps = ((t as any).dependencies || []) as Array<{ depends_on_id?: string }>
    depsMap.set(t.id, deps.map(d => d.depends_on_id!).filter(Boolean))
  }

  const visited = new Set<string>()
  const stack = [...(depsMap.get(targetId) || [])]
  while (stack.length) {
    const cur = stack.pop()!
    if (!cur || visited.has(cur)) continue
    visited.add(cur)
    for (const nxt of depsMap.get(cur) || []) {
      if (!visited.has(nxt)) stack.push(nxt)
    }
  }
  return visited
}

export function getBlockingDeps(tasks: Task[], targetId: string): Set<string> {
  const all = getTransitiveDeps(tasks, targetId)
  const blocked = new Set<string>()
  for (const id of all) {
    const t = tasks.find(x => x.id === id)
    const st = normalizeStatus(t?.status)
    if (st !== 'completed') blocked.add(id)
  }
  return blocked
}


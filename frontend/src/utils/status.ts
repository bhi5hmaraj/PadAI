export type NormalizedStatus = 'open' | 'ready' | 'in_progress' | 'completed'

export function normalizeStatus(s?: string): NormalizedStatus {
  if (!s) return 'open'
  const v = s.toLowerCase()
  if (v === 'closed' || v === 'complete' || v === 'completed') return 'completed'
  if (v === 'in_progress' || v === 'in-progress' || v === 'progress') return 'in_progress'
  if (v === 'ready') return 'ready'
  return 'open'
}

export function statusToColor(status: NormalizedStatus): string {
  switch (status) {
    case 'completed':
      return '#60a5fa'
    case 'in_progress':
      return '#fbbf24'
    case 'ready':
      return '#4ade80'
    default:
      return '#6b7280'
  }
}


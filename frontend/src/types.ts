export interface Task {
  id: string;
  title: string;
  status?: string;
  assignee?: string;
  description?: string;
  issue_type?: string; // task|bug|feature|epic|chore
  priority?: number;   // 0-4
  created_at?: string;
  updated_at?: string;
  dependencies?: Dependency[];
}

export interface Dependency {
  issue_id: string;
  depends_on_id: string;
  type: 'blocks' | 'related' | 'parent' | 'discovered-from';
}

export interface Status {
  total: number;
  ready: number;
  in_progress: number;
  completed: number;
}

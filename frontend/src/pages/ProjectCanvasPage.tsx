import { useMemo, useCallback, useState, useEffect, useRef } from "react"
import { useParams, Link } from "react-router-dom"
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  type Connection,
  type Node,
  type Edge,
  useNodesState,
  useEdgesState,
  MarkerType,
} from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { useCanvas } from "@/hooks/useCanvas"
import { useApproveProposal, useUpdateGoal, useDeleteGoal } from "@/hooks/useGoals"
import { useDeletePremise } from "@/hooks/usePremises"
import { PremiseNode } from "@/components/canvas/PremiseNode"
import { GoalNode } from "@/components/canvas/GoalNode"
import { ConfirmDialog } from "@/components/canvas/ConfirmDialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const nodeTypes = {
  premise: PremiseNode,
  goal: GoalNode,
}

export function ProjectCanvasPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const { data, isLoading, refetch } = useCanvas(projectId!)
  const approveProposal = useApproveProposal(projectId!)
  const updateGoal = useUpdateGoal(projectId!)
  const deleteGoal = useDeleteGoal(projectId!)
  const deletePremise = useDeletePremise(projectId!)

  const [edgeToDelete, setEdgeToDelete] = useState<Edge | null>(null)
  const [goalToDelete, setGoalToDelete] = useState<string | null>(null)
  const [premiseToDelete, setPremiseToDelete] = useState<string | null>(null)

  const handleDeletePremise = useCallback((premiseId: string) => {
    setPremiseToDelete(premiseId)
  }, [])

  const handleDeleteGoal = useCallback((goalId: string) => {
    setGoalToDelete(goalId)
  }, [])

  const initialNodes: Node[] = useMemo(() => {
    if (!data) return []
    const premiseNodes = data.premises.map((p, i) => ({
      id: `premise-${p.id}`,
      type: "premise",
      position: { x: 50, y: 100 + i * 120 },
      data: { premise: p, onDelete: handleDeletePremise },
    }))
    const goalNodes = data.goals.map((g, i) => ({
      id: `goal-${g.id}`,
      type: "goal",
      position: { x: 500, y: 100 + i * 150 },
      data: { goal: g, onDelete: handleDeleteGoal },
    }))
    return [...premiseNodes, ...goalNodes]
  }, [data, handleDeletePremise, handleDeleteGoal])

  const initialEdges: Edge[] = useMemo(() => {
    if (!data) return []
    return data.goals.flatMap((g) =>
      g.premise_ids.map((pid) => ({
        id: `edge-${g.id}-${pid}`,
        source: `premise-${pid}`,
        target: `goal-${g.id}`,
        type: "smoothstep",
        markerEnd: { type: MarkerType.ArrowClosed },
        style: { stroke: "#9ca3af" },
      })),
    )
  }, [data])

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  // Track if we've done initial sync to avoid double-setting on mount
  const hasInitializedRef = useRef(false)
  // Track DB edge IDs to detect user-added edges
  const dbEdgeIdsRef = useRef<Set<string>>(new Set())

  useEffect(() => {
    setNodes(initialNodes)

    if (!data) {
      setEdges(initialEdges)
      dbEdgeIdsRef.current = new Set()
      return
    }

    const currentDbEdgeIds = new Set(initialEdges.map((e) => e.id))

    // On mount — always set edges from initial data
    if (!hasInitializedRef.current) {
      hasInitializedRef.current = true
      dbEdgeIdsRef.current = currentDbEdgeIds
      setEdges(initialEdges)
      return
    }

    // After refetch — DB edges changed. Merge: keep DB edges + user-added edges
    const prevIds = dbEdgeIdsRef.current
    const dbChanged =
      prevIds.size !== currentDbEdgeIds.size ||
      ![...prevIds].every((id) => currentDbEdgeIds.has(id))

    if (dbChanged) {
      // DB edges changed (e.g. new connection saved)
      // Keep edges that are either in DB or were user-added
      setEdges((prevEdges) => {
        const merged = [
          ...initialEdges,
          ...prevEdges.filter((e) => !currentDbEdgeIds.has(e.id)),
        ]
        dbEdgeIdsRef.current = currentDbEdgeIds
        return merged
      })
    }
    // else: DB edges unchanged — don't touch edges
  }, [initialNodes, initialEdges, setNodes, setEdges, data])

  const confirmPremiseDelete = useCallback(() => {
    if (!premiseToDelete) return
    deletePremise.mutate(premiseToDelete)
    setNodes((nds) => nds.filter((n) => n.id !== `premise-${premiseToDelete}`))
    setEdges((eds) =>
      eds.filter((e) => e.source !== `premise-${premiseToDelete}`),
    )
    setPremiseToDelete(null)
  }, [premiseToDelete, deletePremise, setNodes, setEdges])

  const confirmGoalDelete = useCallback(() => {
    if (!goalToDelete) return
    deleteGoal.mutate(goalToDelete)
    setNodes((nds) => nds.filter((n) => n.id !== `goal-${goalToDelete}`))
    setEdges((eds) =>
      eds.filter((e) => e.target !== `goal-${goalToDelete}`),
    )
    setGoalToDelete(null)
  }, [goalToDelete, deleteGoal, setNodes, setEdges])

  const onEdgeClick = useCallback((event: React.MouseEvent, edge: Edge) => {
    event.stopPropagation()
    setEdgeToDelete(edge)
  }, [])

  const confirmEdgeDelete = useCallback(() => {
    if (!edgeToDelete || !data) return
    const premiseId = edgeToDelete.source.replace("premise-", "")
    const goalId = edgeToDelete.target.replace("goal-", "")
    const goal = data.goals.find((g) => g.id === goalId)
    if (!goal) return
    const newPremiseIds = goal.premise_ids.filter((id) => id !== premiseId)
    updateGoal.mutate({ goalId, payload: { premise_ids: newPremiseIds } })
    setEdges((eds) => eds.filter((e) => e.id !== edgeToDelete.id))
    setEdgeToDelete(null)
  }, [edgeToDelete, data, updateGoal, setEdges])

  const onConnect = useCallback(
    (connection: Connection) => {
      const premiseNodeId = connection.source
      const goalNodeId = connection.target
      if (!premiseNodeId?.startsWith("premise-") || !goalNodeId?.startsWith("goal-")) {
        return
      }
      const premiseId = premiseNodeId.replace("premise-", "")
      const goalId = goalNodeId.replace("goal-", "")
      const goal = data?.goals.find((g) => g.id === goalId)
      if (!goal) return
      const newPremiseIds = [...new Set([...goal.premise_ids, premiseId])]
      updateGoal.mutate({ goalId, payload: { premise_ids: newPremiseIds } })
      // Add edge locally for instant feedback
      setEdges((eds) =>
        addEdge(
          {
            ...connection,
            type: "smoothstep",
            markerEnd: { type: MarkerType.ArrowClosed },
            style: { stroke: "#9ca3af" },
          },
          eds,
        ),
      )
      // Refetch canvas to persist edge in initialEdges
      // This ensures the edge survives unmount/remount
      refetch()
    },
    [data, updateGoal, setEdges, refetch],
  )

  const handleApprove = async (proposalId: string) => {
    const proposal = data?.proposals.find((p) => p.id === proposalId)
    if (!proposal) return
    await approveProposal.mutateAsync({
      formulation: proposal.formulation,
      deadline: proposal.deadline ?? null,
      priority: proposal.priority ?? 3,
      premise_ids: proposal.premise_ids,
    })
    // Обновляем канвас — новая цель должна появиться с связями
    await refetch()
  }

  if (isLoading) {
    return <div className="p-6">Загрузка канваса...</div>
  }

  return (
    <div className="flex h-screen">
      <div className="w-[320px] border-r bg-gray-50 p-4 overflow-y-auto">
        <Link to={`/projects/${projectId}`}>
          <Button variant="ghost" size="sm" className="mb-4">← Назад</Button>
        </Link>
        <h2 className="text-lg font-bold mb-4">Предложенные цели</h2>
        {!data?.proposals.length ? (
          <p className="text-sm text-muted-foreground">Нет предложений</p>
        ) : (
          <div className="space-y-2">
            {data.proposals.map((p) => (
              <div key={p.id} className="border rounded-lg p-3 bg-yellow-50 relative">
                {p.confidence < 1 && (
                  <Badge className="absolute top-2 right-2 bg-orange-400 text-white hover:bg-orange-500">
                    LLM TODO
                  </Badge>
                )}
                <div className="text-xs font-semibold text-yellow-800 mb-1">
                  {p.rule}
                </div>
                <div className="text-sm font-medium">{p.formulation}</div>
                {p.deadline && (
                  <div className="text-xs text-gray-600 mt-1">до {p.deadline}</div>
                )}
                <div className="flex gap-2 mt-2">
                  <Button
                    size="sm"
                    onClick={() => handleApprove(p.id)}
                  >
                    Утвердить
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onEdgeClick={onEdgeClick}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      <ConfirmDialog
        open={!!edgeToDelete}
        title="Удалить связь?"
        description="Связь между вводной и целью будет удалена."
        onConfirm={confirmEdgeDelete}
        onCancel={() => setEdgeToDelete(null)}
      />

      <ConfirmDialog
        open={!!goalToDelete}
        title="Удалить цель?"
        description="Цель будет удалена. Связи с вводными — тоже."
        onConfirm={confirmGoalDelete}
        onCancel={() => setGoalToDelete(null)}
      />

      <ConfirmDialog
        open={!!premiseToDelete}
        title="Удалить вводную?"
        description="Вводная будет удалена. Связи с целями — тоже."
        onConfirm={confirmPremiseDelete}
        onCancel={() => setPremiseToDelete(null)}
      />
    </div>
  )
}

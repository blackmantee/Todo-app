import { useEffect, useState } from 'react'
import {
  DndContext,
  KeyboardSensor,
  PointerSensor,
  closestCenter,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import {
  SortableContext,
  arrayMove,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import * as api from './api'

function TodoItem({ todo, onToggle, onDelete }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: todo.id })

  const style = { transform: CSS.Transform.toString(transform), transition }

  return (
    <li ref={setNodeRef} style={style} className={`todo ${isDragging ? 'dragging' : ''}`}>
      <button className="handle" aria-label="Drag to reorder" {...attributes} {...listeners}>
        ⠿
      </button>
      <label className={todo.done ? 'done' : ''}>
        <input type="checkbox" checked={todo.done} onChange={() => onToggle(todo)} />
        <span>{todo.title}</span>
      </label>
      <button className="delete" aria-label="Delete" onClick={() => onDelete(todo)}>
        ✕
      </button>
    </li>
  )
}

export default function App() {
  const [todos, setTodos] = useState([])
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  useEffect(() => {
    api.getTodos().then(setTodos).catch(() => setError('Could not reach the server.'))
  }, [])

  async function handleAdd(e) {
    e.preventDefault()
    if (!title.trim()) return
    const todo = await api.addTodo(title)
    setTodos([...todos, todo])
    setTitle('')
  }

  async function handleToggle(todo) {
    const updated = await api.updateTodo(todo.id, { done: !todo.done })
    setTodos(todos.map((t) => (t.id === updated.id ? updated : t)))
  }

  async function handleDelete(todo) {
    await api.deleteTodo(todo.id)
    setTodos(todos.filter((t) => t.id !== todo.id))
  }

  function handleDragEnd({ active, over }) {
    if (!over || active.id === over.id) return
    const oldIndex = todos.findIndex((t) => t.id === active.id)
    const newIndex = todos.findIndex((t) => t.id === over.id)
    const reordered = arrayMove(todos, oldIndex, newIndex)
    setTodos(reordered) // update the screen immediately
    api.reorderTodos(reordered.map((t) => t.id)) // then save the new order
  }

  const remaining = todos.filter((t) => !t.done).length

  return (
    <main className="app">
      <h1>To-Do List</h1>

      <form onSubmit={handleAdd} className="add">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          autoFocus
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={todos.map((t) => t.id)} strategy={verticalListSortingStrategy}>
          <ul className="list">
            {todos.map((todo) => (
              <TodoItem key={todo.id} todo={todo} onToggle={handleToggle} onDelete={handleDelete} />
            ))}
          </ul>
        </SortableContext>
      </DndContext>

      {todos.length === 0 ? (
        <p className="empty">Nothing to do yet. Add your first task above!</p>
      ) : (
        <p className="count">{remaining} of {todos.length} left</p>
      )}
    </main>
  )
}

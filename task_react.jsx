import React, { useState } from "react";

// =====================================================
// Initial Task Data
// =====================================================

const initialTasks = [
  {
    id: 1,
    title: "Complete project report",
    description: "Finish the final project documentation",
    category: "Academic",
    priority: "High",
    status: "Pending",
    dueDate: "2026-08-25"
  },
  {
    id: 2,
    title: "Prepare presentation",
    description: "Create slides for the project presentation",
    category: "Academic",
    priority: "Medium",
    status: "In Progress",
    dueDate: "2026-08-27"
  },
  {
    id: 3,
    title: "Read research paper",
    description: "Review the latest software engineering paper",
    category: "Research",
    priority: "Low",
    status: "Completed",
    dueDate: "2026-08-20"
  }
];


// =====================================================
// Main Application
// =====================================================

function App() {

  const [tasks, setTasks] = useState(initialTasks);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("Academic");
  const [priority, setPriority] = useState("Medium");
  const [dueDate, setDueDate] = useState("");

  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("All");

  const [nextId, setNextId] = useState(4);


  // ===================================================
  // Add New Task
  // ===================================================

  const addTask = () => {

    if (!title.trim()) {
      alert("Task title is required");
      return;
    }

    if (!dueDate) {
      alert("Please select a due date");
      return;
    }

    const newTask = {
      id: nextId,
      title: title,
      description: description,
      category: category,
      priority: priority,
      status: "Pending",
      dueDate: dueDate
    };

    setTasks([...tasks, newTask]);

    setNextId(nextId + 1);

    setTitle("");
    setDescription("");
    setCategory("Academic");
    setPriority("Medium");
    setDueDate("");
  };


  // ===================================================
  // Delete Task
  // ===================================================

  const deleteTask = (id) => {

    const confirmed = window.confirm(
      "Are you sure you want to delete this task?"
    );

    if (!confirmed) {
      return;
    }

    const updatedTasks = tasks.filter(
      (task) => task.id !== id
    );

    setTasks(updatedTasks);
  };


  // ===================================================
  // Change Task Status
  // ===================================================

  const changeStatus = (id, newStatus) => {

    const updatedTasks = tasks.map((task) => {

      if (task.id === id) {
        return {
          ...task,
          status: newStatus
        };
      }

      return task;
    });

    setTasks(updatedTasks);
  };


  // ===================================================
  // Change Priority
  // ===================================================

  const changePriority = (id, newPriority) => {

    const updatedTasks = tasks.map((task) => {

      if (task.id === id) {
        return {
          ...task,
          priority: newPriority
        };
      }

      return task;
    });

    setTasks(updatedTasks);
  };


  // ===================================================
  // Search and Filter
  // ===================================================

  const filteredTasks = tasks.filter((task) => {

    const matchesSearch =
      task.title
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      task.description
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      task.category
        .toLowerCase()
        .includes(search.toLowerCase());

    const matchesStatus =
      filterStatus === "All" ||
      task.status === filterStatus;

    return matchesSearch && matchesStatus;
  });


  // ===================================================
  // Statistics
  // ===================================================

  const totalTasks = tasks.length;

  const pendingTasks = tasks.filter(
    (task) => task.status === "Pending"
  ).length;

  const progressTasks = tasks.filter(
    (task) => task.status === "In Progress"
  ).length;

  const completedTasks = tasks.filter(
    (task) => task.status === "Completed"
  ).length;


  // ===================================================
  // Clear Completed Tasks
  // ===================================================

  const clearCompleted = () => {

    const remainingTasks = tasks.filter(
      (task) => task.status !== "Completed"
    );

    setTasks(remainingTasks);
  };


  // ===================================================
  // Render Application
  // ===================================================

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f4f6f8",
        padding: "30px",
        fontFamily: "Arial, sans-serif"
      }}
    >

      {/* =================================================
          Header
      ================================================= */}

      <header
        style={{
          backgroundColor: "#ffffff",
          padding: "25px",
          borderRadius: "10px",
          marginBottom: "25px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
        }}
      >

        <h1
          style={{
            margin: 0,
            color: "#222"
          }}
        >
          Task Management Dashboard
        </h1>

        <p
          style={{
            color: "#666"
          }}
        >
          Create, manage, search and track your tasks.
        </p>

      </header>


      {/* =================================================
          Statistics
      ================================================= */}

      <section
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(4, 1fr)",
          gap: "15px",
          marginBottom: "25px"
        }}
      >

        <StatCard
          title="Total Tasks"
          value={totalTasks}
        />

        <StatCard
          title="Pending"
          value={pendingTasks}
        />

        <StatCard
          title="In Progress"
          value={progressTasks}
        />

        <StatCard
          title="Completed"
          value={completedTasks}
        />

      </section>


      {/* =================================================
          Add Task Form
      ================================================= */}

      <section
        style={{
          backgroundColor: "#ffffff",
          padding: "25px",
          borderRadius: "10px",
          marginBottom: "25px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
        }}
      >

        <h2>Add New Task</h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(2, 1fr)",
            gap: "15px"
          }}
        >

          <input
            type="text"
            placeholder="Task title"
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            style={inputStyle}
          />

          <input
            type="date"
            value={dueDate}
            onChange={(event) =>
              setDueDate(event.target.value)
            }
            style={inputStyle}
          />

          <textarea
            placeholder="Task description"
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            style={{
              ...inputStyle,
              minHeight: "80px"
            }}
          />

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "10px"
            }}
          >

            <select
              value={category}
              onChange={(event) =>
                setCategory(event.target.value)
              }
              style={inputStyle}
            >
              <option>Academic</option>
              <option>Research</option>
              <option>Personal</option>
              <option>Work</option>
              <option>Other</option>
            </select>

            <select
              value={priority}
              onChange={(event) =>
                setPriority(event.target.value)
              }
              style={inputStyle}
            >
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
            </select>

          </div>

        </div>

        <button
          onClick={addTask}
          style={buttonStyle}
        >
          Add Task
        </button>

      </section>


      {/* =================================================
          Search and Filters
      ================================================= */}

      <section
        style={{
          backgroundColor: "#ffffff",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "25px"
        }}
      >

        <div
          style={{
            display: "flex",
            gap: "15px",
            alignItems: "center"
          }}
        >

          <input
            type="text"
            placeholder="Search tasks..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            style={{
              ...inputStyle,
              flex: 1
            }}
          />

          <select
            value={filterStatus}
            onChange={(event) =>
              setFilterStatus(event.target.value)
            }
            style={inputStyle}
          >
            <option>All</option>
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>

          <button
            onClick={clearCompleted}
            style={{
              ...buttonStyle,
              backgroundColor: "#555"
            }}
          >
            Clear Completed
          </button>

        </div>

      </section>


      {/* =================================================
          Task List
      ================================================= */}

      <section>

        <h2>
          Tasks ({filteredTasks.length})
        </h2>

        {filteredTasks.length === 0 ? (

          <div
            style={{
              backgroundColor: "#ffffff",
              padding: "30px",
              borderRadius: "10px",
              textAlign: "center"
            }}
          >
            <p>No tasks found.</p>
          </div>

        ) : (

          <div
            style={{
              display: "grid",
              gap: "15px"
            }}
          >

            {filteredTasks.map((task) => (

              <TaskCard
                key={task.id}
                task={task}
                onDelete={deleteTask}
                onStatusChange={changeStatus}
                onPriorityChange={changePriority}
              />

            ))}

          </div>

        )}

      </section>

    </div>
  );
}


// =====================================================
// Statistics Card Component
// =====================================================

function StatCard({ title, value }) {

  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        padding: "20px",
        borderRadius: "10px",
        textAlign: "center",
        boxShadow:
          "0 2px 8px rgba(0,0,0,0.08)"
      }}
    >

      <h3
        style={{
          margin: "0 0 10px 0",
          color: "#777"
        }}
      >
        {title}
      </h3>

      <div
        style={{
          fontSize: "30px",
          fontWeight: "bold"
        }}
      >
        {value}
      </div>

    </div>
  );
}


// =====================================================
// Task Card Component
// =====================================================

function TaskCard({
  task,
  onDelete,
  onStatusChange,
  onPriorityChange
}) {

  return (
    <article
      style={{
        backgroundColor: "#ffffff",
        padding: "20px",
        borderRadius: "10px",
        boxShadow:
          "0 2px 8px rgba(0,0,0,0.08)"
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start"
        }}
      >

        <div>

          <h3
            style={{
              marginTop: 0
            }}
          >
            {task.title}
          </h3>

          <p>
            {task.description}
          </p>

        </div>

        <button
          onClick={() =>
            onDelete(task.id)
          }
          style={{
            border: "none",
            backgroundColor: "#e74c3c",
            color: "white",
            padding: "8px 12px",
            borderRadius: "5px",
            cursor: "pointer"
          }}
        >
          Delete
        </button>

      </div>


      {/* Task Details */}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          marginTop: "15px"
        }}
      >

        <span style={badgeStyle}>
          Category: {task.category}
        </span>

        <span style={badgeStyle}>
          Due: {task.dueDate}
        </span>

      </div>


      {/* Status */}

      <div
        style={{
          marginTop: "20px"
        }}
      >

        <label>
          Status:
        </label>

        <select
          value={task.status}
          onChange={(event) =>
            onStatusChange(
              task.id,
              event.target.value
            )
          }
          style={{
            marginLeft: "10px",
            padding: "8px"
          }}
        >

          <option>Pending</option>
          <option>In Progress</option>
          <option>Completed</option>

        </select>

      </div>


      {/* Priority */}

      <div
        style={{
          marginTop: "10px"
        }}
      >

        <label>
          Priority:
        </label>

        <select
          value={task.priority}
          onChange={(event) =>
            onPriorityChange(
              task.id,
              event.target.value
            )
          }
          style={{
            marginLeft: "10px",
            padding: "8px"
          }}
        >

          <option>Low</option>
          <option>Medium</option>
          <option>High</option>

        </select>

      </div>

    </article>
  );
}


// =====================================================
// Common Styles
// =====================================================

const inputStyle = {
  padding: "12px",
  border: "1px solid #ddd",
  borderRadius: "6px",
  fontSize: "14px",
  boxSizing: "border-box",
  width: "100%"
};


const buttonStyle = {
  marginTop: "20px",
  padding: "12px 20px",
  border: "none",
  borderRadius: "6px",
  backgroundColor: "#2563eb",
  color: "white",
  cursor: "pointer",
  fontSize: "15px"
};


const badgeStyle = {
  backgroundColor: "#f0f0f0",
  padding: "6px 10px",
  borderRadius: "5px",
  fontSize: "13px"
};


export default App;

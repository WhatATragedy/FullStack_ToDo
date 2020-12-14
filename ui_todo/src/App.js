import React, { useState, useEffect } from "react";
import "./App.css";
import axios from 'axios';

function Todo({ todo, index, completeTodo, removeTodo }) {
  return (
    <div
      className="todo"
      style={{ textDecoration: todo.is_completed ? "line-through" : "" }}
    >
      {todo.task}
      <div>
        <button onClick={() => completeTodo(index)}>Complete</button>
        <button onClick={() => removeTodo(index)}>X</button>
      </div>
    </div>
  );
}

function TodoForm({ addTodo }) {
  const [value, setValue] = React.useState("");

  const handleSubmit = e => {
    e.preventDefault();
    if (!value) return;
    addTodo(value);
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        className="input"
        value={value}
        onChange={e => setValue(e.target.value)}
      />
    </form>
  );
}

function App() {
  const [todos, setTodos] = React.useState([]);

  useEffect(() => {
    const getTodos = async () => {
      fetch("http://127.0.0.1:5000/todos/user/1")
        .then((response) => response.json())
        .then((data) => {
          setTodos(data);
        });
    };

    getTodos();
  }, []);

  const addTodo = text => {
    var task_id = 0
    axios.post('http://127.0.0.1:5000/todos/create', {
      "user_id": 1,
      "task": text,
      "is_completed": false,
      "priority": "low"
    })
    .then((response) => {
      task_id = response.data
    });
    const newTodos = [...todos, { 
      "user_id": 1,
      "task": text,
      "is_completed": false,
      "priority": "low",
      "task_id": task_id

     }];
    setTodos(newTodos);
  };

  const completeTodo = index => {
    const newTodos = [...todos];
    const todo = newTodos[index]
    console.log(todo)
    newTodos[index].is_completed = true;
    setTodos(newTodos);
    axios({
      method: 'post',
      url: `http://127.0.0.1:5000/todos/update/${todo.task_id}`,
      data: {
        "user_id": 1,
        "task": todo.text,
        "isCompleted": true,
        "priority": todo.priority
      }
    });
  };

  const removeTodo = index => {
    const newTodos = [...todos];
    const todo = newTodos[index]
    newTodos.splice(index, 1);
    setTodos(newTodos);
    axios.post(`http://127.0.0.1:5000/todos/delete/${todo.task_id}`)
  };

  return (
    <div className="app">
      <div className="todo-list">
        {todos.map((todo, index) => (
          <Todo
            key={index}
            index={index}
            todo={todo}
            completeTodo={completeTodo}
            removeTodo={removeTodo}
          />
        ))}
        <TodoForm addTodo={addTodo} />
      </div>
    </div>
  );
}

export default App;
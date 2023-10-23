"use client";
import { apiHost } from "@/constants";
import React from "react";
import Link from "next/link";

export default function Items() {
  // Get items
  const [items, setItems] = React.useState<
    Record<string, { id: string; description: string }>
  >({});
  React.useEffect(() => {
    fetch(`${apiHost}/items`)
      .then((res) => res.json())
      .then((json) => setItems(json));
  }, []);

  const [newItem, setNewItem] = React.useState("");
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch(`${apiHost}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: newItem,
        id: new Date().toISOString(),
      }),
    })
      .then((res) => res.json())
      .then((json) => {
        setItems((items) => ({ ...items, [json.id]: json }));
        setNewItem("");
      });
  };

  return (
    <main>
      <Link href="/">Home</Link>
      <h1>Items</h1>
      <h2>Current items</h2>
      <ul>
        {Object.values(items).map((item) => (
          <li key={item.id}>{item.description}</li>
        ))}
      </ul>
      <h2>Add a new item</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>
    </main>
  );
}

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
    </main>
  );
}

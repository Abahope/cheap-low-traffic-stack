import Link from "next/link";
import LambdaWarmer from "./LambdaWarmer";

export default function Home() {
  return (
    <main>
      <LambdaWarmer />
      <Link href="/items">Items</Link>
      <h1>Home</h1>
      <p>
        Look here while the Lambda warms up or the items page might be slow!
      </p>
    </main>
  );
}

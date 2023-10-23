import LambdaWarmer from "./LambdaWarmer";

export default function Home() {
  return (
    <main>
      <LambdaWarmer />
      <h1>Home</h1>
      <p>
        Look here while the Lambda warms up or the items page might be slow!
      </p>
    </main>
  );
}

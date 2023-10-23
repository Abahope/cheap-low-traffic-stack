let apiHost = "";

if (!process.env.NEXT_PUBLIC_API_HOST) {
  throw new Error("NEXT_PUBLIC_API_HOST is not set");
} else {
  apiHost = process.env.NEXT_PUBLIC_API_HOST;
}

export { apiHost };

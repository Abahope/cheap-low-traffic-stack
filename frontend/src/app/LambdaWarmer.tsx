"use client";
import React from "react";
import { apiHost } from "@/constants";

export default function LambdaWarmer() {
  React.useEffect(() => {
    fetch(`${apiHost}`);
  }, []);
  return null;
}

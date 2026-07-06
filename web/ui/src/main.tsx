import { mountApp } from "./App";

const root = document.getElementById("root");

if (!root) {
  throw new Error("Missing root element");
}

mountApp(root);

import client from "./client";

export async function runSimulation(params) {
  const { data } = await client.post("/simulate", params);
  return data;
}

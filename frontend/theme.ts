export const colors = {
  bg: "#0d1117", card: "#161b22", border: "#30363d",
  text: "#e6edf3", muted: "#8b949e", accent: "#58a6ff",
  green: "#3fb950", yellow: "#d29922", red: "#f85149",
};
export function levelColor(value: number, limit: number): string {
  const ratio = value / limit;
  if (ratio >= 1.5) return colors.red;
  if (ratio >= 1) return colors.yellow;
  return colors.green;
}
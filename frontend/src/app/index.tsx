import { StyleSheet, Text, View, useWindowDimensions } from "react-native";
import { colors, levelColor } from "../../theme";
import { Ring } from "../../components/Ring";
import { useEffect, useState } from "react";
import { ForecastChart } from "../../components/ForecastChart";
import { StatCard } from "../../components/StatCard";

const API = "http://10.22.252.97:8000";
const LIMIT = 50;

type Day = { day: string; mean: number; level: string };
type Point = { time: string; value: number | null };
type Span = { start: string; end: string; hours: number; peak: number };

const pad = (n: number) => String(n).padStart(2, "0");
const hhmm = (iso: string) => { const d = new Date(iso); return `${pad(d.getHours())}:${pad(d.getMinutes())}`; };
const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export default function Index() {
  const { width } = useWindowDimensions();
  const [days, setDays] = useState<Day[]>([]);
  const [points, setPoints] = useState<Point[]>([]);
  const [spans, setSpans] = useState<Span[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/forecast`)
      .then((r) => r.json())
      .then((data) => { setDays(data.days); setPoints(data.points); setSpans(data.windows); })
      .catch((e) => setError(String(e)));
  }, []);

  const todayKey = points[0] ? new Date(points[0].time).toDateString() : "";
  const today = points.filter((p) => new Date(p.time).toDateString() === todayKey);
  const peak = today.reduce<Point | null>(
    (best, p) => (p.value !== null && (best === null || p.value > (best.value ?? 0)) ? p : best), null);
  const span = spans.find((s) => new Date(s.start).toDateString() === todayKey);
  const color = days[0] ? levelColor(days[0].mean, LIMIT) : colors.text;

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Ragweed Alert</Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {days[0] && <Ring value={days[0].mean} limit={LIMIT} />}
      {days[0] && <Text style={[styles.status, { color }]}>{cap(days[0].level)} day</Text>}
      {peak && <Text style={styles.muted}>Peak around {hhmm(peak.time)}</Text>}
      {points.length > 1 && days[0] && (
        <View style={styles.card}>
          <Text style={styles.muted}>Next 72 hours</Text>
          <ForecastChart points={points} color={color} width={width - 58} />
        </View>
      )}
      {peak && (
        <View style={styles.cards}>
          <StatCard label="Today's peak" value={String(Math.round(peak.value ?? 0))} sub={`at ${hhmm(peak.time)}`} />
          <StatCard label="High hours" value={span ? `${hhmm(span.start)}–${hhmm(span.end)}` : "None"} sub="today" />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, alignItems: "center", justifyContent: "center" },
  title: { color: colors.text, fontSize: 28, fontWeight: "700", marginBottom: 16 },
  error: { color: colors.red, marginBottom: 12 },
  status: { fontSize: 16, fontWeight: "600", marginTop: 12 },
  muted: { color: colors.muted, fontSize: 12, marginBottom: 4 },
  card: { backgroundColor: colors.card, borderColor: colors.border, borderWidth: 1, borderRadius: 12, padding: 12, marginTop: 16 },
  cards: { flexDirection: "row", gap: 12, width: "100%", paddingHorizontal: 16, marginTop: 12 },
});
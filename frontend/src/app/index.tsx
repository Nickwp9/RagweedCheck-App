import { StyleSheet, Text, View } from "react-native";
import { colors } from "../../theme";
import { Ring } from "../../components/Ring";
import { useEffect, useState } from "react";

const API = "http://10.22.252.97:8000";
const LIMIT = 50;

type Day = { day: string; mean: number; level: string };

export default function Index() {
  const [days, setDays] = useState<Day[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/forecast`)
      .then((r) => r.json())
      .then((data) => setDays(data.days))
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Ragweed Alert</Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {days[0] && <Ring value={days[0].mean} limit={LIMIT} />}
      {days[0] && <Text style={styles.row}>{days[0].level}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, alignItems: "center", justifyContent: "center" },
  title: { color: colors.text, fontSize: 28, fontWeight: "700", marginBottom: 24 },
  error: { color: colors.red, marginBottom: 12 },
  row: { color: colors.text, fontSize: 16, marginTop: 12 },
});
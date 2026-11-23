import { StyleSheet, Text, View } from "react-native";
import { colors } from "../theme";

type Props = { label: string; value: string; sub?: string; color?: string };

export function StatCard({ label, value, sub, color = colors.text }: Props) {
  return (
    <View style={styles.card}>
      <Text style={styles.label}>{label}</Text>
      <Text style={[styles.value, { color }]}>{value}</Text>
      {sub ? <Text style={styles.label}>{sub}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: { flex: 1, backgroundColor: colors.card, borderColor: colors.border, borderWidth: 1, borderRadius: 12, padding: 12 },
  label: { color: colors.muted, fontSize: 12 },
  value: { fontSize: 20, fontWeight: "700", marginVertical: 4 },
});
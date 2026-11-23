import { Text, View } from "react-native";
import Svg, { Circle } from "react-native-svg";
import { colors, levelColor } from "../theme";

type Props = { value: number; limit: number; size?: number };

export function Ring({ value, limit, size = 176 }: Props) {
  const stroke = 12, mid = size / 2, r = (size - stroke) / 2, c = 2 * Math.PI * r;
  const filled = Math.min(value / limit, 1) * c;
  return (
    <View style={{ width: size, height: size, alignItems: "center", justifyContent: "center" }}>
      <Svg width={size} height={size}>
        <Circle cx={mid} cy={mid} r={r} stroke="#21262d" strokeWidth={stroke} fill="none" />
        <Circle cx={mid} cy={mid} r={r} stroke={levelColor(value, limit)} strokeWidth={stroke} fill="none"
          strokeLinecap="round" strokeDasharray={`${filled} ${c}`} rotation={-90} origin={`${mid}, ${mid}`} />
      </Svg>
      <Text style={{ position: "absolute", color: colors.text, fontSize: 44, fontWeight: "700" }}>{Math.round(value)}</Text>
    </View>
  );
}
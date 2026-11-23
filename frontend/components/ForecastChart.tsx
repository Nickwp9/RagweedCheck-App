import Svg, { Path, Text as SvgText } from "react-native-svg";
import { colors } from "../theme";

type Point = { time: string; value: number | null };
type Props = { points: Point[]; color: string; width: number; height?: number };

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export function ForecastChart({ points, color, width, height = 130 }: Props) {
  const top = 8, plotH = height - top - 24;
  const maxY = Math.max(1, ...points.map((p) => p.value ?? 0));
  const x = (i: number) => (i / (points.length - 1)) * width;
  const y = (v: number) => top + plotH - (v / maxY) * plotH;
  const line = points.map((p, i) => `${i === 0 ? "M" : "L"}${x(i)},${y(p.value ?? 0)}`).join(" ");
  const noons = points.map((p, i) => ({ i, d: new Date(p.time) })).filter(({ d }) => d.getHours() === 12);
  return (
    <Svg width={width} height={height}>
      <Path d={`${line} L${width},${y(0)} L0,${y(0)} Z`} fill={color} fillOpacity={0.15} />
      <Path d={line} fill="none" stroke={color} strokeWidth={2} strokeLinejoin="round" />
      {noons.map(({ i, d }) => (
        <SvgText key={i} x={x(i)} y={height - 6} fill={colors.muted} fontSize={11} textAnchor="middle">
          {DAYS[d.getDay()]}
        </SvgText>
      ))}
    </Svg>
  );
}
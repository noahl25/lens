"use client"

import { TrendingUp } from "lucide-react"
import { Label, PolarRadiusAxis, RadialBar, RadialBarChart } from "recharts"

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

export default function DashboardRadial({ title, subtitle, label, min, max, number, rightLabel, leftLabel, labelColor = "red" }) {

    let pct = (number - min) / (max - min) * 100;
    pct = pct.toFixed(2);
    const chartData = [{ [leftLabel]: Math.round(pct), [rightLabel]: Math.round(100 - pct) }]

    return (
        <Card className="pt-0 bg-black text-white border-white/20 border-2 col-span-1 row-span-1">
            <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>{title}</CardTitle>
                    <CardDescription>
                        {subtitle}
                    </CardDescription>
                </div>
            </CardHeader>
            <CardContent className="flex flex-1 items-center justify-center pb-0">
                <ChartContainer
                    className="mx-auto aspect-square w-full max-w-[250px] relative translate-y-1/8"
                    config={{
                        [rightLabel]: { color: "" },
                        [leftLabel]: { color: "" }
                    }}
                >
                    <RadialBarChart
                        data={chartData}
                        endAngle={180}
                        innerRadius={80}
                        outerRadius={130}
                    >
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent hideLabel />}
                        />
                        <PolarRadiusAxis tick={false} tickLine={false} axisLine={false}>
                            <Label
                                content={({ viewBox }) => {
                                    if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                                        return (
                                            <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle" fill={labelColor === "red" ? "rgba(128, 0, 0, 1)" : "rgba(43, 128, 0, 1)"}>
                                                <tspan
                                                    x={viewBox.cx}
                                                    y={(viewBox.cy || 0) - 16}
                                                    className="text-2xl font-bold"
                                                >
                                                    {number}
                                                </tspan>
                                                <tspan
                                                    x={viewBox.cx}
                                                    y={(viewBox.cy || 0) + 4}
                                                    className="text-sm"
                                                >
                                                    {label}
                                                </tspan>
                                            </text>
                                        )
                                    }
                                }}
                            />
                        </PolarRadiusAxis>
                        <RadialBar
                            dataKey={rightLabel}
                            stackId="a"
                            cornerRadius={5}
                            fill="rgba(128, 0, 0, 1)"
                            className="stroke-transparent stroke-2"
                        />
                        <RadialBar
                            dataKey={leftLabel}
                            fill="#007d00ff"
                            stackId="a"
                            cornerRadius={5}
                            className="stroke-transparent stroke-2"
                        />
                    </RadialBarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

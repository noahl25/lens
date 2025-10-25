"use client"
import * as React from "react"
import { useState, useEffect } from "react"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartContainer,
} from "@/components/ui/chart"

export function LineGraph({ data, title, subtitle}) {

    const [yDomain, setYDomain] = useState([0, 0]);
    
    const values = data.map(d => d.line);
    const min = Math.min(...values);
    const max = Math.max(...values);

    useEffect(() => {
        
        if (data && data.length > 0) {

            const padding = (max - min) * 0.1;
            setYDomain([min - padding, max + padding]);
        }

    }, [data])

    const chartConfig = {
        "line": {
            label: "Line",
            color: "var(--chart-1)",
        },
    };
    
    return (
        <Card className="pt-0 bg-black text-white border-white/20 border-2 col-span-2 flex flex-col h-full">
            <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>{title}</CardTitle>
                    <CardDescription>
                        {subtitle}
                    </CardDescription>
                </div>
            </CardHeader>
            <CardContent className="flex-1 flex items-center justify-center">
                <ChartContainer
                    config={chartConfig}
                    className="h-[300px] bg-black rounded-lg mx-auto w-full max-w-[800px] mr-10"
                >
                    <AreaChart data={data} className="p-2">
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="date"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            minTickGap={32}
                            tickFormatter={(value) => {
                                const date = new Date(value)
                                return date.toLocaleDateString("en-US", {
                                    month: "short",
                                    day: "numeric",
                                })
                            }}
                        />
                        <YAxis
                            tickFormatter={
                                (value) => {
                                    return value.toExponential(2);
                                }
                            }
                            domain={[_ => {
                                if (!data || data.length === 0) return 0;
                                const values = data.map(d => d.line);
                                const min = Math.min(...values);
                                const max = Math.max(...values);
                                const padding = (max - min) * 0.1 || 1;
                                return min - padding;
                            }, _ => {
                                if (!data || data.length === 0) return 1;
                                const values = data.map(d => d.line);
                                const max = Math.max(...values);
                                const min = Math.min(...values);
                                const padding = (max - min) * 0.1 || 1;
                                return max + padding;
                            }]}

                        />
                        <Area
                            dataKey="line"
                            type="natural"
                            fill="url(#fillline)"
                            stroke="var(--color-line)"
                            stackId="a"
                        />
                    </AreaChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

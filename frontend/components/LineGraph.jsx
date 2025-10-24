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

    const [key, setKey] = useState("");

    console.log(data)
    
    useEffect(() => {
        for (let key in data[0]) {
            if (data[0].hasOwnProperty(key)) { 
                setKey(key);
            }
        }
    }, [])

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
                        <defs>
                            <linearGradient id="fillline" x1="0" y1="0" x2="0" y2="1">
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-line)"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-line)"
                                    stopOpacity={0.1}
                                />
                            </linearGradient>

                        </defs>
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
                        <YAxis/>
                        <Area
                            dataKey={key}
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

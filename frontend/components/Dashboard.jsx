'use client'

import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { fontBasic } from "@/app/layout";
import { Search, X } from "lucide-react";
import { LineGraph } from "./LineGraph";
import DashboardTable from "./DashboardTable";
import Summary from "./Summary";
import DashboardRadial from "./DashboardRadial";
import Reccomended from "./Reccomended";

export default function Dashboard({ query }) {

    const chartData = [
        { date: "2024-04-01", line: 222 },
        { date: "2024-04-02", line: 97},
        { date: "2024-04-03", line: 167 },
    ]

    return (
        <div className="w-full h-full pb-10 overflow-x-hidden">
            <div className={`mt-[85px] max-w-6xl mx-auto text-white ${fontBasic.className}`}>
                <div className="flex items-center justify-between gap-6 mb-5">
                    <div>
                        <h1 className="text-5xl">Dashboard</h1>
                        <p className="text-xs text-white/60 relative translate-x-[2px] mt-1">Explore your AI-powered results.</p>
                    </div>
                    <div>
                        <div className="w-[500px] h-12 rounded-4xl backdrop-blur-md border-2 border-white/50 relative flex">
                            <input placeholder={query} type="text" className="text-sm ml-12 mr-4 focus:outline-none w-full"></input>
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2" color="#ffffff74" />
                        </div>
                        <p className="text-xs text-center text-white/60 mt-2">Press Enter to search.</p>
                    </div>
                </div>
                <div className="grid grid-flow-row-dense grid-cols-3 gap-10 auto-rows-min auto-flow-dense">
                    <LineGraph data={chartData} title={"Hello!"} subtitle={"Hello world!"}/>
                    <DashboardTable title={"Hello"} subtitle={"Hello world"} headers={["Btc", "Eth"]} data={[["price", "1", "2"]]}/>
                    <DashboardRadial title={"Hello"} subtitle={"Hello world"} label={"Sentiment"} min={-1} max={1} number={-0.25} leftLabel={"Positive"} rightLabel={"Negative"}/>
                    <Summary title={"Hello"} subtitle={"Hello world"} text={"Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum. Lorem impsum."}/>
                    <Reccomended reccomended={[
                        {
                            image: "https://www.purina.com/sites/default/files/styles/2x1_small/public/2024-08/eco_126_puppyteething.jpg?itok=rv6wURzz"
                        },
                        {
                            image: "https://www.purina.com/sites/default/files/styles/2x1_small/public/2024-08/eco_126_puppyteething.jpg?itok=rv6wURzz"
                        },
                    ]}/>
                </div>
            </div>
        </div>
    );
}
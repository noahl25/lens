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
import DashboardComponents from "./DashboardComponents";

export default function Dashboard({ query }) {

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
                    <DashboardComponents/>
                </div>
            </div>
        </div>
    );
}
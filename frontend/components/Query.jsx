'use client'

import { Search } from "lucide-react";
import { useState, useRef } from "react";
import TypewriterTextComponent from "./Typewriter";
import { useRouter } from "next/navigation";

export default function Query({ setQuery }) {

    const [showExamples, setShowExamples] = useState(true);
    const [exampleIndex, setExampleIndex] = useState(0);

    const examples = [
        "How has sentiment on $ADA changed over the last 7 days?",
        "Show Bitcoin's price history and market fear/greed over the past month.",
        "Show me trending topics about $BTC.",
    ]

    const inputRef = useRef();

    const onSubmit = () => {

        setQuery(inputRef.current.value.trim());

    }

    return (
        <>
            <div className="rounded-4xl p-10 bg-transparent whitespace-nowrap overflow-hidden text-[70px] text-white z-5">
                <div className="text-center" style={{ lineHeight: 1 }}>
                    <p className="text-[200px] text-white">LENS</p>
                    <p className="text-[20px] text-neutral-200 font-thin">Explore AI-powered, real-time blockchain metrics and sentiment.</p>
                </div>

                <div className="w-120% h-12 mt-5 rounded-4xl backdrop-blur-md border-1 border-white/20 relative flex">
                    <TypewriterTextComponent examples={examples} showExamples={showExamples} exampleIndex={exampleIndex} setExampleIndex={setExampleIndex}/>
                    <input type="text" ref={inputRef} className="text-sm ml-12 mr-4 focus:outline-none w-full" onKeyDown={(e) => e.key === "Enter" && onSubmit()} onClick={() => { setShowExamples(false); }} onBlur={() => { setShowExamples(true); }}></input>
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2" color="#ffffff58"/>
                </div>
                <p className="text-xs text-white/60 mt-2 text-center">Press Enter to search</p>
            </div>
        </>
    );

}